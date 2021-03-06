from contextlib import closing
import http.client
from tempfile import SpooledTemporaryFile
import utils


class DFSError(IOError):
    """To send error in case of file locked"""

    pass


class File(SpooledTemporaryFile):
    """Is a distant file, it's stored in memory if it size if less than
       the max_size parameter, otherwise it's stored on the disk.
    """

    def __init__(self, filepath, mode='rtc'):
        """filepath: the path of the distant file
        """
        self.mode = mode
        self.filepath = filepath
        host, port = utils.get_host_port(config['nameserver'])
        self.srv = utils.get_server(filepath, host, port)

        if self.srv is None:
            raise DFSError('Impossible to find a server that serve %s.'
                    % filepath)

        self.last_modified = None
        SpooledTemporaryFile.__init__(self, config['max_size'], mode.replace('c', ''))

        host, port = utils.get_host_port(config['lockserver'])
        if utils.is_locked(filepath, host, port):
            raise DFSError('The file %s is locked.' % filepath)

        if 'w' not in mode:
            host, port = utils.get_host_port(self.srv)
            with closing(http.client(host, port)) as con:
                con.request('GET', filepath)
                response = con.getresponse()
                self.last_modified = response.getheader('Last-Modified')
                status = response.status

                if status not in (200, 204):
                    raise DFSError('Error (%d) while opening file.' % status)

                if status != 204:
                    self.write(response.read())

                if 'r' in mode:
                    self.seek(0)

                self.lock_id = None

        if 'a' in mode or 'w' in mode:
            # automatically gets a lock if we're in write/append mode
            host, port = utils.get_host_port(config['lockserver'])
            self.lock_id = int(utils.get_lock(filepath, host, port))

        if 'c' in mode:
            File._cache[filepath] = self

    def __exit__(self, exc, value, tb):
        """Send the change to the DFS, and close the file."""

        self.close()

        if 'c' not in self.mode:
            return SpooledTemporaryFile.__exit__(self, exc, value, tb)

        return False

    def close(self):
        """Send the change to the DFS, and close the file."""

        self.flush()

        if 'c' not in self.mode:
            SpooledTemporaryFile.close(self)

    def flush(self):
        """Flush the data to the server."""

        SpooledTemporaryFile.flush(self)
        self.commit()

    def commit(self):
        """Send the local file to the remote fileserver."""

        if 'a' in self.mode or 'w' in self.mode:
            # send the file from the begining
            self.seek(0)
            data = self.read()
            host, port = utils.get_host_port(self.srv)
            with closing(http.client(host, port)) as con:
                con.request('PUT', self.filepath + '?lock_id=%s' % self.lock_id,
                            data)

                response = con.getresponse()
                #self.last_modified = response.getheader('Last-Modified')
                status = response.status
                if status != 200:
                    raise DFSError('Error (%d) while committing change to'
                                     ' the file.' % status)

        if self.lock_id is not None:
            host, port = utils.get_host_port(config['lockserver'])
            utils.revoke_lock(self.filepath, host, port, self.lock_id)

    @staticmethod
    def from_cache(filepath):
        """save file in local disk"""
        if filepath in File._cache:
            f = File._cache[filepath]

            host, port = utils.get_host_port(config['nameserver'])
            fs = utils.get_server(filepath, host, port)
            host, port = utils.get_host_port(fs)

            with closing(http.client(host, port)) as con:
                con.request('HEAD', filepath)

                if (f.last_modified ==
                        con.getresponse().getheader('Last-Modified')):
                    f.seek(0)
                    return f
                else:
                    del File._cache[filepath]

        return None


def unlink(filepath, lock_id=None):
    """Delete the file from the filesystem.
       If lock_id is provided, it's used to delete the file."""
    
    host, port = utils.get_host_port(config['nameserver'])
    fs = utils.get_server(filepath, host, port)
    host, port = utils.get_host_port(fs)

    with closing(http.client(host, port)) as con:
        con.request('DELETE', filepath + '?lock_id=%s' % lock_id)

        status = con.getresponse().status

        if status != 200:
            raise DFSError('Error (%d) while deleting %s.' %
                             (status, filepath))



open = File

config = {
        'nameserver': None,
        'lockserver': None,
        'max_size': 1024 ** 2,
         } # default
File._cache = {}
utils.load_config(config, 'client.dfs.json')




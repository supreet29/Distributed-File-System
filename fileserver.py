import logging
import os.path
import time

from contextlib import closing
from httplib import HTTPConnection

import web

import utils

class FileServer:
    """File Server is responsible for holding and sharing file"""

    def GET(self, filepath):
        """Return the file if it's not locked"""
    
        _raise_if_locked(filepath)
        _raise_if_not_exists(filepath)
        _raise_if_dir_or_not_servable(filepath)
    
    
        p = _get_local_path(filepath)
        with open(p) as f:
        return f.read()

    def DELETE(self, filepath):
        """Remove the filepath if it's not locked, or if the correct
        lock_id matches in 'lock_id'."""
    
        _raise_if_locked(filepath)
        _raise_if_not_exists(filepath)
        _raise_if_dir_or_not_servable(filepath)
    
    
        os.unlink(_get_local_path(filepath))
        return 'OK'

    def PUT(self, filepath):
        """Replace the file."""
        
        _raise_if_locked(filepath)
        _raise_if_dir_or_not_servable(filepath)
        
        p = _get_local_path(filepath)
        
        with open(p, 'w') as f:
            f.write(web.data())
        
        return ''

    def HEAD(self, filepath):
        
        _raise_if_locked(filepath)
        _raise_if_not_exists(filepath)
        _raise_if_dir_or_not_servable(filepath)

        p = _get_local_path(filepath)
        
        return ''

def _get_local_path(filepath):
    """ Convert the file path to the absolute path"""
    return os.path.join(os.getcwd(), _config['fsroot'], filepath[1:])

def _raise_if_locked(filepath):
    """Raise a unauthorized if the filepath is locked, and no
         lock wasn't given in the request."""
    
    i = web.input()
    
    host, port = utils.get_host_port(_config['lockserver'])
    if utils.is_locked(filepath, host, port, i.get('lock_id', None)):
        raise web.unauthorized()

def _raise_if_dir_or_not_servable(filepath):
    """Raise if the filepath isn't present, or if it's a directory."""
    
    p = _get_local_path(filepath)
    
    if (os.path.dirname(filepath) not in _config['directories'] or
        os.path.isdir(p)):
        # request a file which this server isn't supposed to serve!
        raise web.notacceptable()


def _raise_if_not_exists(filepath):
    """Raise if the file doesn't exists."""
    
    p = _get_local_path(filepath)
    
    if not os.path.exists(p):
        raise web.webapi.HTTPError('No Content',
                                   {'Content-Type': 'plain/text'})


def _init_file_server():
    """Just notify the nameserver about which directories we serves."""
    
    host, port = utils.get_host_port(_config['nameserver'])
    with closing(HTTPConnection(host, port)) as con:
        data = 'srv=%s&dirs=%s' % (_config['srv'],
                                   '\n'.join(_config['directories']),)
        con.request('POST', '/', data)


_config = {
        'nameserver': None,
        'directories': [],
        'fsroot': 'fs/',
        'srv': None,
    }

logging.info('Loading config file fileserver.json.')

# just to speed up the search to know if we can serve a file
# O(n) → O(log n)
_config['directories'] = set(_config['directories'])







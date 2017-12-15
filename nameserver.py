import os
import web
import shelve
import logging

urls = (
        '/filepath/(.*)', 'NameServer'
        )

class NameServer:
    """Nameserver is used for the mapping between the directories and file server."""
    
_names = shelve.open('dbfile')

def GET(self, filepath):
    
    filepath = str(filepath)
    dirpath = str(os.path.dirname(filepath))
    if filepath == '/':
        return '\n'.join('%s=%s' % (dirpath, _names[dirpath])
                for dirpath in sorted(_names))
    
        
    if dirpath in _names:
        return _names[dirpath]

    raise web.notfound('No file server serve this file.')


_names = shelve.open('dbfile')
_names.close()

"""
    filename = ""
    if '*' in filepath:
        dirname = open.shelve("NameServer")
        print(dirname)
        dirname.close()
           
        if not filepath:
            return "No such file or directory"
    
    dirname=open.shelve("NameServer")

    try:
        filename = dirname[filepath]
    finally:
        dirname.close()
    return filename
"""

def POST(self, filepath):
    filepath = str(filepath)
    dirpath = str(os.path.dirname(filepath))
    return update(str(dirpath))

def DELETE(self, filepath):
    filepath = str(filepath)
    dirpath = str(os.path.dirname(filepath))
    return update(str(dirpath), False)
        
    
def update(dirpath, add=True):
    web.header('Content-Type', 'text/plain; charset=UTF-8')
    i = web.input()
    
    if 'srv' not in i:
        raise web.badrequest()

    srv = i['srv']

    if dirpath == '/':
        if 'dirs' not in i:
            raise web.badrequest()

        for dirpath in i['dirs'].split('\n'):
            if not dirpath:
                continue

            try:
                update_names(dirpath, srv, add)
            except ValueError as e:
                logging.exception(e)

    else:
        try:
            update_names(dirpath, srv, add)
        except ValueError as e:
            logging.exception(e)
            
    return 'OK'        
        
def update_names(dirpath, srv, add=True):
        if dirpath[-1] == '/':
            dirpath = os.path.dirname(dirpath)

        if add:
            logging.info('Update directory %s on %s.', dirpath, srv)
            _names[dirpath] = srv

        elif dirpath in _names:
            logging.info('Remove directory %s on %s.', dirpath, srv)
            del _names[dirpath]

        else:
            raise ValueError('%s wasn\'t not deleted, because it wasn\'t'
                         ' in the dictionnary/database.' % dirpath)
            
if __name__=="__main__":
    app = web.application(urls,globals())
    app.run()

import atexit
import logging
import os
import shelve

import web

import utils

class NameServer:
    """Nameserver is used for the mapping between the directories and file server."""

def GET(self, filepath):
    """Returs the directory in which file path is mentioned if filepath is "/" then it returns
    a whole directory"""

    web.header('Content-Type', 'text/plain; charset=UTF-8')
        filepath = str(filepath)
        
        if filepath == '/':
            return '\n'.join('%s=%s' % (dirpath, _names[dirpath])
                    for dirpath in sorted(_names))

        dirpath = str(os.path.dirname(filepath))

        if dirpath in _names:
            return _names[dirpath]

        raise web.notfound('No file found in the server')


def POST(self, dirpath):
        """See _update (with add=True)"""

        return _update(str(dirpath))
    
def DELETE(self, dirpath):
        """See _update (with add=False)"""

        return _update(str(dirpath), False)
    
    
def _update(dirpath, add=True):
    """Adding directories to the name server"""
    
    """ If directory path is root then it will create list of directories 
    in dirs, associate the query to name server and store in the srv
    
    other wise it will remove the directory name in the same way instead of 
    adding them"""
    
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
            
            _update_names(dirpath, srv, add)
        
        else:
            _update_names(dirpath, srv, add)
            
       """ Return OK in case of valueError because we have to delete the 
       directory from the name server list and in case of null value it seems 
       like we've done that. """
       
    return 'OK'
            
            
            

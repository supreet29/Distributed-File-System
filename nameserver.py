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

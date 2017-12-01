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

    """web.header()"""
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
    
   """ web.header()"""
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
                _update_names(dirpath, srv, add)
            except ValueError as e:
                logging.exception(e)

    else:
        try:
            _update_names(dirpath, srv, add)
        except ValueError as e:
            logging.exception(e)
            
            
       """ Return OK in case of valueError because we have to delete the 
       directory from the name server list and in case of null value it seems 
       like we've done that. """
       
    return 'OK'

""" updating the name dictionary"""

def _update_names(dirpath, srv, add=True):
    """dirpath: To update the directory path.
       srv: To associate the dirpath to the server in case of add is false.
       add: if True then it add the couple (dirpath, srv) otherwise delete the 
       dirpath from the dictionnary."""
       
       
    if dirpath[-1] == '/':
        dirpath = os.path.dirname(dirpath)
        
        if dirpath[-1] == '/':
        dirpath = os.path.dirname(dirpath)

    if add:
        logging.info('Update directory %s on %s.', dirpath, srv)
        _names[dirpath] = srv

    elif dirpath in _names:
        logging.info('Remove directory %s on %s.', dirpath, srv)
        del _names[dirpath]
        
    
    else:
        raise ValueError('%s not deleted, because it was not'
                         ' in the dictionnary/.' % dirpath)
        
 
_config = {
            'dbfile': 'names.db',
         }

logging.info('Loading config file nameserver.json.')
utils.load_config(_config, 'nameserver.json')
_names = shelve.open(_config['dbfile'])

atexit.register(lambda: _names.close())
            
            
            

import web
import os
import logging
import utils
from contextlib import closing
import http.client

urls = (
        '/filepath/(.*)', 'Fileserver'
        )

class Fileserver:
    def GET(self,filepath):
        # To open and read the requested file (filepath is passed).
        i = web.input()
        
        host, port = utils.get_host_port(_config['lockserver'])
        if utils.is_locked(filepath, host, port, i.get('lock_id', None)):
            raise web.unauthorized()
    
        
        p = os.path.join(os.getcwd(), _config['fsroot'], filepath[1:])
        
        if (os.path.dirname(filepath) not in _config['directories'] or
            os.path.isdir(p)):
            # request a file which this server isn't supposed to serve!
            raise web.notacceptable()
            
            if not os.path.exists(p):
                raise web.webapi.HTTPError('204 No Content',
                                           {'Content-Type': 'plain/text'})
                    
                    with open(p) as f:
                        return f.read()

def PUT(self, filepath):
    """Replace the file by the data in the request."""
        i = web.input()
        
        host, port = utils.get_host_port(_config['lockserver'])
        if utils.is_locked(filepath, host, port, i.get('lock_id', None)):
            raise web.unauthorized()
    
    
        p = os.path.join(os.getcwd(), _config['fsroot'], filepath[1:])
        
        if (os.path.dirname(filepath) not in _config['directories'] or
            os.path.isdir(p)):
            # request a file which this server isn't supposed to serve!
            raise web.notacceptable()
            
            if not os.path.exists(p):
                raise web.webapi.HTTPError('204 No Content',
                                           {'Content-Type': 'plain/text'})
                    
                    with open(p, 'w') as f:
                        f.write(web.data())
                            
                            return ''

_config = {
    'lockserver': None,
        'nameserver': None,
        'directories': [],
        'fsroot': 'fs/',
        'srv': None,
    }

logging.info('Loading config file fileserver.dfs.json.')
utils.load_config(_config, 'fileserver.dfs.json')

# just to speed up the search to know if we can serve a file
# O(n) → O(log n)
_config['directories'] = set(_config['directories'])

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

import web
import os
import logging
import utils
from contextlib import closing
import http.client
import time

urls = (
        '/filepath/(.*)', 'Fileserver'
        )

class Fileserver:
    def GET(self,filepath):
        # To open and read the requested file (filepath is passed).
        
        #p = os.path.isfile(filepath)
        print("inside get")
        if os.path.isfile(filepath):
            with open(filepath) as f:
                return f.read()
        else:
            return "wrong path"

def PUT(self, filepath):
    """Replace the file by the data in the request."""
        
        p = os.path.isfile(filepath)
        
        with open(filepath, 'w') as f:
            print(web.data())
            f.write(web.data().decode())

    return ''

def DELETE(self, filepath):
    os.unlink(_get_local_path(filepath))
    return 'OK'

def HEAD(self, filepath):
    p = _get_local_path(filepath)
        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))
        return ''

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


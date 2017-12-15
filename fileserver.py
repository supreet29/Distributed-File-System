import web
import os
import logging
import utils


urls = (
    '/filepath/(.*)', 'Fileserver'
)

class Fileserver:
    def GET(self,filepath):
        # To open and read the requested file (filepath is passed).
        
        #p = os.path.isfile(filepath)
        print("inside get")
        if not filepath:
            return "File path not given"
        else:
            if os.path.isfile(filepath):
                with open(filepath) as f:
                    return f.read()
            else:
                return "Not found"
     
    def PUT(self, filepath):
        """Replace the file by the data in the request."""
        
        #p = os.path.isfile(filepath)
        
        with open(filepath, 'w') as f:
            print(web.data())
            f.write(web.data().decode())

        return ''

    def DELETE(self, filepath):
        os.unlink(filepath)
        return 'OK'

config = {
        'lockserver': None,
        'nameserver': None,
        'directories': [],
        }

logging.info('Loading config file fileserver.dfs.json.')
utils.load_config(config, 'fileserver.dfs.json')

config['directories'] = set(config['directories'])


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

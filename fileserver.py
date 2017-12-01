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



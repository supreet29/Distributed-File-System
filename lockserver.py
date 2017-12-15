import web
import shelve
import datetime
import logging
import random

urls = (
        '/filepath/(.*)', 'NameServer'
        )

class LockServer:

    def GET(self, filepath):
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        filepath = str(filepath)
        i = web.input()

        if filepath == '/':
            p = lock[filepath]
            # just a list of file=(granted, last_used)
            return '\n'.join('%s=(%s, %s)' % (filepath,
                   str(p.granted),
                   str(p.last_used),)
                   for filepath in sorted(lock))

        elif filepath not in lock and 'lock_id' not in i:
            return 'OK'

        elif 'lock_id' in i:
            locks = lock.get(filepath, -1)
            try:
                if int(i['lock_id']) == locks.lock_id:
                    t = datetime.datetime.now()

                    logging.info('Update lock on %s from %s to %s.',
                                 filepath, lock[filepath].last_used, t)

                    l = lock[filepath]
                    l = lock(l.lock_id, l.granted, t)
                    lock[filepath] = l
                    return 'OK'
                else:
                    raise Exception("Bad lock_id")

            except (Exception, ValueError) as e:
                # logging.exception(e)
                if filepath in lock:
                    logging.info('Revoking lock on %s.', filepath)
                    del lock[filepath]
                raise web.conflict()

        raise web.conflict()

    def POST(self, filepath):
         web.header('Content-Type', 'text/plain; charset=UTF-8')
         filepath = str(filepath)

         if filepath == '/':
            granted_locks = {}

            for filepath in web.data().split('\n'):
                if not filepath:
                    # to allow an empty line at the end of the request data
                    continue

                try:
                    lock_id = random.randrange(0, 32768)
                    logging.info('Granting lock (%d) on %s.', lock_id, filepath)
                    t = datetime.datetime.now()
                    lock[filepath] = lock(lock_id, t, t)
                    return lock_id
                except Exception as e:
                    logging.exception(e)

                    raise web.unauthorized()

            # list of filename=lock_id
            return '\n'.join('%s=%d' % (filepath, lock_id,)\
                    for filepath, lock_id in granted_locks.items())
    
         raise web.unauthorized()

    def DELETE(self, filepath):
        web.header('Content-Type', 'text/plain; charset=UTF-8')

        filepath = str(filepath)
        i = web.input()

        # allow deletion of multiple locks
        # so it'll be easier to add transactions
        if filepath == '/':
            if 'filepaths' not in i or 'lock_ids' not in i:
                raise web.badrequest()

            for filepath, lock_id in\
                    zip(i['filepaths'].split('\n'), i['lock_ids'].split('\n')):
                if lock[filepath].lock_id == int(lock_id):
                    if filepath in lock:
                        logging.info('Revoking lock on %s.', filepath)
                        del lock[filepath]

            # return OK even if some lock_ids were wrong
            return 'OK'

        elif filepath in lock:
            if 'lock_id' in i:
                lock_id = i['lock_id']

                if lock[filepath].lock_id == int(lock_id):
                    if filepath in lock:
                        logging.info('Revoking lock on %s.', filepath)
                        del lock[filepath]

                # see above for why always ok
                return 'OK'

            raise web.badrequest()

        else:
            return 'OK'

    

    def new_lock(filepath):
        """Create a new lock for filepath, and return its id."""

        lock_id = random.randrange(0, 32768)
        logging.info('Granting lock (%d) on %s.', lock_id, filepath)
        t = datetime.datetime.now()
        lock[filepath] = lock(lock_id, t, t)
        return lock_id


    def update_lock(filepath):
        t = datetime.datetime.now()

        logging.info('Update lock on %s from %s to %s.',
                 filepath, lock[filepath].last_used, t)

        l = lock[filepath]
        l = lock(l.lock_id, l.granted, t)
        lock[filepath] = l


    def revoke_lock(filepath):
        """Revoke the lock associated to filepath."""

        if filepath in lock:
            logging.info('Revoking lock on %s.', filepath)
            del lock[filepath]

        	
     
_config = {
            'dbfile': 'locks.db',
            'lock_lifetime': 60,
         }

lock = shelve.open(_config['dbfile'])


if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()

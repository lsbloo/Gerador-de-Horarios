from sockets.service import quickstart
quickstart()

"""
from multiprocessing import Pool
from sockets.service import ThreadService



def startService():
    os.system('python3 {}'.format(start_service))
    
if __name__=="__main__":
    start_service = 'initserver.py'
    pool = Pool(processes=1)
    th = ThreadService(pool,startService(),start_service)
    th.start()
"""


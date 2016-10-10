import multiprocessing as mp
import os
from xmltree import Fsscan
import cProfile
import re




def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()
	
def addtoqueue(queue,filepath):
	#cProfile.run('re.compile("addtoqueue|queue,message")')
	fsscan = Fsscan()
	fsscan.filesystemscan_recursive(filepath,2)
	queue.put(fsscan.tableoftables)
	
	
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('cpu count: ',os.cpu_count())
    print('active children: ',mp.active_children())

def fa(name):
    info('function fa')
    print('hello', name)

if __name__ == '__main__':

    queue = mp.Queue()
    qp = mp.Process(target = addtoqueue, args = (queue,r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization V\Assets\Gameplay\XML\Units",))
    qp2 = mp.Process(target = addtoqueue, args = (queue,r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization V\Assets\Gameplay\XML\AI",))
    qp.start()
    qp2.start()
    
    print(queue.get())
    print(queue.get())

    qp.join()
    qp2.join()
	
	
    parent_conn, child_conn = mp.Pipe()	
    p = mp.Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
	
    p = mp.Process(target=fa, args=('bob',))
    p.start()
    info('main line')
    p.join()
	
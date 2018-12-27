from threading import Thread, Event
from queue import Queue
import time
import multiprocessing

# Code to execute in an independent thread
def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


# Create and launch a thread
t = Thread(target=countdown, args=(10,))
t.start()

# Verify if a Thread is still alive

if t.is_alive():
    print('Still running')
else:
    print('Completed')

# You can also request to join with a thread, which waits for it to terminate:
t.join()

# Daemonic threads can’t be joined. However, they are destroyed automatically when the
# main thread terminates.
#t = Thread(target=countdown, args=(10,), daemon=True)
#t.start()


# Example to terminate a Thread with a class
class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus - terminate at 5', n)
            n -= 1
            time.sleep(1)

c = CountdownTask()
t = Thread(target=c.run, args=(10,))
t.start()
time.sleep(5)
c.terminate() # Signal termination
t.join() # Wait for actual termination (if needed)


# Example for a I/O operation with timeout to stop a thread
class IOTask:

    def terminate(self):
        self._running = False

    def run(self, sock):
        # sock is a socket
        sock.settimeout(5) # Set timeout period
        while self._running:
        # Perform a blocking I/O operation w/ timeout
            try:
                data = sock.recv(8192)
                break
            except socket.timeout:
                continue
        # Continued processing
        #...
        # Terminated
        return


# Exemple via inheritance from the Thread class,
# works but is restricted and introduces a extra dependency of other libs
class CountdownThread(Thread):

    def __init__(self, n):
        super().__init__()
        self.n = 0

    def run(self):
        while self.n > 0:
            print('T-minus', self.n)
            self.n -= 1
            time.sleep(5)

c = CountdownThread(5)
c.start()

# Example of a usage of the Thread in multiprocessing
c = CountdownTask(5)
p = multiprocessing.Process(target=c.run)
p.start()



##########################################################################################################

# Events, to control if a Thread is started, wait until start

# Code to execute in an independent thread
def countdown(n, started_evt):
    print('countdown starting')
    started_evt.set()
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

# Create the event object that will be used to signal startup
started_evt = Event()

# Launch the thread and pass the startup event
print('Launching countdown')
t = Thread(target=countdown, args=(10,started_evt))
t.start()

# Wait for the thread to start
started_evt.wait()
print('countdown is running')

#Writing code that involves a lot of tricky synchronization between threads is likely to
#make your head explode. A more sane approach is to thread threads as communicating
#tasks using queues or as actors.


##########################################################################################################

# Communicating Between Threads
# Queue object in lib

# A thread that produces data
def producer(out_q):
    while True:
        # Produce some data
        data = 'teste'
        out_q.put(data)

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()
        # Process the data
        print(data)

# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()

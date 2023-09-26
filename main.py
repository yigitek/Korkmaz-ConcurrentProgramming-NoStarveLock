import threading
import time
from random import randint
class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = threading.Semaphore(1)

    def lock(self, semaphore):
        with self.mutex:
            self.counter += 1
            if self.counter == 1:
                semaphore.acquire()

    def unlock(self, semaphore):
        with self.mutex:
            self.counter -= 1
            if self.counter == 0:
                semaphore.release()

readSwitch = Lightswitch ()
roomEmpty = threading.Semaphore(1)
turnstile = threading.Semaphore(1)

def writer():
    turnstile.acquire()
    roomEmpty.acquire()
    print(f"{threading.current_thread().name} is in critical section")
    time.sleep(randint(5,10))
    turnstile.release()
    roomEmpty.release()
    print(f"{threading.current_thread().name} has left the critical section")
def reader():
    turnstile.acquire()
    turnstile.release()
    readSwitch.lock(roomEmpty)
    print(f"{threading.current_thread().name} is in critical section")
    time.sleep(randint(1, 7))
    readSwitch.unlock(roomEmpty)
    print(f"{threading.current_thread().name} has left the critical section")
readers = []
writers = []
writers2 = []
readers2 = []
readers3 = []
for i in range(2):
    writers.append(threading.Thread(target=writer, name=f"writer{i+1}"))

for i in range(2):
    writers2.append(threading.Thread(target=writer, name=f"writer{i+3}"))

for i in range(2):
    readers.append(threading.Thread(target=reader, name=f"reader{i+1}"))

for i in range(3):
    readers2.append(threading.Thread(target=reader, name=f"reader{i+3}"))

for i in range(3):
    readers3.append(threading.Thread(target=reader, name=f"reader{i+6}"))

for thread in readers + writers + readers2 + writers2 + readers3:
    thread.start()

for thread in readers + writers + readers2 + writers2 + readers3:
    thread.join()
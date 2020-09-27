from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

def local_time(counter):
    return ' (Vector={}, LOCAL_TIME={})'.format(counter,datetime.now())

# simulates and internal event
def event(pid, counter):
    counter[pid] += 1
    print('Internal Event in {} !'.format(pid) + local_time(counter))
    return counter

# simulates the sending event
def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Sending Message from ' + str(pid) + local_time(counter))
    return counter

# simulates the receiving event
def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    counter[pid] += 1
    print('Receiving Message at ' + str(pid)  + local_time(counter))
    return counter

def calc_recv_timestamp(recv_time_stamp, counter):
    for id  in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter

# process a as depicted in task
def process_one(pipe12):
    pid = 0
    counter = [0,0,0]
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    print(f'Process 0: {counter}')

# process b as depicted in task
def process_two(pipe21, pipe23):
    pid = 1
    counter = [0,0,0]
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)
    print(f'Process 1: {counter}')

# process c as depicted in task
def process_three(pipe32):
    pid = 2
    counter = [0,0,0]
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)
    print(f'Process 2: {counter}')

# Runner
if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one, args=(oneandtwo,))
    process2 = Process(target=process_two, args=(twoandone, twoandthree))
    process3 = Process(target=process_three, args=(threeandtwo,))

    # Run
    process1.start()
    process2.start()
    process3.start()

    # Make sure processes finish before exiting
    process1.join()
    process2.join()
    process3.join()

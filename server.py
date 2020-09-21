import socket
import os
import tqdm

total_read = 0
SERVER_HOST = socket.gethostbyaddr(socket.gethostbyname(socket.gethostname()))[0]
SERVER_PORT = 5000
BUFFER_SIZE = 4096
SEPARATOR = "<STOP>"

# create, bind and listen
server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print("Listening at {}:{}".format(SERVER_HOST, SERVER_PORT))

# accept client
client_socket, address = server_socket.accept() 
print("client {} is connected.".format(address))

# receive data
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)
filesize = int(filesize)

# duplicates
base, extension = os.path.splitext(filename)

# files in directory
contents = os.listdir()

copies = base + "_copy"
copy_number = []

# check if any copies exist
for c in contents:
    if copies in c:
        i = int(''.join(x for x in c if x.isdigit()))
        copy_number.append(i)

# file name exists
if os.path.isfile(filename):
    # no copy, create first copy and rename
    if len(copy_number) == 0:
        base_copy = base + "_copy1"
        os.rename(filename, base_copy + extension)
    else:
        # copy, increase copy number by 1 and rename
        x = max(copy_number) + 1
        base_copy = copies + f'{x}'
        os.rename(filename, base_copy + extension)
else:
    filename = filename

# Recieve file and update progress bar
progress = tqdm.tqdm(range(filesize), "Receiving {}".format(filename), unit="B", unit_scale=True, unit_divisor=1024, leave=True)
with open(filename, "wb") as f:
    for _ in progress:
        while total_read != filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)

            if total_read == filesize:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
            total_read += len(bytes_read)

f.close()
client_socket.close()
server_socket.close()
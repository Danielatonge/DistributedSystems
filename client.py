import socket
import argparse
import os
import tqdm

SEPARATOR = "<STOP>"
BUFFER_SIZE = 4096

def send(filename, host, port):
    total_read = 0
    file_size = os.path.getsize(filename)

    # create client socket and connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to {}:{} ".format(host,port))
    client_socket.connect((host, int(port)))
    print("Client connected to the server")

    client_socket.send(f"{filename}{SEPARATOR}{file_size}".encode())

    progress_bar = tqdm.tqdm(range(file_size), "Sending {}".format(filename), unit="B", unit_scale=True, unit_divisor=1024, leave=True)        
    
    # read file and update progress bar
    with open(filename, "rb") as f:
        for _ in progress_bar:
            while total_read != file_size:  # while file_size not done transmitting, transmit
                bytes_read = f.read(BUFFER_SIZE)
                if total_read == file_size:
                    break
                client_socket.sendall(bytes_read)
                progress_bar.update(len(bytes_read))
                total_read += len(bytes_read)
    f.close()
    client_socket.close()

if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("host_ip")
    parser.add_argument("portnumber")
    args = parser.parse_args()
    filename = args.filename
    host = args.host_ip
    port = args.portnumber
    send(filename, host, port)
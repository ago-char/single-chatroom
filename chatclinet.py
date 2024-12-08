import socket
import threading
import signal
import sys

HOST="127.0.0.1"
PORT=55665

def sent_to_server_from_stdin(connected_socket: socket.socket):
        while True:
            data_to_send=input("client data: ")
            if data_to_send:
                connected_socket.sendall(data_to_send.encode('utf-8'))

def exit_if_connection_dies(conn: socket.socket):
    while True:
        if conn.fileno()==-1:
            exit()

def signal_handler(sig, frame):
    # print('CTRL+C caught. Exiting...')
    # sys.exit(0)  # exit the program
    exit()

# Register the signal handler for SIGINT (CTRL+C)
signal.signal(signal.SIGINT, signal_handler)

# try:
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"Lesgo")
    t1=threading.Thread(target=sent_to_server_from_stdin, args=(s,))
    t2=threading.Thread(target=exit_if_connection_dies,args=(s,))
    t1.daemon=True
    t2.daemon=True
    t1.start()
    t2.start()
    while True:
        data=s.recv(1024)
        if data:
            print(data.decode('utf-8'))
        else:
            break
        if not t1.is_alive or s.fileno()==-1:
            exit()
# except KeyboardInterrupt:
#     # print("CTRL+C Exiting Main Thread....")
#     exit()

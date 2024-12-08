import socket
import threading
import signal
import sys


HOST="127.0.0.1"
PORT=55665

def sent_to_clinet_from_stdin(connected_socket: socket.socket):
        while True:
            data_to_send=input("dede baba: ")
            if data_to_send:
                connected_socket.sendall(data_to_send.encode('utf-8'))

def signal_handler(sig, frame):
    # print('CTRL+C caught. Exiting...')
    # sys.exit(0)  # exit the program1
    exit()

def exit_if_connection_dies(conn: socket.socket):
    while True:
        if conn.fileno()==-1:
            exit()

# Register the signal handler for SIGINT (CTRL+C)
signal.signal(signal.SIGINT, signal_handler)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn,addr=s.accept()
    print(f"Connected {addr}")
    with conn:
        # try:
        t1=threading.Thread(target=sent_to_clinet_from_stdin,args=(conn,)) 
        t2=threading.Thread(target=exit_if_connection_dies,args=(conn,)) 
        t1.daemon=True    
        t2.daemon=True    
        t1.start()
        t2.start()
        while True:
                data=conn.recv(1024)
                if data:
                    print(data.decode('utf-8'))
                else:
                    break
                if not t1.is_alive or s.fileno()==-1:
                    exit()
        # except KeyboardInterrupt:
        #     # print("CTRL+C Exiting Main Thread....")
        #     raise Exception("ExitingServer...")
        #     exit()
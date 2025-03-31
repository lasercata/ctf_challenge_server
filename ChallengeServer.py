#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2025.03.31
# Version           : v1.0.0
#
#--------------------------------


##-Imports
import socket

from sys import argv
from sys import exit as sysexit
from datetime import datetime as dt

import threading

from collections.abc import Callable

##-Init
HOST = '0.0.0.0'

##-Utils
def get_pwd_from_user(conn: socket.SocketType, msg: str, pwd: str) -> bool:
    '''
    Asks the client for the password.

    - conn : the connection details ;
    - msg  : the message to show to the client ;
    - pwd  : the password.

    Returns True iff the client gives `pwd`.
    '''

    conn.sendall(msg.encode('utf-8'))
    password_input = conn.recv(1024).decode('utf-8').strip() # Décodage et suppression des espaces

    return password_input == pwd


##-Main
class ChallengeServer:
    '''Defines a simple server that can be accessed using netcat'''

    def __init__(self, handle_client: Callable[[socket.SocketType, tuple[str, str]], None], timeout: int | None = None):
        '''
        Initiate the class.

        - handle_client : the function that handles the client. Should be of prototype :
            handle_client(conn: socket, addr: tuple[str, str])

        - timeout       : the maximal duration for the user to answer. If None, it is not set.
        '''
    
        self.handle_client = handle_client
        self.timeout = timeout

    def _handle_client_wrapper(self, conn: socket.SocketType, addr: tuple[str, str]):
        '''
        Wrapper around self.handle_client with a try block to catch errors.

        - conn : the connection details ;
        - addr : the address of the client (ip, port).
        '''
    
        try:
            self.handle_client(conn, addr)

        except socket.timeout:
            conn.sendall('\nConnection timed out. Please be faster.\n'.encode('utf-8'))
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

        except ConnectionResetError:
            conn.close()

        except BrokenPipeError:
            conn.close()

        print(f'[{dt.now()}] Disconnection from {addr[0]}:{addr[1]}')

    def run(self, port: int, host: str):
        '''
        Launches the server and listen for connections.
        Put every client in a thread.

        - port : the port on which listen ;
        - host : the address on which listen.
        '''
    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((host, port))
            server.listen()

            print(f"[*] Server listening on {host}:{port}...")

            try:
                while True:
                    conn, addr = server.accept()
                    if self.timeout != None:
                        conn.settimeout(self.timeout)

                    print(f'[{dt.now()}] Connexion received from {addr[0]}:{addr[1]}')

                    client_thread = threading.Thread(target=self._handle_client_wrapper, args=(conn, addr))
                    client_thread.start()

            except KeyboardInterrupt:
                print('\n[*] Exiting ...')
                return


##-Parser
def print_help():
    '''Prints the help message.'''

    print(f'Usage: {argv[0]} port')

def parse(handle_client: Callable[[socket.SocketType, tuple[str, str]], None], timeout: int | None = None):
    '''
    Defines the argument parser.

    - handle_client : the function to run in the client
    '''

    if len(argv) < 2:
        print_help()
        sysexit()

    try:
        port = int(argv[1])

    except ValueError:
        print_help()
        print('Error: the port should be an int !')
        sysexit()

    C = ChallengeServer(handle_client, timeout=timeout)
    C.run(port=port, host=HOST)


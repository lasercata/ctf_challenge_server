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
from ChallengeServer import parse, get_pwd_from_user

##-Init
with open('flag.txt', 'r') as f:
    flag = f.read().strip('\n')

##-Utils
def handle_client(conn, addr: tuple[str, str]):
    '''
    Example of a handle client function.

    - conn : the connection details ;
    - addr : the address, of the form (ip, port).
    '''

    conn.sendall('Welcome !\nEnter "password" to get the flag.\n'.encode("utf-8"))
    while not get_pwd_from_user(conn, 'Enter the password :\n>', 'password'):
        pass

    conn.sendall(f'The flag is "{flag}"\n'.encode("utf-8"))
    conn.close()


##-Running
if __name__ == '__main__':
    parse(handle_client, timeout=None)

# Challenge server

This script defines a simple python server that can be accessed using netcat (client side).
It can be useful to create CTF challenges.


## Usage

Edit the `handle_client` function in the `chall.py` file to implement the desired challenge.

Then run (server side) :
```
./chall.py [port]
```

The clients can then connect with
```
nc [host ip] [port]
```

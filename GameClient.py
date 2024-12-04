##### Alex Tregub
##### 2024-12-04
##### gameClient.py
##### ===========
##### Demonstrates socket-wise connections using base code by Dr. Giovanni Villalobos-Herrera
#####     for Computer Communication networks course Fall 2024.
##### - IP and PORT of server hardcoded in this file
##### - WASD controls, R to restart when needed, Q to quit
##### VERSION=v1.0.2
##### ===========
import keyboard
import socket
import time

SERVER_IP = "10.22.60.31"
PORT = 5000


def client_program():
    print("trying to connect to server")
    host = SERVER_IP
    port = PORT  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("waiting for keyboard input")
    while True:
        if keyboard.is_pressed('a'):
            client_socket.send('a'.encode())  # send message
            time.sleep(0.1)
        if keyboard.is_pressed('d'):
            client_socket.send('d'.encode())  # send message
            time.sleep(0.1)
        if keyboard.is_pressed('s'):
            client_socket.send('s'.encode())  # send message
            time.sleep(0.1)
        if keyboard.is_pressed('w'):
            client_socket.send('w'.encode())  # send message
            time.sleep(0.1)

        # Reset command
        if keyboard.is_pressed('r'):
            client_socket.send('r'.encode())
            time.sleep(0.1)

        if keyboard.is_pressed('q'):
            # client_socket.send('q'.encode())
            client_socket.send('r'.encode()) # Sends reset signal to first reset game state and then quit
            time.sleep(0.2)
            break
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
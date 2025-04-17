import python.scapytest.Sniffingtest.code.keygen as keygen
import socket
import threading
import python.scapytest.Sniffingtest.code.fun as fun

host = "127.0.0.1"
port = 12345
count = 0


def main():
    # Ask the user if they want to use encryption
    # TODO need to set up way for client3 and 4 to generate keys then both confirm encryption.
    # TODO Messaging functions are working

    here_in_the_deep_blue_sea = fun.unenc()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to server...")
    s.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    here_in_the_deep_blue_sea.unencrypted_messaging(s)


main()

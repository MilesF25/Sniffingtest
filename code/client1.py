import python.scapytest.Sniffingtest.code.keygen as keygen
import socket
import threading
import python.scapytest.Sniffingtest.code.fun as fun

# need to load keys from file, set up connection to server, then have enc and decryption methods

host = "127.0.0.1"
port = 12345


def receive_messages(socket):
    """Thread function to continuously receive messages from the server."""
    try:
        while True:
            message = socket.recv(1024)
            if not message:
                print("Server disconnected.")
                break
            print(f"\nReceived from Client 1: {message.decode()}")
    except ConnectionResetError:
        print("Connection lost.")
    except Exception as e:
        print(f"Error receiving message: {e}")


def send_messages(socket):
    """Main thread function to send messages to the server."""
    try:
        while True:
            your_message = input("Enter message:  ")
            if your_message == "Bye Bye":
                print("Client disconnected.")
                socket.close()
                break
            socket.sendall(your_message.encode())

    except KeyboardInterrupt:
        print("Chat ended by user.")
        socket.close()


# threading lets me do multple things at once, so I can send and receive messages at the same time
def unencrypted_messaging(socket):
    # Start a thread for receiving messages
    receive_thread = threading.Thread(
        target=receive_messages, args=(socket,), daemon=True
    )
    receive_thread.start()

    # Main thread handles sending messages
    send_messages(socket)


def main():
    here_in_the_deep_blue_sea = fun.unenc()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to server...")
        s.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        here_in_the_deep_blue_sea.unencrypted_messaging(s)


main()

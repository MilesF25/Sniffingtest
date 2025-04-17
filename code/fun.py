import socket
import threading
import python.scapytest.Sniffingtest.code.keygen as keygen


def wait_for_encryption_agreement(clients):
    responses = []
    for conn in clients:
        conn.sendall(b"Do you want to use encryption? (yes/no): ")
        response = conn.recv(1024).decode().strip().lower()
        responses.append(response)

    # Wait until both clients respond with "yes"
    if responses == ["yes", "yes"]:
        print("Both clients agreed to use encryption.")
        for conn in clients:
            conn.sendall(b"Encryption enabled.")
        return True
    else:
        print("One or both clients declined encryption.")
        for conn in clients:
            conn.sendall(b"Encryption disabled.")
        return False


class unenc:
    def __init__(self):
        pass

    def receive_messages(self, socket):
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

    def send_messages(self, socket):
        """Main thread function to send messages to the server."""
        try:
            while True:
                your_message = input("Enter message: ")
                if your_message == "Bye Bye":
                    print("Client disconnected.")
                    socket.close()
                    break
                socket.sendall(your_message.encode())

        except KeyboardInterrupt:
            print("Chat ended by user.")
            socket.close()

    # threading lets me do multple things at once, so I can send and receive messages at the same time
    def unencrypted_messaging(self, socket):
        # Start a thread for receiving messages
        cl = unenc()
        # target runs the function
        # daemon makes sure the program exits when the main thread exits
        # args passes the socket to the function
        receive_thread = threading.Thread(
            target=cl.receive_messages, args=(socket,), daemon=True
        )
        receive_thread.start()

        # Main thread handles sending messages
        cl.send_messages(socket)


class enc:
    def receive_enc_messages(self, socket, privatekey):
        """Thread function to continuously receive encrypted messages from the server."""

        try:
            while True:
                message = socket.recv(1024)
                dec_msg = keygen.decrypt(message, privatekey)

                if not message:
                    print("Server disconnected.")
                    break
                print(f"\nReceived from Client 1: {message.decode()}")
        except ConnectionResetError:
            print("Connection lost.")
        except Exception as e:
            print(f"Error receiving message: {e}")

    def send_enc_messages(self, socket, publickey):
        """Main thread function to send messages to the server."""
        try:
            while True:
                your_message = input("Enter message:  ")
                if your_message == "Bye Bye":
                    print("Client disconnected.")
                    socket.close()
                    break
                enc_msg = keygen.encrypt(your_message, publickey)
                socket.sendall(enc_msg.encode())

        except KeyboardInterrupt:
            print("Chat ended by user.")
            socket.close()

    def encrypted_messaging(self, socket):
        # Start a thread for receiving messages
        # calls the enc class functions
        cl = enc()
        receive_thread = threading.Thread(
            target=cl.receive_enc_messages(), args=(socket,), daemon=True
        )
        receive_thread.start()

        # Main thread handles sending messages
        cl.send_messages(socket)

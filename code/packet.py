import socket
import threading
import time

host = "127.0.0.1"
port = 12345
connections = []


def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        while True:
            # Receive data from the client (up to 1024 bytes)
            data = conn.recv(1024)

            # If client sends nothing (disconnects), exit the loop
            if not data:
                break

            # Loop through all connected clients
            for client in connections:
                # Send the message to all clients *except* the one who sent it
                if client != conn:
                    time.sleep(
                        0.4
                    )  # Optional: add a small delay to avoid overwhelming the clients
                    client.sendall(data)
    except ConnectionError:
        # If an error happens (e.g., client disconnects unexpectedly)
        print(f"[-] Lost connection to {addr}")
    finally:
        # Clean up: close connection and remove from list
        conn.close()
        connections.remove(conn)


def main():
    # Create a TCP socket using IPv4 addressing
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the host and port so it can listen for incoming connections
        s.bind((host, port))

        # Start listening for incoming connections (2 max for now)
        s.listen(2)
        print(f"Listening on {host}:{port}...")

        # Wait until two clients have connected
        while len(connections) < 2:
            # Accept an incoming connection
            conn, addr = s.accept()

            # Add the new client connection to the global list
            connections.append(conn)

            # Create a new thread to handle this client's messaging
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


# listening socket
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     # binds the socket to the host and port
#     s.bind((host, port))
#     s.listen()
#     # waits for a connection
#     print(f"Listening on {host}:{port}...")
#     # accepts a connection from a client
#     conn, addr = s.accept()

#     # Data exchange loop

#     # Will loop until client closes the connection
#     with conn:
#         if connections == 1:
#             s.sendall(b"Waiting for someone else to connect")
#         else:
#             try:
#                 print(f"Connected by {addr}")

#                 data = conn.recv(1024)  # will be received in 8bit units
#                 # will loop until the client sends a empty packet
#                 # if not data:
#                 #     break
#                 conn.sendall(data)  # will be sent in 8bit units
#             except KeyboardInterrupt:
#                 print("Program interrupted by user")

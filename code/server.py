import socket
import threading

HOST = "127.0.0.1"
PORT = 12345


# def handle_client(conn, client_id):
#     global clients
#     other_client = clients[1] if client_id == 0 else clients[0]

#     try:
#         while True:
#             data = conn.recv(4096)
#             if not data:
#                 break
#             print(
#                 f"Client {client_id + 1} says: {data[:50]}..."
#             )  # Print beginning of message
#             other_client.sendall(data)
#     except ConnectionResetError:
#         print(f"Client {client_id + 1} disconnected.")
#     # finally:
#     #     conn.close()


def handle_client(conn, client_id, clients):
    try:
        while True:
            # Wait until both clients are connected
            if len(clients) < 2:
                print(
                    f"Client {client_id + 1} is waiting for the other client to connect..."
                )
                continue  # Skip this iteration until both clients are connected

            # Determine the other client
            other_client = clients[1] if client_id == 0 else clients[0]

            # Receive data from the current client
            data = conn.recv(4096)
            if not data:  # If no data is received, the client has disconnected
                break

            # Print the message for debugging/logging purposes
            print(f"Client {client_id + 1} says: {data.decode()}")

            # Forward the message to the other client
            other_client.sendall(data)
    except ConnectionResetError:
        print(f"Client {client_id + 1} disconnected.")


def main():
    clients = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(2)
            print("Server is running and waiting for two clients to connect...")

            # Wait for two clients to connect
            while len(clients) < 2:
                conn, addr = s.accept()
                print(f"Client {len(clients) + 1} connected from {addr}")
                clients.append(conn)

            # Start threads for both clients after both have connected
            for i in range(2):
                thread = threading.Thread(
                    target=handle_client, args=(clients[i], i, clients)
                )
                thread.start()
                print(f"Thread started for Client {i + 1}")

            print("Both clients are connected. Communication can now begin.")
    except KeyboardInterrupt:
        print("Server interrupted. Shutting down...")


main()

import socket
import threading
import os

# --- Configuration ---
# Railway assigns a port dynamically; your code must read it.
# Internal Port on Railway should be set to 5000 via a PORT environment variable
PORT = int(os.environ.get("PORT", 5000))
SERVER_HOST = "0.0.0.0"

# Sockets to store the active connections.
client_conn = None
listener_conn = None
# ---------------------

def handle_connection(conn, addr, name):
    global client_conn, listener_conn
    print(f"Connection established with {name} from {addr}")
    
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                print(f"{name} disconnected.")
                break

            # Relay the message to the OTHER party
            if name == "Client" and listener_conn:
                print(f"Relaying from Client to Listener: {data.decode()}")
                listener_conn.sendall(data)
            elif name == "Listener" and client_conn:
                print(f"Relaying from Listener to Client: {data.decode()}")
                client_conn.sendall(data)

        except Exception as e:
            print(f"Error handling {name} connection: {e}")
            break

    # Clean up the connection when the loop breaks
    if name == "Client":
        client_conn = None
    elif name == "Listener":
        listener_conn = None
    conn.close()


def start_server():
    global client_conn, listener_conn
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, PORT))
    server_socket.listen(5)
    print(f"Middleman server listening on {SERVER_HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        
        if client_conn is None:
            client_conn = conn
            thread = threading.Thread(target=handle_connection, args=(conn, addr, "Client"))
            thread.start()
        elif listener_conn is None:
            listener_conn = conn
            thread = threading.Thread(target=handle_connection, args=(conn, addr, "Listener"))
            thread.start()
        else:
            conn.sendall("Server full, try later.".encode('utf-8'))
            conn.close()

if __name__ == "__main__":
    start_server()

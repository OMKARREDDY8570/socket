import socket
import threading

clients = []

def handle(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            for c in clients:
                if c != client:
                    c.send(data)
        except:
            break
    clients.remove(client)
    client.close()

s = socket.socket()
s.bind(("0.0.0.0", 5000))
s.listen()

print("Relay server running...")

while True:
    client, addr = s.accept()
    print("Connected:", addr)
    clients.append(client)
    threading.Thread(target=handle, args=(client,), daemon=True).start()

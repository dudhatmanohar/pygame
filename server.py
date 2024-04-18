import socket
import pickle
import threading

# Constants
HOST = '0.0.0.0'
PORT = 5555

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# Global variables
clients = []
player_positions = {}

# Function to handle client connections
def handle_client(conn, addr):
    print(f"Connected to {addr}")

    # Add client to the list
    clients.append(conn)

    # Main loop to handle client input
    while True:
        try:
            # Receive player input
            data = conn.recv(1024)
            if not data:
                print(f"Disconnected from {addr}")
                clients.remove(conn)
                del player_positions[addr]
                break

            # Process player input and update game state
            player_positions[addr] = pickle.loads(data)

            # Broadcast updated game state to all clients
            broadcast_game_state()

        except Exception as e:
            print(f"Error: {e}")
            break

    # Close connection
    conn.close()

# Function to broadcast game state to all connected clients
def broadcast_game_state():
    global player_positions
    for client in clients:
        try:
            client.sendall(pickle.dumps(player_positions))
        except:
            pass  # Skip if there's an error

# Function to start the server
def start_server():
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

# Start the server
start_server()

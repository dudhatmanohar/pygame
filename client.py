import pygame
import socket
import pickle

# Constants
SERVER = '0.0.0.0'
PORT = 5555

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Set up the display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game")

# Colors
WHITE = (255, 255, 255)

# Initialize player position
player_position = [0, 0]

# Function to send player position to the server
def send_position(position):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER, PORT))
        client_socket.sendall(pickle.dumps(position))
        client_socket.close()
    except Exception as e:
        print(f"Error sending position: {e}")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_position[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_position[0] += 5
    if keys[pygame.K_UP]:
        player_position[1] -= 5
    if keys[pygame.K_DOWN]:
        player_position[1] += 5

    # Send player position to the server
    send_position(player_position)

    # Clear the screen
    win.fill(WHITE)

    # Draw player
    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(player_position[0], player_position[1], 50, 50))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

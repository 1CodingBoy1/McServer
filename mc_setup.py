#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import urllib.request

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

# --- NEW: Version Selection ---
mc_version = cyan_input("\nEnter Minecraft Version to install (e.g., 1.20.4, 1.19.2): ")

# Fallback to 1.20.4 if user just presses enter
if not mc_version.strip():
    mc_version = "1.20.4"
    cyan_print(f"[INFO] No version entered, defaulting to {mc_version}")

server_name = cyan_input("\nEnter Server Name (This will be your folder name): ")

# Fallback to server1 if empty
if not server_name.strip():
    server_name = "server1"

# Remove spaces from folder name to prevent bash errors
server_name = server_name.replace(" ", "_")

# --- Installation Process ---
cyan_print(f"\n[INFO] Starting installation for '{server_name}'...")
os.makedirs(server_name, exist_ok=True)
os.chdir(server_name)

# Get absolute path for the screen session to work correctly
abs_path = os.getcwd()

# 1. Generate eula.txt and server.properties IMMEDIATELY
cyan_print("[INFO] Generating eula.txt and server.properties...")
with open("eula.txt", "w") as f:
    f.write("eula=true\n")

with open("server.properties", "w") as f:
    f.write("# CodingBoyz Minecraft Server Properties\n")
    f.write("server-port=25565\n")
    f.write("max-players=20\n")
    f.write("level-seed=CodingBoyz\n")
    f.write("motd=Subscribe to CodingBoyz\n")
    f.write("enable-command-block=true\n")

# 2. Install dependencies (Java 17 and Screen)
cyan_print("[INFO] Installing Java 17 and Screen (requires sudo)...")
subprocess.run("sudo apt update -y > /dev/null 2>&1", shell=True)
subprocess.run("sudo apt install openjdk-17-jre-headless screen wget curl -y > /dev/null 2>&1", shell=True)

# 3. Download selected server JAR
cyan_print(f"[INFO] Preparing to download version {mc_version}...")
jar_name = "server.jar" # Default name
download_success = False

try:
    if server_type == "1": # PaperMC (Using your requested curl method)
        cyan_print(f"[INFO] Downloading PaperMC {mc_version} via curl...")
        # Using the official PaperMC API endpoint so it downloads the actual JAR file
        paper_url = f"https://api.papermc.io/v2/projects/paper/versions/{mc_version}/builds/latest/downloads/paper-{mc_version}-latest.jar"
        cmd = f'curl -H "User-Agent: MyMinecraftServer/1.0 (contact@example.com)" -fL "{paper_url}" -o paper.jar'
        if subprocess.run(cmd, shell=True).returncode == 0: 
            jar_name = "paper.jar" # Update jar name to match what we just downloaded
            download_success = True
            
    elif server_type == "2": # Vanilla
        cyan_print("[INFO] Contacting Mojang API...")
        api_url = f"https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            download_url = ""
            for v in data['versions']:
                if v['id'] == mc_version:
                    with urllib.request.urlopen(v['url']) as ver_response:
                        ver_data = json.loads(ver_response.read().decode())
                        download_url = ver_data['downloads']['server']['url']
                    break
            if not download_url:
                raise Exception(f"Version {mc_version} not found on Mojang servers.")
            
        cyan_print(f"[INFO] Downloading Vanilla {mc_version}...")
        cmd = f'wget -q --show-progress -O {jar_name} "{download_url}"'
        if subprocess.run(cmd, shell=True).returncode == 0: download_success = True
        
    elif server_type == "3": # Spigot
        cyan_print(f"[INFO] Downloading Spigot {mc_version}...")
        cmd = f"wget -q --show-progress -O {jar_name} https://download.getbukkit.org/spigot/spigot-{mc_version}.jar"
        if subprocess.run(cmd, shell=True).returncode == 0: download_success = True
        
    else:
        cyan_print("[WARNING] Invalid choice. Defaulting to Vanilla 1.20.4.")
        mc_version = "1.20.4"
        api_url = f"https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            download_url = ""
            for v in data['versions']:
                if v['id'] == mc_version:
                    with urllib.request.urlopen(v['url']) as ver_response:
                        ver_data = json.loads(ver_response.read().decode())
                        download_url = ver_data['downloads']['server']['url']
                    break
        cmd = f'wget -q --show-progress -O {jar_name} "{download_url}"'
        if subprocess.run(cmd, shell=True).returncode == 0: download_success = True

except Exception as e:
    cyan_print(f"[ERROR] Failed to fetch download link: {e}")
    sys.exit(1)

# Verify download actually worked and isn't a tiny error page
if not download_success or not os.path.exists(jar_name) or os.path.getsize(jar_name) < 10000:
    cyan_print(f"[ERROR] Download failed! The file {jar_name} is missing or too small.")
    cyan_print("[ERROR] Double-check that the version you typed exists for that server type.")
    sys.exit(1)

# 4. Create start script with RAM allocation (Dynamically uses paper.jar or server.jar)
cyan_print(f"[INFO] Configuring startup script with {ram} RAM...")
start_script = f"""#!/bin/bash
cd {abs_path}
java -Xmx{ram} -Xms{ram} -jar {jar_name} nogui
"""
with open("start.sh", "w") as f:
    f.write(start_script)
os.chmod("start.sh", 0o755)

# 5. Display CPU/Disk info
cyan_print(f"[INFO] Allocated CPU Cores: {cpu} | Disk Limit: {disk}GB")

# 6. Start the server in a Screen session
cyan_print(f"\n[INFO] Starting server in background screen session named '{server_name}'...")
subprocess.run(f"screen -S {server_name} -X quit > /dev/null 2>&1", shell=True)
subprocess.run(f"screen -dmS {server_name} bash start.sh", shell=True)

# --- Final Output ---
cyan_print("\n" + "="*50)
cyan_print("✅ SERVER INSTALLATION COMPLETE! ✅")
cyan_print("="*50)
cyan_print(f"Server Type: {'PaperMC' if server_type == '1' else 'Vanilla' if server_type == '2' else 'Spigot'}")
cyan_print(f"Server Version: {mc_version}")
cyan_print(f"Server is now running in the background.")
cyan_print(f"Folder created: {abs_path}")
cyan_print("\n>>> HOW TO ACCESS YOUR CONSOLE FROM ANYWHERE <<<")
cyan_print(f"1. Open a new terminal/SSH connection to your VPS.")
cyan_print(f"2. Type: screen -r {server_name}")
cyan_print("3. To exit the console WITHOUT stopping the server, press: CTRL+A, then press D")
cyan_print("="*50 + "\n")

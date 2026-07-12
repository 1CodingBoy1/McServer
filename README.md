# CodingBoyz Minecraft Server Setup

A quick, interactive Python script to automatically set up a Minecraft Server (Paper, Vanilla, or Spigot) on any Linux VPS.

## Features
- 🎨 Clean, interactive Cyan UI
- ⚙️ Automatic Java 17 & Screen installation
- 📦 Supports PaperMC, Vanilla, and Spigot
- 🖥️ Runs in a `screen` session so you can close your terminal and access the console later from anywhere.

## How to Use (Via SSH/Terminal)

1. Clone this repository to your VPS:
   ```bash
   git clone https://github.com/1CodingBoy1/McServer.git
   ```

2. Navigate into the cloned folder:
   ```bash
   cd McServer
   ```

3. Run the script:
   ```bash
   python3 mc_setup.py
   ```

4. Follow the on-screen prompts!

## How to Use (Via Jupyter Notebook)
If you prefer Jupyter Notebook, you can still use this exact script:
1. Upload `mc_setup.py` to your Jupyter directory.
2. Open a new Jupyter Notebook cell.
3. Run this command in the cell:
   ```python
   %run mc_setup.py
   ```

## Accessing Your Server Console
Once installed, your server runs in the background. To access it:
- SSH into your VPS and type: `screen -r <your_server_name>`
- To detach without stopping the server: Press `CTRL + A`, then press `D`.
```

---

### Why this is better for GitHub:
1. **The `cd` fix:** In the previous version, `screen` might occasionally fail to find the `.jar` file because it doesn't inherit Python's `os.chdir()`. I added `abs_path = os.getcwd()` and hardcoded the `cd` into the generated `start.sh` file. Now it is bulletproof.
2. **Error Handling:** Added `returncode == 0` checking for `wget`. If the user has no internet, or Minecraft releases a new version breaking the link, the script safely exits with an error instead of silently failing and crashing on startup.
3. **The Shebang (`#!/usr/bin/env python3`)**: Allows users to optionally just run `./mc_setup.py` if they make it executable (`chmod +x mc_setup.py`).
4. **Jupyter Fallback Included:** As noted in the `README.md`, even as a standalone Python file, it can still be triggered inside Jupyter using the `%run` magic command. You get the best of both worlds.

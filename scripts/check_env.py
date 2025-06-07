import os
import subprocess
from datetime import datetime

LOG_DIR = "../logs"
LOG_FILE = os.path.join(LOG_DIR, "debug_log.txt")

REQUIRED_ENV_VARS = [
    "KITE_USERNAME",
    "KITE_PASSWORD",
    "API_KEY",
    "API_SECRET",
    "REDIRECT_URI",
    "DB_HOST",
    "DB_USER",
    "DB_PASSWORD"
]

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def check_command(name, cmd):
    try:
        subprocess.check_output(cmd, shell=True)
        log(f"[OK] {name} is installed and working.")
    except subprocess.CalledProcessError:
        log(f"[ERROR] {name} is NOT installed or misconfigured.")

def check_env_vars():
    env_path = "../.env"
    if not os.path.exists(env_path):
        log("[ERROR] .env file not found.")
        return
    log("[OK] .env file found.")
    with open(env_path) as f:
        content = f.read()
        for var in REQUIRED_ENV_VARS:
            if var in content:
                log(f"[OK] {var} found in .env.")
            else:
                log(f"[WARNING] {var} is missing from .env.")

def main():
    open(LOG_FILE, "w").close()  # Clear old logs
    log("Starting environment check...\n")

    check_command("Python", "py --version")
    check_command("Docker", "docker --version")
    check_command("Node.js", "node -v")
    check_command("npm", "npm -v")
    check_command("Git", "git --version")
    check_command("VS Code", "code --version")

    log("\nChecking environment variables...")
    check_env_vars()

    log("\nEnvironment check complete.\n")

if __name__ == "__main__":
    main()

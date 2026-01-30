from flask import Flask, request
import subprocess
import threading
import os

app = Flask(__name__)

# Your project directory and docker-compose file
PROJECT_PATH = "/home/Pratik/Myprojects/GithubActionLms/Learning-Management-System-Fullstack"
DOCKER_COMPOSE_FILE = "docker-compose.yml"

def run_command(cmd_list, cwd=PROJECT_PATH):
    """Run a shell command and print stdout/stderr."""
    print(f"Running command: {' '.join(cmd_list)} in {cwd}")
    result = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        raise Exception(f"Command failed with exit code {result.returncode}")

def deploy_project():
    """Deploy Django + Docker stack."""
    try:
        print("🔹 Stopping old containers...")
        run_command(["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "down"])

        print("🔹 Building and starting containers...")
        run_command(["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d", "--build"])

        print("🔹 Running Django migrations...")
        # Using run --rm instead of exec for reliability
        run_command([
            "docker", "compose", "-f", DOCKER_COMPOSE_FILE,
            "run", "--rm", "django", "python", "manage.py", "migrate"
        ])

        print("✅ Deployment complete!")

    except Exception as e:
        print("❌ Deployment failed:", e)

@app.route('/deploy', methods=['POST'])
def deploy():
    """Trigger deployment in a separate thread to avoid blocking Flask."""
    threading.Thread(target=deploy_project).start()
    return "Deployment triggered!", 200

if __name__ == "__main__":
    # Use 0.0.0.0 to be reachable by ngrok
    app.run(host="0.0.0.0", port=5000)
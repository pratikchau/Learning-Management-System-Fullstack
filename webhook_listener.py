from flask import Flask
import subprocess

app = Flask(__name__)

PROJECT_PATH = "/home/Pratik/Myprojects/GithubActionLms/Learning-Management-System-Fullstack"
DOCKER_COMPOSE_FILE = "docker-compose.yml"  # explicit file to avoid .yml-bak issues

def run_command(cmd_list, cwd=PROJECT_PATH):
    """Run a shell command and print output/errors."""
    try:
        print(f"Running command: {' '.join(cmd_list)} in {cwd}")
        subprocess.run(cmd_list, cwd=cwd, check=True)
        print("✅ Command completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        raise e

@app.route('/deploy', methods=['POST'])
def deploy():
    try:
        print("🔹 Stopping old containers...")
        run_command(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "down"])

        print("🔹 Building and starting containers...")
        run_command(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d", "--build"])

        print("🔹 Running Django migrations...")
        run_command(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "exec", "django", "python", "manage.py", "migrate"])

        print("✅ Deployment complete!")
        return "Deployment triggered!", 200
    except Exception as e:
        return f"Deployment failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
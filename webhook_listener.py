from flask import Flask
import subprocess

app = Flask(__name__)

PROJECT_PATH = "/home/Pratik/Myprojects/GithubActionLms/Learning-Management-System-Fullstack"
DOCKER_COMPOSE_FILE = "docker-compose.yml"

def run_command(cmd_list, cwd=PROJECT_PATH):
    print(f"Running command: {' '.join(cmd_list)} in {cwd}")
    subprocess.run(cmd_list, cwd=cwd, check=True)

@app.route('/deploy', methods=['POST'])
def deploy():
    try:
        print("🔹 Stopping old containers...")
        run_command(["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "down"])

        print("🔹 Building and starting containers...")
        run_command(["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d", "--build"])

        print("🔹 Running Django migrations...")
        run_command([
            "docker", "compose", "-f", DOCKER_COMPOSE_FILE,
            "exec", "django", "python", "manage.py", "migrate"
        ])

        print("✅ Deployment complete!")
        return "Deployment triggered!", 200

    except Exception as e:
        print(e)
        return f"Deployment failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
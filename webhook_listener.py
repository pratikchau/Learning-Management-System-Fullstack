from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    project_path = "/home/Pratik/Myprojects/GithubActionLms/Learning-Management-System-Fullstack"

    try:
        print("Stopping old containers...")
        subprocess.run(["docker-compose", "down"], cwd=project_path, check=True)
        
        print("Building and starting containers...")
        subprocess.run(["docker-compose", "up", "-d", "--build"], cwd=project_path, check=True)
        
        print("Running Django migrations...")
        subprocess.run(["docker-compose", "exec", "django", "python", "manage.py", "migrate"], cwd=project_path, check=True)
    except subprocess.CalledProcessError as e:
        return f"Deployment failed: {e}", 500

    return "Deployment triggered!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
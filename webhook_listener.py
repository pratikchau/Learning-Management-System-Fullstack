from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    # Stop containers
    subprocess.run(["docker-compose", "down"], cwd="/home/Pratik/Myprojects/GithubActionLms/Learning-Management-System-Fullstack")
    # Rebuild images
    subprocess.run(["docker-compose", "up", "-d", "--build"], cwd="/home/Pratik/Myprojects/GithubActionLms/Learning-Management-System-Fullstack")
    # Run Django migrations
    subprocess.run(["docker-compose", "exec", "django", "python", "manage.py", "migrate"], cwd="/home/Pratik/Myprojects/GithubActionLms/Learning-Management-System-Fullstack")
    return "Deployment triggered!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

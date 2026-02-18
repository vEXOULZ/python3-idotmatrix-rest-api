import os
import subprocess

from flask import Flask, request

app = Flask(__name__)

def is_windows():
    return os.name == "nt"

@app.route("/", methods=['POST'])
async def base():
    args = request.get_json()

    if is_windows():
        env_args = [".", "run_in_venv.ps1"]
    else:
        env_args = ["/bin/bash", "run_in_venv.sh"]

    process = subprocess.Popen(
        [*env_args, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text = True,
        bufsize=1
    )

    stdout = []

    for line in process.stdout:
        print(line.strip())
        stdout.append(line.strip())

    process.stdout.close()
    process.wait()

    return {
        "returncode": process.returncode,
        "stdout": stdout
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=10067)
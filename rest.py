# logging setup / always first import
from utils import logging_setup

import os
import subprocess
import logging

from flask import Flask, request

app = Flask(__name__)

logger = logging.getLogger(__name__)

def is_windows():
    return os.name == "nt"

token = open("token.secret", "r").read().strip()

def authenticable(route):
    async def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header != f"Bearer {token}":
            return {"error": "Unauthorized"}, 401
        return await route(*args, **kwargs)
    return wrapper

@app.route("/", methods=['POST'])
@authenticable
async def handle_request():
    args = request.get_json()
    if is_windows():
        env_args = [".", "run_in_venv.ps1"]
    else:
        env_args = ["/bin/bash", "run_in_venv.sh"]

    logger.info(f"Running request with args: {env_args} {args}")

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
    }, 200 if process.returncode == 0 else 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=10067)

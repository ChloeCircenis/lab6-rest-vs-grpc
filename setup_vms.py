
#!/usr/bin/env python3

import subprocess

PROJECT_REPO = "https://github.com/ChloeCircenis/lab6-rest-vs-grpc.git"
ZONE = "us-west1-a"
VM_NAME = "lab6-client"

STARTUP_SCRIPT = f"""#!/bin/bash
set -e
exec > /var/log/lab6-setup.log 2>&1

apt-get update
apt-get install -y git curl

# Install uv system-wide
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

# Clone the repository if needed
if [ ! -d /opt/lab6-rest-vs-grpc ]; then
    git clone {PROJECT_REPO} /opt/lab6-rest-vs-grpc
fi

cd /opt/lab6-rest-vs-grpc

# Install project dependencies
/usr/local/bin/uv sync

# Allow SSH users to access the project and virtual environment
chmod -R a+rX /opt/lab6-rest-vs-grpc

# Verify installation
/usr/local/bin/uv run python -c "import flask; import grpc; import PIL"

touch /opt/lab6-rest-vs-grpc/SETUP_COMPLETE
echo "SETUP_COMPLETE"
"""


def run(command):
    print(f"Running: {' '.join(command[:6])} ...", flush=True)
    subprocess.run(command, check=True)


def create_vm():
    run([
        "gcloud", "compute", "instances", "create", VM_NAME,
        f"--zone={ZONE}",
        "--machine-type=e2-standard-2",
        "--image-family=debian-12",
        "--image-project=debian-cloud",
        "--boot-disk-size=20GB",
        "--tags=lab6-rpc",
        f"--metadata=startup-script={STARTUP_SCRIPT}"
    ])


def main():
    print(f"Creating {VM_NAME} in {ZONE}")
    create_vm()
    print("VM created. Wait for startup setup to finish.")


if __name__ == "__main__":
    main()

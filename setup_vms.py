
#!/usr/bin/env python3

import subprocess

PROJECT_REPO = "https://github.com/ChloeCircenis/lab6-rest-vs-grpc.git"
ZONE = "us-west1-a"
VM_NAME = "lab6-client"


def run(command):
    print(f"\nRunning: {' '.join(command)}", flush=True)
    subprocess.run(command, check=True)


def create_vm():
    run([
        "gcloud", "compute", "instances", "create", VM_NAME,
        f"--zone={ZONE}",
        "--machine-type=e2-standard-2",
        "--image-family=debian-12",
        "--image-project=debian-cloud",
        "--boot-disk-size=20GB",
        "--tags=lab6-rpc"
    ])


def main():
    print("Lab 6 Google Cloud Setup")
    print(f"Repository: {PROJECT_REPO}")
    print(f"First VM: {VM_NAME} ({ZONE})")

    confirmation = input("Create first billable VM? (yes/no): ")

    if confirmation.lower() != "yes":
        print("Cancelled.")
        return

    create_vm()
    print("VM created successfully.")


if __name__ == "__main__":
    main()

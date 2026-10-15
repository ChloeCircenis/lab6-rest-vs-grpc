import subprocess

VM_NAME = "lab6-client"
ZONE = "us-west1-a"
SNAPSHOT_NAME = "lab6-base-snapshot"


def main():

    subprocess.run([
        "gcloud", "compute", "disks", "snapshot", VM_NAME,
        f"--zone={ZONE}",
        f"--snapshot-names={SNAPSHOT_NAME}"
    ], check=True)

    print("Snapshot created successfully.")


if __name__ == "__main__":
    main()
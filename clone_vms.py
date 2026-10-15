import subprocess

SNAPSHOT_NAME = "lab6-base-snapshot"

VMS = [
    ("lab6-server", "us-west1-a"),
    ("lab6-europe", "europe-west3-a")
]


def main():
    for name, zone in VMS:
        print(f"Creating {name} in {zone}...")

        subprocess.run([
            "gcloud", "compute", "instances", "create", name,
            f"--zone={zone}",
            "--machine-type=e2-standard-2",
            f"--create-disk=boot=yes,auto-delete=yes,source-snapshot={SNAPSHOT_NAME},size=20GB",
            "--tags=lab6-rpc"
        ], check=True)

    print("Both VMs created successfully.")


if __name__ == "__main__":
    main()
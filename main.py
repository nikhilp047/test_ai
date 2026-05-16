import os
import subprocess

base_path = "/mnt/c/Users/pooja/Documents/AI/Comfyui"

for root, dirs, files in os.walk(base_path):

    # print(root,dirs,files)
    # ✅ Only process folders that have files
    if not files:
        continue

    file_paths = [os.path.join(root, f) for f in files]

    result = subprocess.run(
        ["du", "-ch"] + file_paths,
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "total" in line:
            print(f"{root} -> {line}")
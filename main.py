import os
import subprocess

base_path = "/mnt/c/Users/pooja/"
full_path = f"{base_path}Documents/AI/"
full_path=f"{base_path}Documents/work_script/test_data/kng/sequences/kng_abjbdb1"

for root, dirs, files in os.walk(full_path):

    if not files:
        continue

    cmd = f'''
    find "{root}" -maxdepth 1 -type f -exec du -cb {{}} + | tail -n 1
    '''

    result = subprocess.run(
        cmd,
        shell=True,              # ✅ required
        capture_output=True,
        text=True
    )

        

    # print(f"{root} -> {result}")


    print(f"{root} -> {result.stdout.strip()}")
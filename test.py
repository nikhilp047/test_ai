import os
import subprocess
import json


def get_metadata_file(root):
    rsg_path = os.path.join(root, ".rsg", "manifest.json")
    task_path = os.path.join(root, ".task_files", "metadata.json")
    direct_path = os.path.join(root, "metadata.json")

    if os.path.exists(rsg_path):
        return [rsg_path, "rsg"]
    elif os.path.exists(task_path):
        return [task_path, "task"]
    elif os.path.exists(direct_path):
        return [direct_path, "direct"]

    return None

# 🔍 recursively find "user" key in JSON
def find_user(**kwargs):
    data = kwargs.get("data")
    param_user = kwargs.get("param_user")

    if isinstance(data, dict):
        for k, v in data.items():
            if k.lower() == param_user:
                return v
            result = find_user(data=v, param_user=param_user)
            if result:
                return result
    # elif isinstance(data, list):
    #     for item in data:
    #         result = find_user(item)
    #         if result:
    #             return result
    return None

base_path = "/mnt/c/Users/pooja/Documents/work_script/test_data/kng/sequences/kng_abjbdb1"

all_dirs = []
for root, dirs, files in os.walk(base_path):
    # print(f"Root: {root}", f"Dirs: {dirs}",end="\n")
     all_dirs.append((root, files))

# print(all_dirs)

def process_dir(root_files):
    root, files = root_files

    metadata_file = get_metadata_file(root)

    current_user = "Unknown"

    if metadata_file:
        try:
            with open(metadata_file[0], "r") as f:
                data = json.load(f)

            if metadata_file[1] == "rsg":
                param_user = "artist_name"
            else:
                param_user = "user"

            found_user = find_user(data=data, param_user=param_user)

            if found_user:
                current_user = found_user

        except:
            current_user = "Error reading JSON"

    if not files:
        return None

    cmd = f'find "{root}" -maxdepth 1 -type f -exec du -cb {{}} + | tail -n 1'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    size = result.stdout.strip()

    return root, current_user, size


from concurrent.futures import ThreadPoolExecutor, as_completed

user_map = {}

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_dir, item) for item in all_dirs]

    for f in as_completed(futures):
        result = f.result()
        if not result:
            continue

        root, user, size = result
        user_map[root] = user

        print(f"{root} -> User: {user}, Size: {size}")
import os
import subprocess
import json

base_path = "/mnt/c/Users/pooja/Documents/work_script/test_data/kng/sequences/kng_abjbdb1"


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


# 📂 get metadata path based on priority
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


user_map = {}

for root, dirs, files in os.walk(base_path):

    parent = os.path.dirname(root)
    parent_user = user_map.get(parent, "Unknown")

    current_user = parent_user

    # 🔹 Always process (for inheritance)
    metadata_file = get_metadata_file(root)

    if metadata_file:
        try:
            with open(metadata_file[0], "r") as f:
                data = json.load(f)
                if metadata_file[1] == "rsg":
                    param_user = "artist_name"
                elif metadata_file[1] == "task":
                    param_user = "user"
                elif metadata_file[1] == "direct":
                    param_user = "user"

                found_user = find_user({"data":data, "param_user": param_user})
                if found_user:
                    current_user = found_user
        except Exception:
            current_user = "Error reading JSON"

    # 🔹 Always store (CRITICAL)
    user_map[root] = current_user

    # 🔹 ONLY print if files exist
    if not files:
        continue

    # SIZE logic
    cmd = f'''
    find "{root}" -maxdepth 1 -type f -exec du -cb {{}} + | tail -n 1
    '''

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    # print(user_map , end ="\n")
    size = result.stdout.strip()

    if current_user == "Unknown":
       split_Data = root.split("/")
    #    print(split_Data[12])
       current_user = split_Data[12]

    print(f"{root} -> User: {current_user}, Size: {size}")
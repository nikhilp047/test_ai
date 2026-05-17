import os
import subprocess
import json
import threading

base_path = "/mnt/c/Users/pooja/Documents/work_script/test_data/kng/sequences/kng_abjbdb1"
results = []


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


def get_all_data(base_path):
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
                        type_folder = ".rsg"
                    elif metadata_file[1] == "task":
                        type_folder = ".task_files"
                        param_user = "user"
                    elif metadata_file[1] == "direct":
                        param_user = "user"

                    data_to_send = {"data": data, "param_user": param_user}

                    found_user = find_user(**data_to_send)
                    if found_user:
                        current_user = found_user
            except Exception as e:
                print(f"Error reading JSON from {metadata_file[0]}: {e}")
                current_user = "Error reading JSON"

        # 🔹 Always store (CRITICAL)
        user_map[root] = current_user

        # 🔹 ONLY print if files exist
        if not files:
            continue

        if current_user == "Unknown":
            current_user = root.split("/")[12]

        # print(f"path : {root} \nUser: {current_user}")
        
        results.append({
            "path": root,
            "user": current_user,
            # "type": type_folder

        })

    return results




import subprocess

# def get_size(path):
#     cmd = f'find "{path}" -maxdepth 1 -type f -exec du -cb {{}} + | tail -n 1'
#     result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
#     size = result.stdout.strip()
#     return {
#         "path": path,
#         "size": size
#     }

def get_size(item):
    print(f"[START] {item} -> {threading.current_thread().name}")
    path = item["path"]
    user = item["user"]
    # type_folder = item.get["type_folder"])

    cmd = f'find "{path}" -maxdepth 1 -type f -exec du -cb {{}} + | tail -n 1'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    size = result.stdout.strip()
    print(f"[END]   {item} -> {threading.current_thread().name}")
    return {
        "path": path,
        "user": user,
        "size": size,
        # "type_folder": type_folder
    }

from concurrent.futures import ThreadPoolExecutor, as_completed

def process_all(items):
    results = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(get_size, item) for item in items]

        for f in as_completed(futures):
            results.append(f.result())

    return results
    # return results

# def get_size(path_list):
#     for item in path_list:
#      print(item["path"], item["user"])
#         # SIZE logic
#         cmd = f'''
#         find "{root}" -maxdepth 1 -type f -exec du -cb {{}} + | tail -n 1
#         '''

#         result = subprocess.run(
#             cmd,
#             shell=True,
#             capture_output=True,
#             text=True
#         )

#         # # print(user_map , end ="\n")
#         size = result.stdout.strip()

#         if current_user == "Unknown":
#         split_Data = root.split("/")
#         #    print(split_Data[12])
#         current_user = split_Data[12]

#         # print(f"{root} -> User: {current_user}, Size: {size}")


# if __name__ == "__main__":
#     data = get_all_data(base_path)
#     op = process_all(data)
#     print(op)

if __name__ == "__main__":
    data = get_all_data(base_path)

    op = process_all(data)

    # print(op)

    for item in op:
        print(f"Path : {item['path']}")
    
        print(f"User : {item['user']}")
        print(f"Size : {item['size']}")
        print("-" * 60)


    # paths = [item["path"] for item in results]
    # size_results = process_all(paths)

    # # Combine user and size info
    # for item in results:
    #     path = item["path"]
    #     user = item["user"]
    #     size_info = next((s for s in size_results if s["path"] == path), None)
    #     size = size_info["size"] if size_info else "Size not found"
    #     print(f"{path} -> User: {user}, Size: {size}")
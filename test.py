# import json 
# def find_user(data):
#     if isinstance(data, dict):
#         for k, v in data.items():
#             if k.lower() == "artist_name":
#                 return v
#             result = find_user(v)
#             if result:
#                 return result
#     # elif isinstance(data, list):
#     #     for item in data:
#     #         result = find_user(item)
#     #         if result:
#     #             return result
#     return None


# metadata_file = r"C:\Users\pooja\Documents\work_script\test_data\kng\sequences\kng_abjbdb1\kng_abjbdb1_shot\lgt\.task_files\manifest.json"
# user = "Unknown"


# if metadata_file:
#     try:
#         with open(metadata_file, "r") as f:
#             data = json.load(f)
#             found_user = find_user(data)
#             if found_user:
#                 user = found_user
#                 print(user)
#     except Exception:
#         user = "Error reading JSON"
# else:
#     print("error")


path = "/mnt/c/Users/pooja/Documents/work_script/test_data/kng/sequences/kng_abjbdb1/kng_abjbdb1_shot/lgt/extracted_aovsd"

split_Data = path.split("/")
print(split_Data[12])


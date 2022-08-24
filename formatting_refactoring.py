import os
from typing import List
import json 


def metadata_file_refactoring(file_path):
    a = None
    with open(file_path) as f:
        a = f.read().replace("HIT", "KNSR")
    with open(file_path, "w") as f:
        f.write(a)
    rename_metadata_file(file_path)

def rename_metadata_file(file_path):
    metadatas = load_metadata_file(file_path)
    for metadata in metadatas:
        if "files" in metadata: 
            for file in metadata["files"]:
                file_name, file_extension = os.path.splitext(file["title"])
                file_name = file_name[0:file_name.index(" -")]
                file["title"] = f"{file_name}{file_extension}"
    save_metadata(metadatas, file_path)

def load_metadata_file(file_path):
    with open(file_path) as f:
        return json.load(f)

def save_metadata(datasets, file_path):
    datasets = [dataset for dataset in datasets if dataset != {}]
    with open(file_path, "w") as f:
        f.write(json.dumps(datasets, indent=4))

def rename_files(directory_path):
    files = list_all_files(directory_path)
    for file in files:
        file_full_name = os.path.basename(file)
        file_name, file_extension = os.path.splitext(file_full_name)
        file_name = file_name[0:file_name.index(" -")].replace("HIT", "KNSR")
        new_file_name = os.path.join(directory_path, f"{file_name}{file_extension}" )
        os.rename(file, new_file_name)

def list_all_files(directory) -> List[str]:
    entries = os.walk(directory)
    file_list = []
    for entry in entries:
        file_list += [os.path.join(f"{entry[0]}/", file) for file in entry[2]]
    return file_list

    

directory_path = "/home/iconoyuri/Code/Dr Jiom internship/zenodo fetch api/test"
metadata_file_path = "/home/iconoyuri/Code/Dr Jiom internship/zenodo fetch api/zip_metadata.json"

rename_files(directory_path)
metadata_file_refactoring(metadata_file_path)

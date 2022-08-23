import zipfile
import shutil
from typing import List
import requests
import os
import json
from globals import max_size, min_size, page_length, access_token, url

def fetch_online_then_download( file_types, queries, metadata_file_name, files_folder_name, url = url, access_token = access_token):
    metadata = fetch_metadata(url, file_types, queries, access_token, metadata_file_name, page_length)
    download_files(metadata, metadata_file_name, files_folder_name)

def load_then_download( file_types, queries, metadata_file_name, files_folder_name, url = url, access_token = access_token):
    try:
        metadata = load_metadata_file(metadata_file_name)
        download_files(metadata, metadata_file_name, files_folder_name)
    except FileNotFoundError:
        fetch_online_then_download( file_types, queries, metadata_file_name, files_folder_name, url, access_token)

def fetch_metadata(url , file_types, queries, access_token, file_name, page_length = page_length ):
    print("__________ metadata querying started __________")

    datasets = []
    for query in queries:
        print(f"making requests on Zenodo \n\tquery = \"{query}\"")
        _url = url
        while True:
            resp = get_metadata(_url, file_types, page_length, query, access_token)
            datasets += resp["hits"]
            _url = resp["next"]
            if not _url:
                break

    print(f"__________ metadata querying over \n({len(datasets)} results found) __________")
    save_metadata(datasets, file_name)
    return datasets

def download_files(datasets, metadata_file, storage_dir):
    path = create_storage_directory(storage_dir)
    for x,dataset in enumerate(datasets):
        # if "files" in dataset:
        for y,file in enumerate(dataset["files"]) :
            if not file["downloaded"] :
                if download_file(file, path) :
                    file["downloaded"] = True
                    print(f" - - - - Downloaded successfully : {file['title']}")
                else: 
                    dataset["files"][y] = {} # deleting the file from the dataset                        
                save_metadata(datasets, metadata_file)
            else:
                print(f"+++++++ Already Downloaded : {file['title']}")
        if is_dataset_empty(dataset):
            datasets[x] = {}

def download_file(file, path):
    file_name = os.path.join(path, file["title"])
    file_name_x_ext = os.path.splitext(file["title"])[0]
    unziped_directory_name = os.path.join(path,file_name_x_ext)
    with open(file_name, "wb") as f:
        print(f"\tDownloading => {file['title']}")
        file_content = requests.get(file["link"], allow_redirects=True).content
        f.write(file_content)
        if file["type"] == 'zip':
            try:
                filtered_list = unzip_file(file_name, unziped_directory_name)
                shutil.rmtree(unziped_directory_name)
                if len(filtered_list) > 0:
                    file["unzipped_files"] = filtered_list
                    return True
            except zipfile.BadZipFile:
                print("bad file")
                return False
            finally:
                os.remove(file_name)
        else: 
            return True
    return False

def unzip_file(file_name, target_directory):
    with zipfile.ZipFile(file_name , "r") as zip_ref:
        zip_ref.extractall(target_directory)
    filtered_list = purge_zip_directory(target_directory)
    return filtered_list

def purge_zip_directory(directory):
    file_list = list_all_files(directory)
    filtered_list = []
    i = 1
    for file in file_list:
        if file.lower().endswith(('.csv', '.xlsx')) :
            if is_zip_child_relevant(filename=file) :
                directory_basename = os.path.basename(directory)
                directory_id = directory_basename[0:directory_basename.index(" -")] # The generated index of the file's parent folder 
                # We rename the file and move it to the zip files directory
                # It must be the grandfather folder ;)
                new_file_name = f"{directory_id}_Z{i} - {os.path.basename(file)}"
                os.rename(file, os.path.join(os.path.dirname(directory), new_file_name))
                filtered_list.append(new_file_name)
                i+=1
            else : 
                # If the unzipped folder contains a file for wich min_size < size < max_size, then, 
                # that folder is considered as unconsistent
                filtered_list = []
                break
        else:
            os.remove(file)
    return filtered_list

def get_metadata(url, file_types, page_length, query, access_token):
    params = {
        "access_token":access_token,
        "headers":{"Content-Type": "application/json"},
        "q":query,
        "size" : page_length,
        "status" : "published",
    }
    r = requests.get(url, params=params)
    r = r.json()

    i = 1
    hits = []
    for hit in r["hits"]["hits"]:
        if "files" in hit :
            rf_hit_id = f"HIT{i}" # reformated hit identifier
            files = []
            j = 1
            for file in hit["files"]:
                if file["type"] in file_types:
                    rf_file_id = f"{rf_hit_id}_F{j}"
                    file = {
                        "id" : rf_file_id,
                        "title" : f"{rf_file_id} - {file['key']}", 
                        "type" : file["type"], 
                        "link" : file["links"]["self"],
                        "size" : int(file["size"]),
                        "downloaded" : False,
                    }
                    if is_file_relevant(file):
                        files.append(file)
                        j+=1

            if len(files) > 0:
                rf_hit = { # reformated hit
                    "id" : rf_hit_id,
                    "doi" : hit["doi"],
                    "title": hit["metadata"]["title"],
                    "link" : hit["links"]["html"],
                    "files" : files
                }
                hits.append(rf_hit)
                i+=1
    
    return {
            "hits" : hits,
            "next" : "next" in r["links"] and r["links"]["next"]
        }

def save_metadata(datasets, file_name):
    print("__________ metadata file updating __________")
    datasets = [dataset for dataset in datasets if dataset != {}]
    with open(f"{file_name}.json", "w") as f:
        f.write(json.dumps(datasets, indent=4))
    print("__________ metadata file updating over __________")

def load_metadata_file(file_name):
    print("Loading metadata file")
    with open(f"{file_name}.json") as f:
        return json.load(f)

def is_file_relevant(file, min_size = min_size, max_size = max_size):
    # Here we ensure that the file isn't too big, doesn't overlap the max size allowed for a file to download
    size = int(file["size"])
    a = min_size < size and size < max_size
    return a

def is_zip_child_relevant(filename, min_size = min_size, max_size = max_size):
    # Here we ensure that the file isn't too big, doesn't overlap the max size allowed for a file to download
    size = os.path.getsize(filename)
    a = min_size < size and size < max_size
    return a

def create_storage_directory(directory, parent=""):
    parent_directory = os.getcwd()
    path = os.path.join(parent or parent_directory, directory)
    try:
        os.mkdir(path)
    except FileExistsError:
        print("storage folder already exists")
    finally:
        return path

def get_directory_path(directory):
    parent_directory = os.getcwd()
    path = os.path.join(parent_directory, directory)
    return path


def list_all_files(directory) -> List[str]:
    _directory = get_directory_path(directory)
    entries = os.walk(_directory)
    file_list = []
    for entry in entries:
        file_list += [os.path.join(f"{entry[0]}/", file) for file in entry[2]]
    return file_list

def is_dataset_empty(dataset):
    for file in dataset["files"]:
        if file != {}:
            return False
    return True
# def get_file_size(url):
#     response = requests.head(url, allow_redirects=True)
#     file_size = response.headers['Content-Length']
#     return file_size
    
# def update_datasets_file_size(file_name):
#     print("Updating metadata : adding files size")
#     datasets = load_metadata_file(file_name)
#     for dataset in datasets:
#         if "file_size" in dataset:
#             continue
#         dataset["file_size"] = get_file_size(dataset['file_link'])
#         save_metadata(datasets, file_name)

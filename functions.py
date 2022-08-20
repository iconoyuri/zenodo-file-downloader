from typing import List
import requests
import os
import json
from globals import max_size

def fetch_online_then_download(url, file_types, queries, access_token, metadata_file_name, files_folder_name):
    metadata = fetch_metadata(url, file_types, queries, access_token, metadata_file_name)
    download_files(metadata, metadata_file_name, files_folder_name, max_size)

def load_then_download(url, file_types, queries, access_token, metadata_file_name, files_folder_name):
    try:
        metadata = load_metadata_file(metadata_file_name)    
        download_files(metadata, metadata_file_name, files_folder_name, max_size)
    except FileNotFoundError:
        fetch_online_then_download(url, file_types, queries, access_token, metadata_file_name, files_folder_name)


def fetch_metadata(url , file_types, queries, access_token, file_name, page_length = 50 ):
    print("__________ metadata querying started __________")

    datasets = []
    for query in queries:
        print(f"making requests on Zenodo \n\tquery = \"{query}\"")
        _url = url
        while True:
            resp = get_metadata(_url, file_types, page_length, query, access_token)
            datasets += resp["hits"]
            _url = resp["next"]
            break
            if not _url:
                break

    print(f"__________ metadata querying over \n({len(datasets)} results found) __________")
    save_metadata(datasets, file_name)
    return datasets

def download_files(datasets, metadata_file, storage_dir, max_size):
    path = create_storage_directory(storage_dir)
    for dataset in datasets:
        for file in dataset["files"] :
            if is_file_relevant(file, max_size):
                if not file["downloaded"] :
                    download_file(file, path)
                    file["downloaded"] = True
                    save_metadata(datasets, metadata_file)
                    print(f" - - - - Downloaded successfully : {file['title']}")
                else:
                    print(f"+++++++ Downloaded : {file['title']}")
            else:
                print("Not relevant file")

def download_file(file, path):
    with open(f"{path}/{file['title']}", "wb") as f:
        print(f"\tDownloading => {file['title']}")
        file_content = requests.get(file["link"], allow_redirects=True).content
        f.write(file_content)

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
                    rf_file_id = f"{rf_hit_id}-F{j}"
                    files.append({
                        "id" : rf_file_id,
                        "title" : file["key"], 
                        "type" : file["type"], 
                        "link" : file["links"]["self"],
                        "size" : int(file["size"]),
                        "downloaded" : False,
                    })
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
    with open(f"{file_name}.json", "w") as f:
        f.write(json.dumps(datasets, indent=4))
    print("__________ metadata file updating over __________")

def load_metadata_file(file_name):
    print("Loading metadata file")
    with open(f"{file_name}.json") as f:
        return json.load(f)

def is_file_relevant(file, max_size):
    # Here we ensure that the file isn't too big, doesn't overlap the max size allowed for a file to download
    # print(file)
    return int(file["size"]) < max_size

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

import requests
import os
import json

def download_files_0(url, file_types, queries, access_token, metadata_file_name, files_folder_name):
    metadata = fetch_metadata(url, file_types, queries, access_token, metadata_file_name)
    save_metadata(metadata, metadata_file_name)
    metadata = load_metadata_file(metadata_file_name)
    download_files(metadata, metadata_file_name, files_folder_name)

def download_files(metadata_file_name, files_folder_name):
    metadata = load_metadata_file(metadata_file_name)
    download_files(metadata, metadata_file_name, files_folder_name)


def fetch_metadata(url , file_types, queries, access_token, file_name, page_length = 10000 ):
    print("__________ metadata querying started __________")

    datasets = []
    for query in queries:
        print(f"making requests on Zenodo \n\tquery = \"{query}\"")
        _url = url
        while True:
            resp = get_metadata(_url, file_types, page_length, query, access_token)
            datasets += resp["files"]
            _url = resp["next"]
            if not _url:
                break

    print(f"__________ metadata querying over \n({len(datasets)} results found) __________")
    save_metadata(datasets, file_name)
    return datasets

def save_metadata(datasets, file_name):
    print("__________ metadata file updating __________")
    with open(f"{file_name}.json", "w") as f:
        f.write(json.dumps(datasets, indent=4))
    print("__________ metadata file updating over __________")

def load_metadata_file(file_name):
    print("resuming metadata")
    with open(f"{file_name}.json") as f:
        return json.load(f)

def download_files(datasets, metadata_file, storage_dir):
    path = create_storage_directory(storage_dir)
    for dataset in datasets:
        if not dataset["downloaded"] :
            download_dataset(dataset, path)
            dataset["downloaded"] = True
            save_metadata(datasets, metadata_file)
        else:
            print("File already downloaded")

def download_dataset(dataset, path):
    with open(f"{path}/{dataset['file_title']}", "wb") as f:
        print(f"\tDownloading => {dataset['file_title']}")
        file_content = requests.get(dataset["file_link"], allow_redirects=True).content
        f.write(file_content)

def create_storage_directory(directory="files", parent=""):
    parent_directory = os.getcwd()
    path = os.path.join(parent or parent_directory, directory)
    try:
        os.mkdir(path)
    except FileExistsError:
        print("storage folder already exists")
    finally:
        return path

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

    files = []
    for hit in r["hits"]["hits"]:
        if "files" in hit :
            for file in hit["files"]:
                if file["type"] in file_types:
                    files.append({
                        "file_title" : file["key"], 
                        "file_type" : file["type"], 
                        "file_link" : file["links"]["self"],
                        "downloaded" : False
                    })
    
    return {
            "files" : files,
            "next" : "next" in r["links"] and r["links"]["next"]
        }



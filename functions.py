import requests
import os
import json

def download_dataset(dataset, path):
    with open(f"{path}/{dataset['file_title']}", "wb") as f:
        print(f"\tDownloading => {dataset['file_title']}")
        file_content = requests.get(dataset["file_link"], allow_redirects=True).content
        f.write(file_content)

def create_storage_directory():
    directory = "files"
    parent_directory = os.getcwd()
    path = os.path.join(parent_directory, directory)
    try:
        os.mkdir(path)
    except FileExistsError:
        print("storage folder already exists")
    finally:
        return path

def save_metadata(datasets):
    print("__________ metadata file updating __________")
    with open("metadata.json", "w") as f:
        f.write(json.dumps(datasets))
    print("__________ metadata file updating over __________")


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



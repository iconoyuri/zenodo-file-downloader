import json
import os
from dotenv import load_dotenv
from functions import create_storage_directory, download_dataset, save_metadata, get_metadata


load_dotenv()


access_token = os.getenv("ZENODO_ACCESS_TOKEN")
zenodo_url = os.getenv("ZENODO_URL")
# url = f"{zenodo_url}records/?page=1&type=dataset"
url = ""
page_length = 10000
file_types = ["xlsx", "csv"]
# file_types = ["zip", "xlsx", "csv"]
queries = ["food", "nutrition", "nutrients"]


def fetch_metadata(url, file_types, page_length, queries, access_token):
    print("__________ metadata querying started __________")

    datasets = []
    for query in queries:
        print(f"making requests on Zenodo \n\tquery = \"{query}\"")
        url = f"{zenodo_url}records/?page=1&type=dataset"
        while True:
            resp = get_metadata(url, file_types, page_length, query, access_token)
            datasets += resp["files"]
            url = resp["next"]
            if not url:
                break

    print(f"__________ metadata querying over \n({len(datasets)} results found) __________")
    save_metadata(datasets)
    return datasets

def load_metadata_file():
    print("resuming metadata")
    with open("metadata.json") as f:
        return json.load(f)

def download_files(datasets):
    path = create_storage_directory()
    for dataset in datasets:
        if not dataset["downloaded"] :
            download_dataset(dataset, path)
            dataset["downloaded"] = True
            save_metadata(datasets)
        else:
            print("File already downloaded")


# datasets = fetch_metadata(url, file_types, page_length, queries, access_token)
# download_files(datasets)
download_files(load_metadata_file())

# def print_data(url):
#     print(url)
# for query in queries:
#     print_data(url)


# results_nbr = len(datasets)

# download_datasets(datasets, results_nbr=results_nbr)

# print("Process ended")

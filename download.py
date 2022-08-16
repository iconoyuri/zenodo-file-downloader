import requests
import os


def download_datasets(datasets):
    path = create_storage_directory()
    for dataset in datasets:
        with open(f"{path}/{dataset['file_title']}", "wb") as f:
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
import zipfile
from functions import download_files_0, download_files_1, create_storage_directory
from globals import *
from typing import List

file_types = ["zip"]
metadata_file_name = "zip_metadata"
files_folder_name = "zip_datasets"
unzipped_files_folder_name = "zip_datasets"


def list_all_files(directory) -> List[str]:
    entries = os.walk(directory)
    file_list = []
    for entry in entries:
        file_list += [os.path.join(f"{entry[0]}/", file) for file in entry[2]]
    return file_list

def unzip_files(zip_files_folder_name):
    files_directory = create_storage_directory(zip_files_folder_name)
    file_list = list_all_files(files_directory)
    for file in file_list:
        with zipfile.ZipFile(file , "r") as zip_ref:
            zip_ref.extractall(files_directory)

def purge_zips_directory():
    file_list = list_all_files(unzipped_files_folder_name)
    for file in file_list:
        if file.lower().endswith(('.csv', '.xlsx')):
            ...
        else:
            os.remove(file)

download_files_0(url, file_types, queries, access_token, metadata_file_name, files_folder_name)
# download_files_1(metadata_file_name, files_folder_name)
unzip_files(files_folder_name)

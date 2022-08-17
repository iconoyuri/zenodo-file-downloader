import zipfile
from functions import download_files_0, download_files_1, create_storage_directory, get_directory_path
from globals import *
from typing import List
import os

file_types = ["zip"]
metadata_file_name = "zip_metadata"
files_folder_name = "zip_datasets"
unzipped_files_folder_name = "zip_datasets"


def list_all_files(directory) -> List[str]:
    _directory = get_directory_path(directory)
    entries = os.walk(_directory)
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

def purge_zips_directory(file_folder):
    file_list = list_all_files(file_folder)
    for file in file_list:
        if file.lower().endswith(('.csv', '.xlsx')):
            os.rename(file, f"{get_directory_path(file_folder)}/{os.path.basename(file)}")
        else:
            os.remove(file)

# download_files_0(url, file_types, queries, access_token, metadata_file_name, files_folder_name)
download_files_1(metadata_file_name, files_folder_name)
# unzip_files(files_folder_name)

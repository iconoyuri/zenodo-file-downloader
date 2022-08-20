import zipfile
from functions import list_all_files, create_storage_directory, get_directory_path
from globals import *
import os


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

# fetch_online_then_download(url, file_types, queries, access_token, metadata_file_name, files_folder_name)

# download_files_0(url, file_types, queries, access_token, metadata_file_name, files_folder_name)
# download_files_1(metadata_file_name, files_folder_name)
# unzip_files(files_folder_name)

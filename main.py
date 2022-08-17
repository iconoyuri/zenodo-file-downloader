from functions import download_files, download_files_0
from globals import *

file_types = ["xlsx", "csv"]
metadata_file_name = "metadata"
files_folder_name = "files"

# download_files_0(url, file_types, queries, access_token, metadata_file_name, files_folder_name)
download_files(metadata_file_name, files_folder_name)
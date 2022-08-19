from functions import download_files_1, download_files_0, update_datasets_file_size
from globals import *

file_types = ["xlsx", "csv"]
metadata_file_name = "metadata"
files_folder_name = "files"

# download_files_0(url, file_types, queries, access_token, metadata_file_name, files_folder_name)
# download_files_1(metadata_file_name, files_folder_name)
update_datasets_file_size(metadata_file_name)
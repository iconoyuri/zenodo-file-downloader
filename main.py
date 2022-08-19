from functions import load_then_download, fetch_online_then_download
from globals import *

xlsx_csv = options["xlsx_csv"]
zip = options["zip"]

fetch_online_then_download(url, xlsx_csv["file_types"], queries, access_token, xlsx_csv["metadata_file_name"], xlsx_csv["files_folder_name"])
fetch_online_then_download(url, zip["file_types"], queries, access_token, zip["metadata_file_name"], zip["files_folder_name"])
# load_then_download( metadata_file_name, files_folder_name)
# update_datasets_file_size(metadata_file_name)
from functions import load_then_download
from globals import *

xlsx_csv = options["xlsx_csv"]
zip = options["zip"]

load_then_download(url, xlsx_csv["file_types"], queries, access_token, xlsx_csv["metadata_file_name"], xlsx_csv["files_folder_name"])
load_then_download(url, zip["file_types"], queries, access_token, zip["metadata_file_name"], zip["files_folder_name"])

# Developed by _Ico no yuri_ and shared using APACHE LICENSE, Version 2.0
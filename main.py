# Developed by _Ico no yuri_ and shared using APACHE LICENSE, Version 2.0


from functions import load_then_download
from globals import *

options = {
    "xlsx_csv" : {
        "file_types" : ["xlsx", "csv"] ,
        "metadata_file_name" : "xlsx_csv_metadata",
        "files_folder_name" : "xlsx_csv_datasets",
    },
    "zip" : {
        "file_types" : ["zip"],
        "metadata_file_name" : "zip_metadata",
        "files_folder_name" : "zip_datasets",
    }
}
# queries = ["food"]
queries = ["food", "nutrition", "nutrients"]

xlsx_csv = options["xlsx_csv"]
zip = options["zip"]

# load_then_download(xlsx_csv["file_types"], queries, xlsx_csv["metadata_file_name"], xlsx_csv["files_folder_name"])
load_then_download(zip["file_types"], queries, zip["metadata_file_name"], zip["files_folder_name"])

import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("ZENODO_ACCESS_TOKEN")
zenodo_url = os.getenv("ZENODO_URL")
queries = ["food", "nutrition", "nutrients"]
page_length = 10000
url = f"{zenodo_url}records/?page=1&type=dataset"
max_size = 30<<20 # 30MiB
# max_size = 1<<20 # 1MiB
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
import os
from dotenv import load_dotenv
import fetch
from download import download_datasets 

load_dotenv()

zenodo_url = os.getenv("ZENODO_URL")
url = f"{zenodo_url}records/?page=1&type=dataset"
file_types = ["zip", "xlsx", "csv"]
page_length = 3


treated_response = {"files": []}
datasets = []

while True:
    resp = fetch.fetch_files(url, file_types, page_length=page_length,query="food")
    datasets += resp["files"]
    url = resp["next"]
    if not url:
        break

download_datasets(datasets)


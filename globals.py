import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("ZENODO_ACCESS_TOKEN")
zenodo_url = os.getenv("ZENODO_URL")
queries = ["food", "nutrition", "nutrients"]
# page_length = 10000
url = f"{zenodo_url}records/?page=1&type=dataset"

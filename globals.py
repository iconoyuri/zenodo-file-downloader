import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("ZENODO_ACCESS_TOKEN")
zenodo_url = os.getenv("ZENODO_URL")
page_length = 10000
url = f"{zenodo_url}records/?page=1&type=dataset"

max_size = 30<<20 # 30 MiB
# max_size = 1<<20 # 1 MiB
min_size = 500 # 500 bytes

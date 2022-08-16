import requests
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("ZENODO_ACCESS_TOKEN")
zenodo_url = os.getenv("ZENODO_URL")
headers = {"Content-Type": "application/json"}

def fetch_files(url, file_types, page_length, query):
    params = {
        "access_token":access_token,
        "headers":headers,
        "q":query,
        "size" : page_length,
        "status" : "published",
    }
    r = requests.get(url, params=params)
    r = r.json()


    files = []
    for hit in r["hits"]["hits"]:
        if "files" in hit :
            for file in hit["files"]:
                if file["type"] in file_types:
                    files.append({
                        "file_title" : file["key"], 
                        "file_type" : file["type"], 
                        "file_link" : file["links"]["self"]
                    })
    
    return {
            "files" : files,
            "next" : "next" in r["links"] and r["links"]["next"]
        }



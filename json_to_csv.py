import json
import os
import csv

header = ["article_doi", "article_title", "article_link", "file_title", "file_download_link"]


def convert_xslx_csv_metadata_file(file_path, header=header):

    converted_file_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, encoding="utf-8") as json_file:
        datasets = json.load(json_file)

    with open(f"{converted_file_name}.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for dataset in datasets:
            for file in dataset["files"]:
                row = [dataset["doi"], dataset["title"], dataset["link"], file["title"], file["link"]]
                writer.writerow(row)
            

def convert_zip_metadata_file(file_path, header=header):

    converted_file_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, encoding="utf-8") as json_file:
        datasets = json.load(json_file)

    with open(f"{converted_file_name}.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for dataset in datasets:
            for file in dataset["files"]:
                for uzip_file in file["unzipped_files"]:
                    row = [dataset["doi"], dataset["title"], dataset["link"], uzip_file, file["link"]]
                    writer.writerow(row)
            
# Set the metadata file path
file_path = "/home/iconoyuri/Code/Dr Jiom internship/zenodo fetch api/zip_metadata.json"

# **************** Uncomment here the function to execute ******************

# convert_xslx_csv_metadata_file(file_path)
# convert_zip_metadata_file(file_path)


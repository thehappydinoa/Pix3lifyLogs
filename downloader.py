import os

import boto3

s3 = boto3.resource("s3")
bucket = s3.Bucket("pix3lify-logs")

if not os.path.exists("logs"):
    os.makedirs("logs")


def download_folder(key):
    logs_folder = "logs"
    local_folder = "/".join([logs_folder, key])
    contents = bucket.meta.client.list_objects(
        Bucket=bucket.name, Prefix=key).get("Contents")
    if contents:
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)
    else:
        print("Could not find " + key)
        return
    for content in contents:
        file_key = content.get("Key")
        bucket.download_file(
            file_key, "/".join([logs_folder, file_key.replace("/Pix3lify_logs", "")]))
    return key


if __name__ == '__main__':
    key = input("Key: ")
    download_folder(key)

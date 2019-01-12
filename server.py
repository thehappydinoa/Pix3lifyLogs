#!/usr/bin/env python
import os
import tarfile
# import zipfile
from io import BytesIO
from uuid import uuid4

import boto3

from sanic import Sanic, response

app = Sanic()

s3 = boto3.resource("s3")
bucket = s3.Bucket("pix3lify-logs")


GOOD_EXT = [".log", ".txt", ".xml", ".prop"]
BAD_EXT = ["__MACOSX", "._"]

EXTRA_ARGS = {"ACL": "public-read"}


def good_filename(filename):
    return any(ext in filename for ext in GOOD_EXT) and not any(ext in filename for ext in BAD_EXT)


# async def save_zip(content, folder):
#     try:
#         zip = zipfile.ZipFile(BytesIO(content), "r")
#         for filename in zip.namelist():
#             if good_filename(filename):
#                 print("Uploading " + filename)
#                 bucket.upload_fileobj(BytesIO(zip.read(
#                     filename)), "/".join([folder, filename]), ExtraArgs=EXTRA_ARGS)
#                 print("Uploaded " + filename)
#     except zipfile.BadZipfile:
#         print("Bad .zip")


async def save_tar(content, folder):
    try:
        tar = tarfile.open(fileobj=BytesIO(content), mode="r")
        for member in tar.getmembers():
            if good_filename(member.name):
                print("Uploading " + member.name)
                bucket.upload_fileobj(BytesIO(member.tobuf(
                )), "/".join([folder, member.name]), ExtraArgs=EXTRA_ARGS)
                print("Uploaded " + member.name)
    except tarfile.TarError:
        print("Bad .tar.xz")


@app.route("/")
def index(request):
    return response.redirect(os.getenv("REDIRECT_URL",
                                       "https://github.com/Magisk-Modules-Repo/Pix3lify"))


@app.route("/submit", methods=["POST", "PUT"])
async def submit_logs(request):
    logs_file = request.files.get("logs")
    if logs_file:
        body = logs_file.body
    else:
        body = request.body
    key = str(uuid4())
    if len(body) < 500000:
        app.add_task(save_tar(body, key))
        return response.text(key)
    return response.text("Failed .tar.xz file too large",
                         status=406)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)),
            workers=int(os.getenv("WORKERS", 1)), auto_reload=True)

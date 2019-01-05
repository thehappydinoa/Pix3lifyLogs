import os
from io import BytesIO
from time import sleep
from uuid import uuid4
from zipfile import BadZipfile, ZipFile

import boto3

from sanic import Sanic, response

app = Sanic()

s3 = boto3.resource("s3")
bucket = s3.Bucket("pix3lify-logs")


REDIRECT_URL = os.getenv(
    "REDIRECT_URL", "https://github.com/Magisk-Modules-Repo/Pix3lify")


class BadExtensionException(Exception):
    pass


async def save_logs(zip_content, folder):
    zip_file = "logs/" + folder + ".zip"
    try:
        open(zip_file, "wb").write(zip_content)
        zip = ZipFile(zip_file, "r")
        for filename in zip.namelist():
            if any(ext in filename for ext in [".log", ".txt", ".xml", ".prop"]) and not any(ext in filename for ext in ["__MACOSX"]):
                print("Uploading " + filename)
                bucket.upload_fileobj(BytesIO(zip.read(
                    filename)), "/".join([folder, filename]), ExtraArgs={'ACL': 'public-read'})
    except BadZipfile:
        print("Bad Zipfile")
    finally:
        os.remove(zip_file)


@app.route("/")
def index(request):
    return response.redirect(REDIRECT_URL)


@app.route("/logs", methods=["POST"])
async def submit_logs(request):
    logs_file = request.files.get("logs")
    print(logs_file.type)
    key = str(uuid4())
    if len(zip_content) < 500000:
        app.add_task(save_logs(logs_file.body, key))
        return response.json({
            "key": key,
        })
    return response.text("Failed zip file too large")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)),
            workers=int(os.getenv("WORKERS", 1)), auto_reload=True)

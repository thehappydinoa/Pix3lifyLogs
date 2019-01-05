from os import getenv

from boto3 import client

from sanic import Sanic, response

app = Sanic()

s3 = client("s3")

REDIRECT_URL = getenv("REDIRECT_URL", "https://github.com/Magisk-Modules-Repo/Pix3lify")

@app.route("/")
def index(request):
    return response.redirect(REDIRECT_URL)


@app.route("/logs", methods=["POST"])
def submit_logs(request):
    print(request.headers)
    print(request.body)
    return response.text("OK")


app.run(host="0.0.0.0", port=int(getenv("PORT", 5000)), workers=2)

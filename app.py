from flask import Flask, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
import requests
import xml_formatter
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    os.environ['BASIC_AUTH_USERNAME']: os.environ['BASIC_AUTH_PASSWORD']
}

# Rossum login
def rossum_auth():
    res = requests.post("https://api.elis.rossum.ai/v1/auth/login",
                        {"username": "tedec67391@diolang.com", "password": "32q^BaSoYLj6U@Z%Dw"})
    if res.ok:
        return res.json()["key"]
    raise ValueError(res.content)


@auth.verify_password
def verify_password(username, password):
    if username in users and users.get(username) == password:
        return username


@app.route('/export', methods=["GET", "POST"])
@auth.login_required
def index():
    if request.method == "POST":
        annotation_id = request.form.get("annotation")
        queue_id = request.form.get("queue")

        # Check if numbers
        try:
            annotation_id = int(annotation_id)
            queue_id = int(queue_id)
        except Exception:
            return "Not a number"

        try:
            token = rossum_auth()
        except ValueError as err:
            return "Failed to login to Rossum"

        # Get the document
        # https://api.elis.rossum.ai/v1/queues/170679/export?format=xml&id=12040765
        res = requests.get("https://api.elis.rossum.ai/v1/queues/" + str(queue_id) + "/export?format=xml&id=" + str(annotation_id), headers={"Authorization": "token " + token})
        if res.ok:
            xml_formated = xml_formatter.reformat_xml(res.content)

            try:
                res = requests.post("https://my-little-endpoint.ok/rossum", {"annotationId": annotation_id, "content": xml_formated})
                return jsonify({"success": res.ok})
            except:
                return jsonify({"success": False})
        else:
            return res.content

    return render_template("export_form.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
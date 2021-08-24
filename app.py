import os
import fitz
from api import FILE
from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from classes.NewHeaders import NewHeaders
from classes.PageNumbers import PageNumbers

# set FLASK_APP=hello
# flask run

# Testing

app = Flask(__name__, instance_relative_config=True)
CORS(app, resources={r"/*": {"origins": "*"}})

# UPLOAD_FOLDER = './uploads' # Not sure what this does.
app.config['UPLOAD_FOLDER'] = "./tmp"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Find out what takes so long when we do redactions.


@app.route('/')
def index():
    return 'Index Page'


@app.route('/upload', methods=['GET', 'POST', 'PUT'])
def upload_route():
    if request.method == "POST":
        FILE.upload(request.files['file'])
        page_count = FILE.data["pageCount"]
        # return send_file("./tmp/test.pdf")
        res = make_response(send_file("./tmp/test.pdf"))
        res.headers['X-PageCount'] = page_count
        # print(os.listdir("./tmp"))
        return res
    elif request.method == 'PUT':
        FILE.close()
        return {}
    else:
        return {
            "file": FILE.data
        }


@app.route('/headers/apply', methods=['POST'])
def apply_headers_route():
    headers = request.form["headers"]
    NewHeaders.applyHeaders(headers)
    testing = fitz.open("./tmp/test.pdf", filetype="pdf")
    print(testing.metadata)
    return send_file("./tmp/test.pdf")


@app.route('/pageNumbers/apply', methods=['POST'])
def apply_page_numbers_route():
    page_numbers = request.form["pageNumbers"]
    PageNumbers.apply_page_numbers(page_numbers)
    return send_file("./tmp/test.pdf")


# if __name__ == '__main__':
#     app.run()

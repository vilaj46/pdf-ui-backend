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
        file_path = FILE.data['filePath']
        file_name = FILE.data['fileName']
        res = make_response(send_file(file_path))
        res.headers['X-PageCount'] = page_count
        res.headers['X-fileName'] = file_name
        res.headers['X-filePath'] = file_path
        FILE.close()  # Simulate heroku
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
    file_name = request.form['fileName']
    file_path = request.form['filePath']
    FILE.initialize_uploaded_document(file_name, file_path)

    NewHeaders.applyHeaders(headers)
    return send_file(file_path)


@app.route('/pageNumbers/apply', methods=['POST'])
def apply_page_numbers_route():
    page_numbers = request.form["pageNumbers"]
    PageNumbers.apply_page_numbers(page_numbers)
    return send_file("./tmp/test.pdf")


# if __name__ == '__main__':
#     app.run()

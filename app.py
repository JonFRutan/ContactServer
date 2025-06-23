#jfr
import requests
from flask import Flask, render_template, request, redirect, url_for
import PythonScripts as cs

#NOTE
# While app.py is running we should maintain an access point
# for anything making a request for the contacts list.
# The contacts list can be dynamically updated and replaced so
# that any subsequent calls to that IP will get a newly updated .vcf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
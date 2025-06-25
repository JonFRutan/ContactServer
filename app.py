#jfr
import requests
from flask import Flask, render_template, request, redirect, url_for
import PythonScripts as cs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask import request
from flask import render_template
import json
app = Flask(__name__,static_url_path='')




@app.route('/')
def send_home():
	return return render_template('index.html',tag ="test")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

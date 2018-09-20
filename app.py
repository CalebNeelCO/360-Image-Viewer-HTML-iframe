from flask import Flask
from flask import request
from flask import render_template
import json
app = Flask(__name__,static_url_path='')




@app.route('/', methods=["GET", "POST"])
def send_home():
	url = request.args.get("url")
	title = request.args.get("title")
	author = request.args.get("author")
	expand = True
	if(title is None):
		expand = False
	return render_template('index.html',url=url,title=title,author=author,expand=expand)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

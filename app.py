#AIzaSyD9BTxjx1z_1My-RJRioZT509nxVctcux4

from flask import Flask
from flask import request
from flask import redirect, send_from_directory
from flask import render_template
from datetime import datetime
from github import Github
import urllib2
import base64
import json
app = Flask(__name__,static_url_path='')

org = g.get_organization("NaviGlobeTreks")
user = g.get_user()


@app.route('/')
def send_home():
	return sendwordpress("https://naviglobetreks.wordpress.com/")

@app.route('/directions')
def send_dir():
	return sendwordpress("https://naviglobetreks.wordpress.com/directions/")

@app.route('/completed')
def send_completed():
	return sendwordpress("https://naviglobetreks.wordpress.com/completed-projects/")

@app.route('/project')
def send_pro():
	return sendwordpress("https://naviglobetreks.wordpress.com/completed-projects/")

@app.route('/privacy')
def Privicy():
    return send_from_directory('static', 'Privicy.html')

@app.route('/js')
def js():
    return send_from_directory('static', 'main.js')

@app.route('/convert')
def convert():
    return send_from_directory('static', 'convert.html')

@app.route('/completedtable')
def completed():
    
	re = {}  
	re['main'] = []  
	
	for repo in org.get_repos():
		data = json.loads(repo.get_file_contents("/README.md").content.decode('base64')) 
		data = data['main']
		re['main'].append({  
	    'title':  data['title'],
	    'description': data['description'],
	    'grade': data['grade'],
	    'subject':  data['subject'],
	    'auther': data['auther'],
	    'url' : repo.name
		})
	return render_template('com.html',tag =re['main'])#data['main']

@app.route('/project/<name>', methods = ['GET'])
def show_user_profile(name):
    page = request.args.get("id")
    id = '1'
    
    if(page is None):
		return Showhomepage(name)
    	
    else:
		id = page
		for repo in org.get_repos():
			if(repo.name == name):
				data = json.loads(repo.get_file_contents("/README.md").content.decode('base64')) 
				if id in data['main']:
					#repo.create_file("/1.html", "init commit", render_template('main.html',tag =data['main'][id], vi=int(id), url = repo.name))
					return render_template('main.html',tag =data['main'][id], vi=int(id), url = repo.name, main = decodemain(data['main'][id]['main']))#data['main']
				else:
					return Showhomepage(name)
		
@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
	if request.method == 'POST':
	    content = request.get_json()
	    if(checkrepo(content['main']) == ""):
	    	msg = creatrepo(content['main'])
	    else:
	    	repo = org.get_repo(checkrepo(content['main']))
	    	file = repo.get_file_contents("/README.md")
            repo.update_file("/README.md", "your_commit_message", json.dumps(content, indent=4, sort_keys=True),file.sha) 
      
            url = "www.naviglobetreks.com/project/" + checkrepo(content['main']) 
            repo.edit(homepage=url)
            #repo.create_file("/index.html", "init commit", render_template('main.html'),file.sha)
	    	
	return "www.naviglobetreks.com/project/" + checkrepo(content['main']) 
	

def sendwordpress(url):
	return render_template('word.html',tag =url)


def checkrepo(data):
	for repo in org.get_repos():
		if(str(repo.description) == str(data['id'])):
			return repo.name
	return ""

def creatrepo(data):
	name = data['title'].replace(" ", "-")
	for repo in g.get_organization("NaviGlobeTreks").get_repos():
		if(repo.name == name):
			name = name + "-" +data['id']
	url = "www.naviglobetreks.com/project/" + name
	repo = org.create_repo(name, description=data["id"],private=False,auto_init=True,homepage=url)
	repo.create_file("/README.md", "init commit", json.dumps(data, indent=4, sort_keys=True))
	return repo.name

def convertimg(img):
	if(data.find("drive.google.com/file/d/") != -1):
		img = img.replace("https://drive.google.com/file/d/", "https://drive.google.com/uc?export=view&id=")
		img = img.replace("/view?usp=sharing", "")
	return img
    
def decodemain(data):
  if(data.find("earth.google.com") == -1):
      if(data.find("youtu") == -1):
        return mainimg(data)
      else:
        return mainyoutube(data)
  else:
      return mainmap(data)
      
def mainimg(data):
  return "<img src='" + data + "' style='object-fit: contain;width:100%;height:100%;'>"
  
def mainyoutube(data):
  c = "/"
  data = data.split(c)
  ur = data[3] 
  ur = ur.replace("watch?v=","")
  data =  "<iframe src='https://www.youtube.com/embed/" + ur + "' frameborder='0' id='ifm' allow='autoplay; encrypted-media' style='width: 100%;' allowfullscreen></iframe>"
  return data
  #print url

def mainmap(data):
	c = "@"
	d = ","
	if(data.find("streetview") == -1):
		data = data.split(c)
		data = data[1].split(d)
  		return "<iframe src='https://www.google.com/maps/embed/v1/view?key=AIzaSyDWGsDmH0LO0as2IBNB4Vb_isW7lf2r658&center=" + data[0] + "," + data[1] + "&maptype=satellite&zoom=22' style='width: 100%;' id='ifm' allowfullscreen></iframe>" 
  	else:
  		data = data.split(c)
		data = data[1].split(d)
  		return "<iframe src='https://www.google.com/maps/embed/v1/streetview?key=AIzaSyDWGsDmH0LO0as2IBNB4Vb_isW7lf2r658&location=" + data[0] + "," + data[1] + "&heading=210&pitch=10&fov=35' style='width: 100%;' id='ifm' allowfullscreen></iframe>" 

def Showhomepage(name):
	for repo in org.get_repos():
		if(repo.name == name):
		    data = json.loads(repo.get_file_contents("/README.md").content.decode('base64')) 
		    return render_template('home.html',tag =data['main'])#data['main']

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

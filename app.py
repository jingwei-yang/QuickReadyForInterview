from flask import Flask, jsonify, render_template, request
import requests

# Create an Flask app object.  We'll use this to create the routes.
app = Flask(__name__)

# Allow Flask to autoreload when we make changes to `app.py`.
app.config['DEBUG'] = True # Enable this only while testing!

@app.route('/')
def hello():
	return render_template('hello.html')

@app.route('/search', methods=["GET", "POST"])
def search():
	if request.method == "POST":
		url = "https://api.github.com/search/repositories?q=" + request.form["user_search"]
		print request.form
		response = requests.get(url)
		response_dict = response.json()
		return render_template("results.html", api_data=response_dict, name="bob")
	else: # request.method == "GET"
		return render_template("search.html")

# Handle
@app.errorhandler(404)
def not_found(error):
	return "Sorry, I haven't coded that yet.", 404

@app.errorhandler(500)
def internal_server_error(error):
	return "My code broke, my bad.", 500


@app.route('/info/<company_name>')
def get_posts(company_name):
    #Returns the list of updates of a company.
    TOKEN ='575731909230644|ZuJwTeYLANGBOsZFWPczcx8JDZo'
    parameters = {'access_token': TOKEN}
    response = requests.get('https://graph.facebook.com/'+ company_name + '/feed', params=parameters)
    response_dict = response.json()
    return jsonify(response_dict)

@app.route('/searchgd')
def search_glassdoor():
    url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=29781&t.k=jQdxv7dRxPc&action=employers&q=Google&userip=0.0.0.0&useragent=Chrome"
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}
    response_dict  = requests.get(url, headers = user_agent).json()
    return jsonify(response_dict)

# If the user executed this python file (typed `python app.py` in their
# terminal), run our app.
if __name__ == '__main__':
	app.run(host='0.0.0.0')
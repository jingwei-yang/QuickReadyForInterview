from flask import Flask, jsonify, render_template, request
#import requests

# Create an Flask app object.  We'll use this to create the routes.
app = Flask(__name__)

# Allow Flask to autoreload when we make changes to `app.py`.
app.config['DEBUG'] = True # Enable this only while testing!

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    return jsonify(ret_data)
 

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        user_agent = {'User-agent': request.headers.get('User-Agent')}
        glassdoor_url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=29781&t.k=jQdxv7dRxPc&action=employers&userip=0.0.0.0&useragent=Chrome&q=" + request.form["user_search"]
        glassdoor_response_dict = requests.get(glassdoor_url, headers = user_agent).json()
        return jsonify(glassdoor_response_dict)
    else:
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

@app.route('/searchgd/<search_query>')
def search_glassdoor(search_query):
    url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=29781&t.k=jQdxv7dRxPc&action=employers&userip=0.0.0.0&useragent=Chrome&q=" + search_query
    user_agent = {'User-agent': request.headers.get('User-Agent')}
    response_dict  = requests.get(url, headers = user_agent).json()
    return jsonify(response_dict)

# If the user executed this python file (typed `python app.py` in their
# terminal), run our app.
if __name__ == '__main__':
    app.run(host='0.0.0.0')
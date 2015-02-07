from flask import Flask, jsonify, render_template, request
import requests
import nytime

# Create an Flask app object.  We'll use this to create the routes.
app = Flask(__name__)

# Allow Flask to autoreload when we make changes to `app.py`.
app.config['DEBUG'] = True # Enable this only while testing!


# Three main pages
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/search', methods=["GET", "POST"])
def search():
    return render_template('search.html')

@app.route('/results', methods=["GET", "POST"])
def results():
    data = {}
    if request.method == "POST":
        keyword = request.form['company-name']
        data['glassdoor'] = glassdoor(keyword)
        data['linkedin'] = linkedin(keyword)
        data['nytimes'] = nytimes(keyword)
        data['facebook'] = facebook(keyword)
        return render_template('results.html', api_data=data)
    return render_template('search.html')


# Login related pages
@app.route('/login')
def login():
    pass

@app.route('/linkedin')
def login_done():
    pass


# Error Handler
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

@app.route('/glassdoor/<search_query>')
def search_glassdoor(search_query):
    user_agent = {'User-agent': request.headers.get('User-Agent')}
    glassdoor_url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=29781&t.k=jQdxv7dRxPc&action=employers&userip=0.0.0.0&useragent=Chrome&q=" + search_query
    glassdoor_response_dict = requests.get(glassdoor_url, headers = user_agent).json()
    glassdoor_response_dict = process_glassdoor_response(glassdoor_response_dict, search_query)
    return jsonify(glassdoor_response_dict)

def process_glassdoor_response(api_dict, company_name):
    if api_dict.get("success") is False:
        return {"success":False,"status":"Failed to retrieve company data"}
    filtered_dict = {"companies":[]}
    response_dict = api_dict.get("response")
    if not response_dict:
        return {"success":False,"status":"Failed to retrieve company data"}
    employers_list = response_dict.get("employers")
    if not employers_list:
        return {"success":False,"status":"no matching companies"}
    for employer in employers_list:
        if company_name.lower() in employer.get("name").lower():
            filtered_employer = {"name":employer.get("name"),"website":employer.get("website"),
            "industry":employer.get("industry"),"logo":employer.get("squareLogo")}
            ceo = employer.get("ceo")
            if ceo:
                filtered_ceo = {"name":ceo.get("name"),"title":ceo.get("title")}
                if ceo.get("image"):
                    filtered_ceo["image"] = ceo.get("image")
                filtered_employer["ceo"] = filtered_ceo
            filtered_dict["companies"].append(filtered_employer)
    if not filtered_dict.get("companies"):
        return {"success":False,"status":"no matching companies"}
    return filtered_dict

# Backend API
def glassdoor(keyword):
    user_agent = {'User-agent': request.headers.get('User-Agent')}
    glassdoor_url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=29781&t.k=jQdxv7dRxPc&action=employers&userip=0.0.0.0&useragent=Chrome&q=" + keyword
    glassdoor_response_dict = requests.get(glassdoor_url, headers = user_agent).json()
    glassdoor_response_dict = process_glassdoor_response(glassdoor_response_dict, keyword)
    return glassdoor_response_dict

def linkedin(keyword):
    return {}

def facebook(keyword):
    return {}

def nytimes(keyword):
    return {}

# If the user executed this python file (typed `python app.py` in their
# terminal), run our app.
if __name__ == '__main__':
    app.run(host='0.0.0.0')
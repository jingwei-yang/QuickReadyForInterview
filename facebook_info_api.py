@app.route('/info/<company_name>')
def get_posts(company_name):
    #Returns the list of updates of a company.
    TOKEN ='575731909230644|ZuJwTeYLANGBOsZFWPczcx8JDZo'
    parameters = {'access_token': TOKEN}
    response = requests.get('https://graph.facebook.com/'+ company_name + '/feed', params=parameters)
    response_dict = response.json()
    return jsonify(response_dict)



@app.route('/facebook_info/<company_name>')
def get_facebook_info(company_name):
    #Returns the list of updates of a company.
    TOKEN ='575731909230644|ZuJwTeYLANGBOsZFWPczcx8JDZo'
    parameters = {'access_token': TOKEN}
    response = requests.get('https://graph.facebook.com/'+ company_name + '/feed', params=parameters)
    response_dict = response.json()
    info_collection = []
    for item in response_dict['data']:
        abstract = {}
        if (item.has_key('status_type') and item['status_type'] == "shared_story") :
            abstract['link'] = item['link']
                abstract['message'] = item['message']
                abstract['name'] = item['name']
                abstract['picture'] = item['picture']
                abstract['updated_time'] = item['updated_time']
                info_collection.append(abstract);
    ret = {'data' : info_collection}
    return jsonify(ret);







import requests
import urllib


def nytime_json(keyword='google'):
    '''
    demo:
    result = nytime_json('google')
    for it in result:
        if it['abstract']:
            print it['abstract'].encode('UTF-8') 
    '''
    base_url = r'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    query = r'keyword'
    begin_date = r'20100101'
    fq = r'news_desk:("Business" "Technology")'
    api_key = r'7182809a0aab73c3c0fb8b6d0af04c31:5:71187653'

    payload = {'q': query, 'fq': fq, 'begin_date': begin_date, 'api-key': api_key}

    response = requests.get(base_url, params=payload).json()
    result = response['response']['docs']

    return result

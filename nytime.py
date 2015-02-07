import requests
import urllib
import json
import HTMLParser
h = HTMLParser.HTMLParser()

def nytime_json(keyword='google'):
    base_url = r'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    query = keyword
    begin_date = r'20100101'
    fq = r'news_desk:("Business" "Technology") AND headline:("%s")' % keyword
    api_key = r'7182809a0aab73c3c0fb8b6d0af04c31:5:71187653'
    result = []

    payload = {
        'q': query,
        'fq': fq,
        'page': 0,
        'begin_date': begin_date,
        'api-key': api_key
    }

    for p in range(2):
        payload['page'] = p
        response = requests.get(base_url, params=payload).json()
        result0 = response['response']['docs']

        for it in result0:
            if it['lead_paragraph'] is None: continue
            web_url = it['web_url']
            headline = it['headline']['main'].encode('ascii', "ignore")
            paragraph = it['lead_paragraph'].encode('ascii', "ignore")
            pub_date = it['pub_date'][:10]
            thumb = next((x['url']
                          for x in it['multimedia']
                          if x['subtype']=='thumbnail'),
                         '')
            result.append({
                'link': web_url,
                'headline': h.unescape(headline),
                'message': h.unescape(paragraph),
                'pub_date': pub_date,
                'picture': thumb
                })

    return {'data': result} # warp into a dictionary

if __name__ == '__main__':
    result = nytime_json('google')
    print result
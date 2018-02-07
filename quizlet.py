#!/usr/bin/env python
import requests
import random
import webbrowser

class InvalidParam(Exception):
    pass

def get_quizlet_bearer_token(code, uri):
    endpoint = 'https://api.quizlet.com/oauth/token'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic Q2tGTkJ1RVBmejpDVk10YmRkUUZLNlN3RnU1Z3puWlVQ'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': uri
    }

    resp = requests.post(endpoint, headers=headers, data=data)
    if resp.status_code == 400:
        raise InvalidParam('One of the parameters are invalid.')

    return resp.json()['access_token']


def oauth():
    random_string = '%010x' % random.randrange(16**10)
    url = 'https://quizlet.com/authorize?response_type=code&client_id=CkFNBuEPfz&scope=write_set'+\
            f'&state={random_string}'
    webbrowser.open(url)

    return url

def post_to_quizlet(title, terms, definitions, token):
    endpoint = 'https://api.quizlet.com/2.0/sets'
    headers = {
        'Host': 'api.quizlet.com',
        'Authorization': f'Bearer {token}' 
    }
    data = {
        'terms[]': terms,
        'definitions[]': definitions,
        'lang_terms': 'en',
        'lang_definitions': 'en',
        'title': title
    }
    try:
        res = requests.post(endpoint, data=data, headers=headers)
    except Exception as e:
        print(e)
        return

    return res.json()

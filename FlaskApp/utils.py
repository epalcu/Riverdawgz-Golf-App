from golfers import golfers
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json

class Utils():
    def __init__(self):
        return

    def is_good_response(self, resp):
        '''
        Returns true if the response seems to be HTML, false otherwise
        '''

        content_type = resp.headers['Content-Type'].lower()

        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)

    def simple_get(self, url):
        '''
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None
        '''

        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None
        except RequestException as e:
            return None

    def updatePosition(self):
        html = self.simple_get('http://www.espn.com/golf/leaderboard/_/tournamentId/401056527')
        contents = BeautifulSoup(html, 'html.parser')

        jsonObject = json.loads(str(contents.find('script')).strip("<script type=\"text/javascript\">window['__espnfitt__']=").strip(';'))
        competitors = jsonObject['page']['content']['leaderboard']['competitors']
        
        # Now we simply loop over our names list,
        # see if name is in our golfers dictionary, 
        # and set his/her position key
        for competitor in competitors:
            for golfer in golfers:
                if golfer['name'] in competitor['name']:
                    try:
                        golfer['overall'] = str(competitor['toPar'])
                        if str(competitor['pos']) == '-':
                            golfer['pos'] = 0
                        else:
                            golfer['pos'] = int(str(competitor['pos']).strip("T"))
                    except:
                        golfer['pos'] = 1000
                        golfer['overall'] = "OUT"
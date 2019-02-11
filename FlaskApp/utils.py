from golfers import golfers
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

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
        html = self.simple_get('https://www.golfchannel.com/tours/pga-tour/2018/pga-championship/')
        contents = BeautifulSoup(html, 'html.parser')
        
        # Let's extract all of the player names and positions
        names = contents.find_all("a", class_="pName")
        positions = contents.find_all("td", class_="pos")
        overall = contents.find_all("td", class_="darkBlueGrad")
        
        # Now we simply loop over our names list,
        # see if name is in our golfers dictionary, 
        # and set his/her position key
        for name in range(0, len(names)):
            for golfer in golfers:
                if golfer['name'] in str(names[name]):
                    try:
                        golfer['pos'] = int(str(positions[name])[16:-5].strip("T"))
                        golfer['overall'] = str(overall[name])[25:-5]
                    except:
                        golfer['pos'] = 1000
                        golfer['overall'] = "OUT"
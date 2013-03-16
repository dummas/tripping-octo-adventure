from lxml.html import fromstring
from lxml.html import submit_form
import urlparse
import urllib
import urllib2


class card_information():
    """
    Card information parser
    """

    def __init__(self, _username='', _password=''):
        """
        Initialization of the library
        """
        self.username = _username
        self.password = _password
        self.root_url = 'https://e.vilniusticket.lt/'
        self.login_page = self.root_url
        self.post_data = '__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDw\
UENTM4MQ9kFgJmD2QWBAIBD2QWBmYPFgIeB1Zpc2libGVnFgQCAQ8PFgIeBFRleHQFCUxp\
ZXR1dmnFs2RkAgMPFgIeC18hSXRlbUNvdW50AgEWAgIBD2QWAmYPFQIVL0RlZmF1bHQuYX\
NweD9sYW5nPWx0CUxpZXR1dmnFs2QCAQ9kFgICCA9kFgICAg8PFgIeBENvZGUCwNbFggZk\
FgICAQ8PFggeBVdpZHRoGwAAAAAAAGlAAQAAAB4GSGVpZ2h0GwAAAAAAAElAAQAAAB4ISW\
1hZ2VVcmwFLkh1bWFuRmlsdGVySW1hZ2VHZW5lcmF0b3IuYXNweD9Db2RlPTE2MTU5NDg2\
MDgeBF8hU0ICgANkZAIEDxYCHwICAxYGAgEPZBYCZg8VAjNodHRwczovL2Uudmlsbml1c3\
RpY2tldC5sdC9ob3dfdG9fYmVjb21lX2NsaWVudC5odG0TSG93IHRvIGJlY29tZSB1c2Vy\
P2QCAw9kFgJmDxUCL2h0dHBzOi8vZS52aWxuaXVzdGlja2V0Lmx0L3Rlcm1zX29mX3Nlcn\
ZpY2UuaHRtEFRlcm1zIE9mIFNlcnZpY2VkAgUPZBYCZg8VAidodHRwczovL2Uudmlsbml1\
c3RpY2tldC5sdC9jb250YWN0cy5odG0HQ29udGFjdGQCAg9kFgJmDxYEHwEF%2BQM8c2Ny\
aXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCI%2BDQp2YXIgZ2FKc0hvc3QgPSAoKCJodHRw\
czoiID09IGRvY3VtZW50LmxvY2F0aW9uLnByb3RvY29sKSA%2FICJodHRwczovL3NzbC4i\
IDogImh0dHA6Ly93d3cuIik7DQpkb2N1bWVudC53cml0ZSh1bmVzY2FwZSgiJTNDc2NyaX\
B0IHNyYz0nIiArIGdhSnNIb3N0ICsgImdvb2dsZS1hbmFseXRpY3MuY29tL2dhLmpzJyB0\
eXBlPSd0ZXh0L2phdmFzY3JpcHQnJTNFJTNDL3NjcmlwdCUzRSIpKTsNCjwvc2NyaXB0Pg\
0KPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiPg0KdHJ5IHsNCnZhciBwYWdlVHJh\
Y2tlciA9IF9nYXQuX2dldFRyYWNrZXIoIlVBLTU1OTQ3MDUtOSIpOw0KcGFnZVRyYWNrZX\
IuX3RyYWNrUGFnZXZpZXcoKTsNCnZhciB2ZXJzaW9uID0gZ2V0U2lsdmVybGlnaHRWZXJz\
aW9uKCk7DQppZiAodmVyc2lvbikgeyBwYWdlVHJhY2tlci5fc2V0VmFyKHZlcnNpb24pOy\
B9DQp9IGNhdGNoIChlcnIpIHsgfTwvc2NyaXB0Pg0KHwBnZBgBBR5fX0NvbnRyb2xzUmVx\
dWlyZVBvc3RCYWNrS2V5X18WAQUYY3RsMDAkUGVyc2lzdGVudENoZWNrQm94s2eLlIXEgY\
zuYWcdzvUSMNSmVIRFUncLj1asW11FqRQ%3D&ctl00%24\
LoginTextBox=' + urllib.quote_plus(self.username) + '&ctl00%24PwdText\
Box=' + urllib.quote_plus(self.password) + '&ctl00%24\
LoginButton=Sign+in&ctl00%24EmailTextBox=&ctl00%24C\
    onfirmEmailTextBox=&ctl00%24RegPasswordTextBox=&ctl00%24SNRTextBox='
        """
        No idea what this all __VIEWSTATE is and why is it so long, but it
        looks like key-ish thing and important peace of information to process
        the login happen
        """

        self.open_http = self.make_open_http()

    def main(self):
        """
        The guider of the universe
        """
        pass

    def url_with_query(self, url, values):
        """
        url parser
        """
        parts = urlparse.urlparse(url)
        rest, (query, frag) = parts[:-2], parts[-2:]
        return urlparse.urlunparse(rest + (urllib.urlencode(values), None))

    def make_open_http(self):
        """
        Makes the http open happen

        Data is encoded already, so there is not need to do the encoding again
        """
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        opener.addheaders = []  # Hacking

        def open_http(method, url, values={}):
            if method == "POST":
                # return opener.open(url, urllib.urlencode(values))
                return opener.open(url, values)
            else:
                return opener.open(self.url_with_query(url, values))

        return open_http

    def go(self, page):
        """
        Method to go to the page
        """
        self.html = fromstring(
            self.open_http("GET", self.root_url + page).read())
        self.current_url = self.root_url + page

    def login(self):
        """
        Make the login happen

        Immediately send a form data, don't bother with form submission,
        everything goes through the JavaScript, so nothing fancy happens
        """
        self.html = fromstring(
            self.open_http("POST", self.login_page, self.post_data).read())

        print self.html.text_content()
        print self.post_data

if __name__ == '__main__':
    ci = card_information('email', 'password')
    ci.login()

import logging

from mills import get_request
from mills import get_redirect_url


from bs4 import BeautifulSoup

def scraw():

    url = "https://sec.today/pulses/"
    r = get_request(url)
    if r:
        try:
            soup = BeautifulSoup(r.content, 'lxml')

        except Exception as e:
            logging.error("GET %s  failed : %s" % (url, repr(e)))
            return
        if soup:
            pass


if __name__ == "__main__":
    scraw()
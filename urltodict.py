import requests     # to get the web page from the url.
from bs4 import BeautifulSoup  # to analyze the html of the web page.
import time     # to identify which parts of our code are slowing it down.
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit, SplitResult    # (SEE BELOW)
# parse_qs converts the query string to a dictionary (so we can change the page number).
# urlencode converts dictionary back to query strings.
import furl
# furl library allows us to read query strings quickly and accurately. docs here: https://github.com/gruns/furl/blob/master/API.md


# class containing all the websites we can extract text from, so far.
class URLtoDict:
    """
    Can convert multiple dictionary websites into array dictionaries.
    """
    def readURL(self, url):
        """NOT PROGRAMMED YET: Uses database of dictionaries to match url to the appropriate function"""
        pass

    # PUBLIC
    def xraybmc(self, url):
        """Returns transcript data specifically from 'http://xray.bmc.uu.se/Courses/Dictionaries/Glossary.html"""
        if self.exists(url):
            # requesting page & retrieving html
            page = requests.get(url).text
            html = BeautifulSoup(page, "lxml")  # turn it into a soup object so you can use .find_all method on it.

            # getting data from page's html
            words = [b.text for b in html.find_all('b')]    # takes out bolded text only: thank this website for being so simple!

            # bolded text (word declaration) is considered part of <p> elements which contain their definitions.
            # without this step, definitions will include the word!
            for h2 in html.find_all('b'):
                h2.decompose()
            defs = [p.text for p in html.find_all('p')]

            # WARNING: hardcoded.
            for i in range(2):  # remove the first two paragraphs from defs, because they are not definitions.
                defs.pop(0)

            # initializing dictionary
            worddict = {}

            # adding words and defs to dictionary.
            if len(words) == len(defs):
                for i, word in enumerate(words):
                    this_def = defs[i].replace("\n", '')[2:]    # formatting
                    worddict[word] = this_def
            else:
                Exception("URLtoTranscript.xraybmc ERROR: len(words) != len(defs).")

            print(url)
            return url, worddict


    def wiktionary(self, url, lang):
        """Returns transcript data specifically from wiktionary dictionaries at https://en.wiktionary.org/wiki/Category:List_of_topics
        In given lang only.
        url should end in Category:topic"""
        pass


    def oxfordreference(self, url):
        """Returns transcript data specifically from oxfordreference dictionaries at https://www.oxfordreference.com/"""
        # defining the query dictionary
        if self.exists(url):
            template_url, template_qs = self.getQueryString('https://www.oxfordreference.com/view/10.1093/acref/9780198802525.001.0001/acref-9780198802525?btog=chap&hide=true&page=2&pageSize=20&skipEditions=true&sort=titlesort&source=%2F10.1093%2Facref%2F9780198802525.001.0001%2Facref-9780198802525')
            # ^^^ hard-coded url from oxfordreference.com, defines the variables of ALL oxfordreference query strings.
            # print("template_url = ", template_url)
            # print("template_qs = ", template_qs)

            query_dict = parse_qs(str(template_qs))
            # print("query_dict =", query_dict)

            # separating url and any query string
            base_url, qs = self.getQueryString(url)   # base_url = url without query, q_string = query string
            # print("base_url = ", base_url)

            # URL check
            # if base_url != template_url:
                # Exception("URLtoTranscript.oxfordreference() ERROR: inputted URL is not from oxfordreference.com")
                # return None

            # determining how many times we have to switch pages
            last_page = self.oxfordLastPage(url)
            words = []

            # reading each page:
            for page in range(1, last_page+1):     # page = 1-last_page
                start_time = time.time()    # so we can measure the time of each iteration.

                # changing query string to turn to the right page:
                print("page = " + str(page) + "/" + str(last_page))
                query_dict['page'] = page
                current_qs = urlencode(query_dict)  # current query string
                current_url = base_url + '?' + current_qs   # current url with the right pageNo
                print("current_url = ", current_url)

                # getting page:
                html = requests.get(current_url).text   # this line is causing our code to run slower.
                soup = BeautifulSoup(html, "lxml")

                # getting words:
                # Each word is contained in <h2> tags, which are nested in separate <div>s.
                # All these divs containing words are held in the parent, <div id=searchContent>.
                searchContent = soup.find(id="searchContent")
                print("searchContent type, page, current_url = ", str(type(searchContent)) + ", " + str(page) + ", " + current_url)
                wordList = searchContent.find_all('div')
                for div in wordList:
                    h2 = div.find('h2').text.replace('\n', '')
                    words.append(h2)
                print("time elapsed: {:.2f}s".format(time.time() - start_time))
        return url, words

    # PRIVATE
    def oxfordLastPage(self, url):
        """returns an integer value for the last page number (i.e. 1050 pages, returns 1050)"""
        page = requests.get(url).text
        soup = BeautifulSoup(page, "lxml")
        number_grid = soup.find(class_='t-data-grid-pager')     # WARNING: This class may repeat itself, be careful.
        page_numbers = [p.text for p in number_grid.find_all('a')]
        last_page = int(page_numbers[-1])
        return last_page


    def exists(self, url):
        """Checking if url exists"""
        request = requests.get(url)
        if request.status_code != 200:
            Exception('URLtoTranscript().getQueryString() ERROR: url parameter does not exist.')
            return False
        return True


    def getQueryString(self, url):
        """ Making the assumption that ? or # is nowhere else in the url. """
        # extracting query string
        qs = furl.furl(url).query

        # extracting base_url. We only want split_url.scheme + split_url.netloc
        split_url = urlsplit(url)   # returns a SplitResult() object that we can pass through urlunsplit.
        new_url = SplitResult(scheme=split_url.scheme, netloc=split_url.netloc, path=split_url.path, query='', fragment='')
        base_url = urlunsplit(new_url)

        return base_url, qs


if __name__ == "main":
    pass

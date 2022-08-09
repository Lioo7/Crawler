# allow us to connect to web pages form Python
from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:
    # class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    # the waiting list (SSD)
    queue_file = ''
    # the pages that we crawled (SSD)
    crawled_file = ''
    # the waiting list (RAM)
    queue = set()
    # the pages that we crawled (RAM)
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        print('boot')
        self.boot()
        print('crawl_page')
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        # checks if any spider did not already crawl this page
        if page_url not in Spider.crawled:
            print(thread_name + ' is now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.queue)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            # remove the uel from the queue and add it to the crawled
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            # converts the sets to files to save the data
            Spider.update_files()

    # crawl the page and return a set of links
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            # makes a connection to the url and stores the response
            response = urlopen(page_url)
            # makes sure that we're connecting to actual webpage
            # if response.getheader('Content-Type') == 'text/html':
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                # converts the data from binary to HTML string
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            # parse the HTML data and return all the links  on the current url
            finder.feed(html_string)

        except:
            print('Error: can not crawl page')
            # if there is no access to the server, then return an empty set
            return set()

        # returns all the url links that the spider found on this page
        return finder.page_links()

    # the function gets a set of links and adds it to an existing waiting list
    @staticmethod
    def add_links_to_queue(links):
        # the condition of domain name in url assure that the spider will
        # add only links from our website
        for url in links:
            if url not in Spider.queue and url not in Spider.crawled \
                    and Spider.domain_name in url:
                Spider.queue.add(url)

    # The function saves the data to files
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
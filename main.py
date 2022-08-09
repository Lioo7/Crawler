import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

"""
The program creates a bunch of spiders (workers) and then it creates
a bunch of jobs (links to crawl).
The spiders will continue crawling as long as there are items in the queue.
"""


# PROJECT_NAME = 'coursera'
# HOME_PAGE = 'https://www.coursera.org/'
# DOMAIN_NAIM = get_domain_name(HOME_PAGE)
# QUEUE_FILE = PROJECT_NAME + '/queue.txt'
# CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
# NUMBER_OF_THREADS = 8
# threads_queue = Queue()
# # calls the first spider on the home page
# Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAIM)


# create spider (worker) threads (will die when main exits)
def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        print('Creating Spider #' + str(_+2))
        thread = threading.Thread(target=work)
        # will die when main exits
        thread.daemon = True
        thread.start()


# do the next job in the queue
def work():
    while True:
        # get the next item (url) from the queue
        url = threads_queue.get()
        # the given url will be crawled by the current thread
        Spider.crawl_page(threading.current_thread().name, url)
        # when the spider is done, he informs the OS that he is ready to work on the next job
        threads_queue.task_done()


# each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        threads_queue.put(link)
    # block the main thread until all the tasks in the queue have been processed
    threads_queue.join()
    crawl()


# check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


if __name__ == '__main__':
    PROJECT_NAME = input('Enter the project name: ')
    HOME_PAGE = input('Enter the URL: ')
    DOMAIN_NAIM = get_domain_name(HOME_PAGE)
    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
    NUMBER_OF_THREADS = 8
    threads_queue = Queue()
    print('Start crawling...')
    # calls the first spider on the home page
    print('Creating Spider #1')
    Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAIM)

    # creates our spiders
    print('Create_spiders')
    create_spiders()
    # creates our jobs (links to crawl)
    print('Creates jobs (links to crawl)')
    crawl()

import threading
from collections import Counter
from queue import Queue
from links_finder import LinksFinder
from words_finder import WordsFinder
from links_storage import *


# All spiders crawls their given website_url in parallel so we make our own implementation of threading.Thread
class Spider (threading.Thread):
    name = ''
    website_name = ''
    website_url = ''
    full_info_crawling = None
    crawl_only_current_url = None
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    dictionary = dict()
    sentences = list()
    pages_queue = Queue()

    def __init__(self, name, website_name, website_url, crawl_only_current_url):
        threading.Thread.__init__(self)
        self.name = name
        self.website_name = website_name
        self.website_url = website_url
        self.crawl_only_current_url = crawl_only_current_url
        self.queue_file = self.website_name + '/queue.txt'
        self.crawled_file = self.website_name + '/crawled.txt'
        self.boot()
        self.crawl_page(self.name, self.website_url)

    # Overriding run() from threading.Thread to tell the spider what to do
    # The spider stops when there are no links in the queue
    def run(self):
        try:
            if self.crawl_only_current_url:
                pass
            else:
                while True:
                    for link in file_to_set(self.queue_file):
                        self.pages_queue.put(link)
                        self.crawl_page(self.name, link)
                    if len(self.queue) == 0:
                        break
        except Exception:
            pass

    # Creates directory and files for current website on first run and starts the spider
    def boot(self):
        create_website_directory(self.website_name)
        create_data_files(self.website_name, self.website_url)
        self.queue = file_to_set(self.queue_file)
        self.crawled = file_to_set(self.crawled_file)

    # Updates user display, fills queue, removes crawled links from the queue, adds each web page words into the
    # Spider.dictionary which is the dictionary of all spiders which are crawling at the moment and updates files
    # of the current website directory
    def crawl_page(self, spider_name, page_url):
        if page_url not in self.crawled:
            print(spider_name + ' crawling ' + page_url)
            print('Queue ' + str(len(self.queue)) + ' | crawled ' + str(len(self.crawled)))
            links = LinksFinder(self.website_url, page_url)
            words = WordsFinder(page_url)
            temp_dictionary = words.get_words()
            Spider.sentences.extend(words.found_sentences)
            self.add_links_to_queue(links.get_links())
            for w in temp_dictionary:
                if w == self.website_name:
                    continue
                else:
                    if w not in Spider.dictionary:
                        Spider.dictionary[w] = temp_dictionary[w]
                    else:
                        Spider.dictionary[w] += temp_dictionary[w]
            self.queue.remove(page_url)
            self.crawled.add(page_url)
            self.update_files()

    # Saves queue data to project files
    def add_links_to_queue(self, links):
        for url in links:
            if (url in self.queue) or (url in self.crawled):
                continue
            self.queue.add(url)

    # update queue.txt and crawled.txt files for the current website
    def update_files(self):
        set_to_file(self.queue, self.queue_file)
        set_to_file(self.crawled, self.crawled_file)

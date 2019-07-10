import re
import requests
from bs4 import BeautifulSoup


class WordsFinder:

    found_sentences = []

    def __init__(self, page_url):
        self.page_url = page_url

    # Function sends request to the page_url of the base_url website, it takes the source code of the web page
    # With BeautifulSoup library we are pulling the <p> tags from the page and then we split text to separate words
    def get_words(self):
        list_of_words = []
        source_code = requests.get(self.page_url).text
        soup = BeautifulSoup(source_code, 'html.parser')
        for each_text in soup.findAll('p'):
            content = each_text.text
            sentences = content.split('.')
            words = content.lower().split()
            for sentence in sentences:
                self.found_sentences.append(sentence)
            for each_word in words:
                list_of_words.append(each_word)
        clean_list = WordsFinder.clean_list_of_words(list_of_words)
        return WordsFinder.create_dictionary(clean_list)

    # Function removes any unwanted symbols and commonly used words from list_of_words which we pull from the current
    # page_url
    @staticmethod
    def clean_list_of_words(list_of_words):
        clean_list = []
        common_words = WordsFinder.fill_with_common_words()
        for word in list_of_words:
            if re.match('^[a-zA-Z]+$', word):
                for i in range(0, len(common_words)):
                    if word == common_words[i]:
                        word = word.replace(word, '')
                if len(word) > 2:
                    clean_list.append(word)
        return clean_list

    # Read the file common_words.txt and load the information in list
    @staticmethod
    def fill_with_common_words():
        file_common_words = open('common_words.txt', 'r')
        common_words = file_common_words.read().split('\n')
        return common_words

    # Creates a dictionary containing each word's count
    @staticmethod
    def create_dictionary(clean_list):
        word_count = dict()
        for word in clean_list:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        return word_count

from spider import Spider
from collections import Counter

crawl_only_current_url = True  # this is to set spider to crawl only the current url


# creating 5 different spiders(threads) and starting each of them to crawl only the current website url
def create_spiders():
    first_spider = Spider('Spider-1', 'the guardian', 'https://www.theguardian.com/world/2019/jul/09/glacial-melting-in-antarctica-may-become-irreversible', crawl_only_current_url)
    second_spider = Spider('Spider-2', 'new york times', 'https://www.nytimes.com/2019/07/10/world/americas/venezuela-shipwreck.html', crawl_only_current_url)
    third_spider = Spider('Spider-3', 'bbc', 'https://www.bbc.com/news/uk-48937120', crawl_only_current_url)
    forth_spider = Spider('Spider-4', 'buzzfeed', 'https://www.buzzfeednews.com/article/albertonardelli/salvini-russia-oil-deal-secret-recording?ref=bfnsplash', crawl_only_current_url)
    fifth_spider = Spider('Spider-5', 'reuters', 'https://www.reuters.com/article/us-usa-fed-powell/fed-chief-likely-to-focus-on-trade-inspired-policy-shift-in-testimony-idUSKCN1U50DT', crawl_only_current_url)

    first_spider.start()
    second_spider.start()
    third_spider.start()
    forth_spider.start()
    fifth_spider.start()


create_spiders()
c = Counter(Spider.dictionary)
top = c.most_common(5)
print(top)
top = dict(top)
for w in top:
    for sentence in Spider.sentences:
        words_from_sentence = sentence.lower().split()
        if w in words_from_sentence:
            print(sentence)
            Spider.sentences.remove(sentence)
            break

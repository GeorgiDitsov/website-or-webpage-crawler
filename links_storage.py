import os


# Each website has a separate folder where are stored two files: queue.txt and crawled.txt
# In the queue.txt file we have all links which the spider found and have to be crawled
# In the crawled.txt file we have all crawled links from this site
def create_website_directory(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(website_name, base_url):
    queue = website_name + '/queue.txt'
    crawled = website_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Create a new file
def write_file(path, website_url):
    f = open(path, 'w')
    f.write(website_url)
    f.close()


# Add data onto an existing file
def append_to_file(path, website_url):
    f = open(path, 'a')
    f.write(website_url + '\n')
    f.close()


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    f = open(file_name, 'rt')
    for line in f:
        results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(web_page_links, file_name):
    delete_file_contents(file_name)
    for link in sorted(web_page_links):
        append_to_file(file_name, link)

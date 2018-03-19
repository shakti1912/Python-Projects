#You have to find the unique list of the names of the total people who are annotated in the captions of the photos
# from the parties before December 1st, 2014.

# get the data and pickle it

# Steps to do
# provide page=0 link
# go to all links, check date, and then scrape if before dec 1, 2014
# after scraping, go to next link if there otherwise end scraping

# do parsing names and count them
import re
from datetime import datetime
from datetime import date
from datetime import time

import pickle
from bs4 import BeautifulSoup
import requests
import parser

url = "http://www.newyorksocialdiary.com/party-pictures?page=6"
default_url = "http://www.newyorksocialdiary.com"
req_date = datetime(2014, 12, 1)
pickle_out = open('data.p', 'w')

entire_name_set = set()

#
def get_view_content_pager_list(given_url):
    markup = requests.get(given_url)
    soup = BeautifulSoup(markup.text, 'html.parser')
    links = soup.find_all('div', attrs={'class': 'views-row'})

    pagers = soup.find_all('li', attrs={'class':'pager__item'})
    return (links, pagers)
    #print links[0].next.next.next.get('href')
    #pagers = soup.find_all('li', attrs={'class': 'pager__item'})
    #print pagers


# get all scrape info and pickle here
def scrape_all_links(links):

    for link in links:
        #print link.next.next.next.next.next
        page_url = default_url + (link.find('a').get('href')).encode('utf8')

        pick_d = scrape_current_page(page_url)
        if type(pick_d[page_url]) ==  list:

        # print pick_d[page_url]
        #pickle(serialize) here
        #pickle_out = open('data.pickle')
            #pickle.dump(pick_d, pickle_out)

            s = parser.parse_names(pick_d[page_url])
            entire_name_set.add(s)

    pickle_out.close()





#scrapes current page and save data.
# check date and scrape if before dec 1, 2014
def scrape_current_page(link):
    pickle_dict = {link:[]}
    markup = requests.get(link)
    soup = BeautifulSoup(markup.text, 'html.parser')
    if len(soup.find_all('div', attrs={'class': 'pane-node-created'})) == 0:
        print "Date is not provided at the top of the page"
        return pickle_dict
    date = soup.find_all('div', attrs={'class': 'pane-node-created'})[0].text.strip().encode('utf8') # need 0 because it is a resultSet
    page_date = datetime.strptime(date, '%A, %B %d, %Y')
    #return 0
    print page_date.strftime('%A, %B %d, %Y')
    if page_date <= req_date: #scrape if page_date is less than or equal to req_date else skip

        labels = (soup.find_all('div', attrs={'class': 'photocaption' }))

        for label in labels:
            label_str = (label.text).encode('utf8').strip()

            pickle_dict[link].append(label_str)

        # cases where div class='photocaption' is not working. Pages that are in 2007
        if len(pickle_dict[link]) <= 1:
            labels = soup.find_all('font', attrs={'face': 'Verdana, Arial, Helvetica, sans-serif'})
            for label in labels:
                label_str = (label.text).encode('utf8').strip()

                pickle_dict[link].append(label_str)

    else:
        #print "Date is greater than required date"
        pickle_dict[link] = "Date is greater than required date: " + page_date.strftime('%A, %B %d, %Y')


    print pickle_dict
    return pickle_dict


# gives next navigation link to go or None if no next link is available
def find_next_link(pagers):
    for page in pagers:
        next_url = None
        s = page.encode('utf8')
        if 'next' in s:
            next_url = default_url + page.next.get('href')
            return next_url
    return next_url


def main(given_url):
    next_url = given_url
    while next_url is not None:
        links, pagers = get_view_content_pager_list(next_url)
        scrape_all_links(links)
        next_url = find_next_link(pagers)

        print next_url
    print "This is last done"
    print entire_name_set


if __name__ == '__main__':
    main(url)




#
# markup = requests.get(url)
#
# soup = BeautifulSoup(markup.text, 'html.parser')
# links = soup.find_all('div', attrs={'class':'view-content'})
# print links
#
# pagers = soup.find_all('li', attrs={'class':'pager__item'})

#print pagers
# print len(pagers)
#
# for page in pagers:
#     s = page.encode('utf8')
#
#     if 'next' in s:
#         print page.next
#         print page.next.get('href')
#         next_url = default_url + page.next.get('href')
#         print next_url

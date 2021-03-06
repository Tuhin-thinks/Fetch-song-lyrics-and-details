import sys
import urllib.parse
import requests
from bs4 import BeautifulSoup


def search_for_eligibility(url, page_list):
    # print('url:', url)
    for page in page_list:
        # print('\tPage:', page)
        if page.lower() in url.lower():
            if 'https://' in url[1:]:
                break
            else:
                # print('--True and Url--')
                return page, True
        else:
            return '', False
    return '', False


def main():
    domain = ''
    # get the song name from user input
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    search = input('Enter song name:') + ' song details and lyrics'
    url = 'https://google.com/search?' + urllib.parse.urlencode({'q': search})
    print('searching url:', url)

    # Making the website believe that you are accessing it using a mozilla browser
    # req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-In,en'})
    web_page = requests.get(url, headers)

    # data is a list of the html code content from the web_page
    data = web_page.content
    soup = BeautifulSoup(data, 'html5lib')  # decoding the data into html format
    print(web_page.status_code)  # this is to confirm if the link allows scraping!

    link_list = []  # a list containing all the links for the search
    link = soup.find_all('div')

    for result in link:
        link = result.find('a', href=True)
        if link:
            link_mod = link['href']  # getting only the hyperlink portion of the attribute
            try:
                if link_mod[link_mod.index('=') + 1:link_mod.index('&')].startswith('https://'):
                    final_link = link_mod[link_mod.index('=') + 1:link_mod.index('&')]
                    if final_link not in link_list and final_link is not None:  # condition to prevent repetition
                        link_list.append(final_link)  # storing valid link in a list
            except ValueError:
                pass  # for ValueError simply skip the step

    flag = 0
    count = 0
    number = 0
    fin_list = []
    domain_list = []
    print('\n'.join(link_list))
    print('Enter Pages you want to search (separated by commas):')
    pages = input().split(',')
    for number, link in enumerate(link_list):
        domain, response = search_for_eligibility(link, pages)
        if response:  # to get links that are only from given sites
            flag = 1
            count += 1
            print(count, '.', link)
            fin_list.append(link)
            domain_list.append(domain)
        else:
            pass
    print(domain)
    if flag == 0:
        print('No songs found with this name!')
        if len(fin_list) > 0:
            print('you can also search from these links:', link_list)
    else:
        del link_list
        print(f'\nSearched {number + 1} link(s), found {count} link(s) valuable.')
        number = int(input('Enter the link you want to choose:'))
        if number > len(fin_list)+1:
            print('Wrong number entered!')
            sys.exit(0)
        print(fin_list[number-1])
        return fin_list[number-1], domain_list[number-1]  # returns first link and it's domain

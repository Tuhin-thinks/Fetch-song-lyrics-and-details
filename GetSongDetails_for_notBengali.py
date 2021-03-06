import shutil
import os
import scrap_google_search_links_practice
import requests
from bs4 import BeautifulSoup

from modules.search import PatternFinder

url = ''


def write_in_file(file_path, note_line):
    with open(file_path, 'a') as file_01:
        file_01.write(note_line)


def find_details(write_perm):
    global url
    # if 'genius.com' in url:
    #     find_details_(write_perm)
    #     return

    cwd = os.getcwd()
    file_path = os.getcwd()
    folder_name = url.split('/')[-1].strip().strip('\n')  # create name of folder to store details

    write_folder = os.path.join(cwd, folder_name)

    if write_perm and os.path.exists(write_folder) is False:
        os.mkdir(folder_name)
        file_path = os.path.join(write_folder, 'song_lyrics_and_details.txt')
    elif write_perm and os.path.exists(write_folder) is True:
        shutil.rmtree(write_folder)
        os.mkdir(folder_name)
        file_path = os.path.join(write_folder, 'song_lyrics_and_details.txt')

    p = PatternFinder(url=url, pattern_to_search='div', x=10)
    match_ = p.find_match(auto_purify=True, save_raw=False)
    if match_:
        p.save_(text=match_, filename=file_path)
    else:
        print("No song details found. for url:"+url)


def find_details_(write_perm):  # gets the write permission
    # to fool the web page by emulating search request as from fire-fox browser
    global url
    file_path = ''
    cwd = os.getcwd()
    folder_name = url.split('/')[-1].strip().strip('\n')  # create name of folder to store details

    if write_perm and os.path.exists(cwd + '/' + folder_name) is False:
        os.mkdir(folder_name)
        file_path = cwd + '/' + folder_name + '/' + 'song_lyrics_and_details.txt'

    headers = {"Accept-Language": "en-US,en;q=0.5", "User-Agent": "Mozilla/5.0"}
    web_page = requests.get(url, headers)

    # Creating a BeautifulSoup object of the html page for easy extraction of data.
    data = web_page.content  # this is the body of the website in list format
    soup = BeautifulSoup(data, 'html5lib')  # parsing the data using html5lib

    # getting the title of the song
    try:
        title = soup.find_all('title')[0].text.strip('\n').strip(' ')
        print(f'-----> SONG TITLE :{title}\n')
        if write_perm:
            write_in_file(file_path, f'-----> SONG TITLE :{title}\n')
    except:
        print('x x x x x Skipped due to "Not Found/Improper formatting"  x x x x x')
        if write_perm:
            write_in_file(file_path, '\nx x x x Cannot write Due to Poor Formatting x x x\n')

    # getting the release date of the song
    print(16 * '--', 'Release Year', 16 * '--')
    if write_perm:
        write_in_file(file_path, f'{16 * "--"} Release Year {16 * "--"}\n')
    try:
        release = soup.find_all('span', attrs={'class': 'metadata_unit-info metadata_unit-info--text_only'})
        print(f'{release[0].text}')

        if write_perm:
            write_in_file(file_path, f'{release[0].text}\n')
    except:
        print('x x x x x Skipped due to "Not Found/Improper formatting"  x x x x x')
        if write_perm:
            write_in_file(file_path, '\nx x x x Cannot write Due to Poor Formatting x x x\n')

    # getting about of the song
    print(16 * '--', 'About the song', 16 * '--')
    if write_perm:
        write_in_file(file_path, f'{16 * "--"} About the song {16 * "--"}\n')
    try:
        about_data = soup.find_all('div', attrs={'class': 'rich_text_formatting'})
        for data in about_data:
            about = data.find('p')
            print(about.text)

            if write_perm:
                write_in_file(file_path, about.text)
    except:
        print('x x x x x Skipped due to "Not Found/Improper formatting"  x x x x x')
        if write_perm:
            write_in_file(file_path, '\nx x x x Cannot write Due to Poor Formatting x x x\n')

    print('\n', 16 * '--', 'Lyrics', 16 * '--')  # for creating a nice formatting for display
    if write_perm:
        write_in_file(file_path, f'\n{16 * "--"} Lyrics {16 * "--"}\n')
    # getting the lyrics of the song
    lyrics = soup.find_all('div', {'class': 'lyrics'})
    for line in lyrics:
        print(line.text.strip('\n'))
        if write_perm:
            write_in_file(file_path, line.text)


def main(web_link, save_details):
    global url
    url = web_link
    print('searching url:', url)
    find_details(save_details)


if __name__ == '__main__':
    # url = 'https://genius.com/Dj-snake-let-me-love-you-lyrics'
    url, domain = scrap_google_search_links_practice.main()
    response = input('want to save the details ? (y/n)')

    if response != 'n' and response != 'no':
        response = True
    else:
        response = False
    print(f'----> Sending save permission as {response}.')
    main(url, save_details=response)

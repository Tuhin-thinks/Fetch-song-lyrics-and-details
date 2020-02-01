import sys
import os
import requests
from bs4 import BeautifulSoup
import scrap_google_search_links_practice
write_perm = ''
file_path = ''


def write_in_file(file_path, note_line):
    with open(file_path, 'a') as file_01:
        file_01.write(note_line)


def gdn8(beng):
    # support for gdn8.com
    deactivate = False
    global write_perm, file_path

    for data in beng:
        text = data.text
        if 'Tags' in text:
            deactivate = True
        if not deactivate:
            print(text)
            if write_perm:
                write_in_file(file_path, text+'\n')  # write the lyrics


def jiosaavn(beng):
    global write_perm
    global file_path
    for data in beng:
        print(data.text)  # this will print all lyrics and details
        if write_perm:
            write_in_file(file_path, data.text+'\n')  # write the lyrics


def main(url, domain, permission):
    global file_path, write_perm
    write_perm = permission
    header = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-In,en'}
    webpage = requests.get(url, header)
    soup = BeautifulSoup(webpage.content, 'html5lib')
    if 'jiosaavn' in domain:
        folder_name = url.split('/')[-2].strip().strip('\n')
    else:
        folder_name = url.split('/')[-1].strip().strip('\n')
    cwd = os.getcwd()

    if os.path.exists(cwd + '/' + folder_name) is False and write_perm:
        os.mkdir(cwd + '/' + folder_name)
    file_path = cwd + '/' + folder_name + '/' + 'song_lyrics_and_details.txt'
    # print(soup.prettify())

    if 'jiosaavn' in domain:
        # support for jiosaavn.com
        beng = soup.find_all('div')  # , attrs={'class': 'meta-list'})
        note = f'{16*"--"} About song {16*"--"}\n'
        if write_perm:
            write_in_file(file_path, note)  # about song header

        for number, data in enumerate(beng):
            if 35 <= number <= 40 and number % 2 == 0:
                now = data.text
                now = '\n'.join([word.strip() for word in now.strip('\n').split('\n')])
                print(now)
                if write_perm:
                    write_in_file(file_path, now.strip('')+'\n')  # write the song about's

        for br in soup.find_all('br'):
            br.replace_with('\n' + br.text)
        print(f'\n{16*"--"}Searching in jiosaavn!{16*"--"}')
        if write_perm:
            note = f'{16 * "--"} Lyrics {16 * "--"}\n'
            write_in_file(file_path, note)  # about song lyrics
        lyrics_data = soup.find_all('p', attrs={'class', 'lyrics'})
        jiosaavn(lyrics_data)

    elif 'gdn8' == domain:
        # support for gdn8
        print('Searching in gdn8!')
        beng = soup.find_all('span')
        gdn8(beng)


# main('https://www.jiosaavn.com/lyrics/chirodini-tumi-je-aamar-male-version-lyrics/HRguZEEEbh4', 'jiosaavn',
# write_perm=False)
url, domain = scrap_google_search_links_practice.main()
if url is not None:
    response = input('Do you want to save song details? (y/n)')
    if response != 'n' and response != 'no':
        response = True
    elif response == 'n' or response == 'no':
        response = False
    else:
        print('Wrong Response!')
        sys.exit(0)
    main(url, domain, permission=response)
else:
    print('Nothing Found!')

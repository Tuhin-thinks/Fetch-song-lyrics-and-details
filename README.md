# Fetch-song-lyrics-and-details
## Used to fetch lyrics(mainly) of almost any song available on INTERNET, using Python code
Packages Used:
- BeautifulSoup
- requests
- json
- ast
- ssl
- urllib

## Working Of the Program:

You have to run the [GetSongDetails_for_notBengali.py](https://github.com/Tuhin-thinks/Fetch-song-lyrics-and-details/blob/master/GetSongDetails_for_notBengali.py) or the [bengali_lyrics.py](https://github.com/Tuhin-thinks/Fetch-song-lyrics-and-details/blob/master/bengali_lyrics.py)
In both the cases the control triggers the [scrap_google_search_links_practice.py](https://github.com/Tuhin-thinks/Fetch-song-lyrics-and-details/blob/master/scrap_google_search_links_practice.py)
the [scrap_google_search_links_practice.py](https://github.com/Tuhin-thinks/Fetch-song-lyrics-and-details/blob/master/scrap_google_search_links_practice.py) simluates human searching on a normal google search page.

I have pre-define scraping techniques for some websites inside the code, like for:
- jiosaavvn
- genius.com
- gdn8.com

And thanks to the huge repository of genius.com, most of the songs are available from their website.
Jiosaavn for india specific songs and old songs.
Though this is not the final version.

I will be upgrading it for more websites to fetch lyrics for more websites.

## EXample:

You'll have to enter some <songname> genius.com then you'll be guided by the program till the last step to finally save the lyrics in a text file.

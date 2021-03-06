import os
import logging
import re
import random

import requests
from bs4 import BeautifulSoup

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PatternFinder:
    headers = [
        {"Accept-Language": "en-US,en;q=0.5", "User-Agent": "Mozilla/5.0"},

        {"Accept-Language": "en-US,en;q=0.5",
         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0", "Accept": "text/html"},

        {"Accept-Language": "en-US,en;q=0.5",
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134", "Accept": "text/html"},

        {"Accept-Language": "en-US,en;q=0.5",
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/74.0.3729.169 Safari/537.36", "Accept": "text/html"},

        {"Accept-Language": "en-US,en;q=0.5",
         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                       "like Gecko) Mobile/15E148", "Accept": "text/html"},

        {"Accept-Language": "en-US,en;q=0.5",
         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 "
                       "(KHTML, like Gecko) Mobile/15E148", "Accept": "text/html"}
    ]

    def __init__(self, url: str, pattern_to_search: str = "div", x: int = 5):
        """
        generally lyrics are wriiten in <p> tag, preceded by a div tag.
        This class will search for any such pattern that is present in the webpage
        :param url: url to search inside
        :param pattern_to_search: pattern to search (:default: div>p)
        :param x threshold condition for a div to be selected a lyrics div
        """
        self.url = url
        self.pattern_to_search = pattern_to_search
        self.p_threshold = x

        self.page_soup = None

    def create_soup(self):
        header_ = random.choice(self.headers)
        page_content = requests.get(self.url, header_)
        self.page_soup = BeautifulSoup(page_content.content, 'html.parser')

    def find_match(self, auto_purify=False, auto_save=False, save_raw=False):
        self.create_soup()  # request page content and create a beautiful soup object

        all_div_selector = self.pattern_to_search
        divs = self.page_soup.select(all_div_selector)
        if divs:  # if there's one div, that has at-least 5 <p> tags inside it.

            # find the best matching div
            all_p_counts = lambda divs: [len(div_html.select('p')) for div_html in divs]
            p_counts = all_p_counts(divs)
            max_index = lambda list_: list_.index(max(list_))
            best_div_index = max_index(p_counts)

            best_div_match = divs[best_div_index]
            max_p_count = p_counts[best_div_index]

            if self.p_threshold > max_p_count:
                res = input(
                    f"Max <p> count({max_p_count}) is much less than threshold({self.p_threshold}) wish to skip "
                    f"finding lyrics for this link (y|Y, n|N) ?")
                if res.lower() == 'y' or res.lower() == 'yes':
                    pass
                else:
                    logger.info("You chose to skip.")
                    return None

            logger.info(f"Best matched <div> has {max_p_count} <p> tags. Selected 1 out of {len(p_counts)},"
                        f" index={best_div_index}")

            # -------------------- extract text from the matching div ------------------------
            text = best_div_match.text  # .text will automatically remove all <script> part, if there's any captured

            if save_raw:
                self.save_(text, 'raw')

            if not auto_purify:
                if auto_save: self.save_(text)
                return text
            else:
                text_ = self.purify_content(text)
                if auto_save: self.save_(text_)
                return text_

    @staticmethod
    def purify_content(text):
        mod_text = re.sub('\n{3,}', '\n', text)
        mod_text = re.sub('x\d+', ' ', mod_text)
        return mod_text

    @staticmethod
    def save_(text, filename: str = 'temp'):
        with open(filename, 'w') as lyrics_:
            lyrics_.write(text)
        logger.info(f"lyrics saved in file: {os.path.realpath(filename)}")


if __name__ == '__main__':
    P = PatternFinder(url="https://www.lyricsmint.com/roy/chittiyaan-kalaiyaan")
    P.find_match(auto_save=True, auto_purify=True)

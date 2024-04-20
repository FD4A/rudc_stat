import time

from Source.Tournament import Tournament
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_state_str = ['rnum', 'p1', 'res', 'p2']
        self.tag_idx = 0
        self.tag_state = 0
        self.matchNum = []
        self.player1 = []
        self.result = []
        self.player2 = []

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == 'td':
            self.tag_state = self.tag_state_str[self.tag_idx]
            self.tag_idx = self.tag_idx + 1
            self.tag_idx = self.tag_idx % 4

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        if self.tag_state == self.tag_state_str[0]:
            self.matchNum.append(int(data))
        if self.tag_state == self.tag_state_str[1]:
            if isinstance(data, list):
                self.player1.append(data[0].strip())
            else:
                self.player1.append(data.strip())
        if self.tag_state == self.tag_state_str[3]:
            if isinstance(data, list):
                self.player2.append(data[0].strip())
            else:
                self.player2.append(data.strip())
        if self.tag_state == self.tag_state_str[2]:
            r = data.split('-')
            r[0] = int(r[0])
            r[1] = int(r[1])
            self.result.append(r)  # clarify possible values
        self.tag_state = ''

    def __str__(self):
        str_ = ''
        for i in range(len(self.matchNum)):
            str_ += f"{self.matchNum[i]}::{self.player1[i]}::{self.result[i]}::{self.player2[i]}\n"
        return str_


class TopdeckGGParser:
    def __init__(self, url : str):
        print(f"TopdeckGGParser URL :: {url}")
        self.url = url

    def parse_tournament(self, tr: Tournament):
        driver = webdriver.Chrome()
        try:
            driver.implicitly_wait(5)
            driver.get(self.url)
        except TimeoutException:
            print('page load not finished and try parse')
            pass
        except InvalidArgumentException:
            print(f"ERROR: problem driver.get({self.url})")
            exit(1)

        time.sleep(5)
        # with open('myfile.txt', 'a') as fd:
        #     fd.write(driver.page_source)
        return self.parse(driver.page_source, tr)


    def parse_round(self, roundtxt: str):
        round_ = Tournament.Round()
        parser = MyHTMLParser()
        parser.feed(roundtxt)
        for i in range(len(parser.matchNum)):
            m = Tournament.Match()
            m.player1 = parser.player1[i]
            m.player2 = parser.player2[i]
            m.result = parser.result[i]
            round_.matches.append(m)
        return round_

    def parse(self, page_source: str, tr: Tournament):
        """
        'id="S1R1">' - stage 1 this is swiss and round n -> #S1RN
        'id="S2R1">' - stage 2 this is top and round n -> #S2RN
        </div></div></div></div></div> - round end
        """
        tag_round_end = '</div></div></div></div></div>'
        round_count = 0
        for j in range(2):  # stage 1 and stage 2
            for i in range(10):  # I suppose for our format 10 round in one stage impossible =)
                tag = f'id="S{j+1}R{i+1}">'
                # print(f"tag:: {tag}")
                pos = page_source.find(tag)
                if -1 == pos:
                    break
                round_count += 1
                round_end = page_source[pos+len(tag):].find(tag_round_end)
                if -1 == round_end:
                    print('Unexpected round end!!!')
                    assert False
                data = page_source[pos:pos+round_end]
                round_ = self.parse_round(data)
                tr.rounds.append(round_)
        return tr

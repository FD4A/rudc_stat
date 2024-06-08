from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException
import re

from Source.Tournament import Tournament
from Source.LegendaryBase import LegendaryBase


class AetherhubParser:
    def __init__(self, url: str, lb: LegendaryBase):
        self.url = url
        self.tr = Tournament()
        self.lb = lb

    def parse_tournament(self):
        driver = webdriver.Chrome()

        driver.set_page_load_timeout(1)
        try:
            driver.get(self.url)
        except TimeoutException:
            pass  # print('page load not finished and try parse')
        except InvalidArgumentException:
            print(f"ERROR: problem driver.get({self.url})")
            exit(1)

        # self.parse_description(driver)
        self.tr.roundsCount = self.get_curr_round_number(driver.page_source)
        # self.get_date(driver.page_source)
        # self.get_organizer(driver.page_source)
        self.parse_round(driver.page_source)

        cur_round = self.tr.roundsCount - 1
        while cur_round != 0:
            idx_eq = self.url.rfind('=')
            if -1 == idx_eq:
                round_url = self.url + f"?p={cur_round}"
            else:
                round_url = self.url[:idx_eq] + f"={cur_round}"
            print(round_url)
            try:
                driver.get(round_url)
            except TimeoutException:
                pass
            self.parse_round(driver.page_source)
            cur_round -= 1

        for round_ in self.tr.rounds:
            for match_ in round_.matches:
                yes1 = False
                yes2 = False
                if len(self.tr.players) > 0:
                    for pl in self.tr.players:
                        if match_.player1.find(pl[0]) != -1:
                            match_.general1 = pl[1]
                            yes1 = True
                        if match_.player2.find(pl[0]) != -1:
                            match_.general2 = pl[1]
                            yes2 = True
                    if not yes1 or not yes2:
                        print('ERROR: bad round parse')
                else:
                    match_.general1 = 'unknown'
                    match_.general2 = 'unknown'
        self.tr.rounds.reverse()  # parse from hub start with standings = last round, then move to first round
        return [self.tr.roundsCount, self.tr.rounds]

    @staticmethod
    def get_player(str_: str):
        pos = str_.rfind(' (')
        str_ = str_[0:pos]
        return str_

    def parse_description(self, driver):
        """ obsolete? now can use local records 'player :: general' for more flexibility"""
        try:
            element = driver.find_element(By.ID, 'deckNote')
        except NoSuchElementException:
            return

        description = element.text
        pair = description.split("\n")
        for line in pair:
            res = line.split(" :: ")
            res[1] = self.lb.check_general_name_and_return_fixed(res[1])
            self.tr.players.append([res[0], res[1]])

    def get_date(self, page_source):
        # <br>
        # 'Finished:'
        # <br>
        list_m = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                  'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                  'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
                  }
        start_pos = page_source.find('Finished:')
        start_pos = start_pos + len('Finished:')
        pos_end = page_source.find('<br>', start_pos)
        date = page_source[start_pos:pos_end]
        date = date.split()
        date[1] = list_m.get(date[1])
        if date[1] is None:
            print('ERROR: parse date error')
            date[1] = '00'
        self.tr.date = f"{date[2]}_{date[1]}_{date[0]}"

    def get_organizer(self, page_source):
        # Organizer
        # <a href="/User/Andysays" target="_blank" rel="noopener">Andysays</a>
        pos = page_source.find('Organizer')
        pos = page_source.find('>', pos + len('Organizer'))
        end_pos = page_source.find('<', pos)
        self.tr.organizer = page_source[pos+1:end_pos]

    def parse_round(self, page_source):
        """"""
        # page Source example for usual and dropped player
        # start_player1 = '<td data-title="Player 1" class="">'
        # start_player2 = '<td data-title="Player 2" class="">'
        # <td data-title="Player 2" class="playerDropped">NAME (0 Points)</td>

        start_player1 = '<td data-title="Player 1"'
        start_player2 = '<td data-title="Player 2"'
        start_result = '<td data-title="Result" class="td-result">'
        end_ = '</td>'

        def form_player_list(player_start_str: str, page_source: str):
            pl_list = []
            pos_start = [i.start() for i in re.finditer(player_start_str, page_source)]
            for i, pos in enumerate(pos_start):
                while page_source[pos] != '>':
                    pos += 1
                pos += 1
                pos_end = page_source.find(end_, pos)
                pl_list.append(self.get_player(page_source[pos:pos_end]))
            return pl_list

        pl1_list = form_player_list(start_player1, page_source)
        pl2_list = form_player_list(start_player2, page_source)

        res_list = []
        pos_start_res = [i.start() for i in re.finditer(start_result, page_source)]
        for i, pos in enumerate(pos_start_res):
            pos_end = page_source.find(end_, pos+len(start_result))
            res = page_source[pos + len(start_result):pos_end].strip().split(' - ')
            if res[0] == 'No results':
                res_list.append(['No results', 'No results'])
            else:
                res_list.append([int(res[0]), int(res[1])])

        round_ = Tournament.Round()
        for i, _ in enumerate(res_list):
            if 'BYE' == pl1_list[i] or 'BYE' == pl2_list[i]:
                continue
            if res_list[i][0] == 'No results':
                continue
            m = Tournament.Match()
            m.player1 = pl1_list[i].strip()
            m.player2 = pl2_list[i].strip()
            m.result = res_list[i]
            round_.matches.append(m)
        self.tr.rounds.append(round_)

    @staticmethod
    def get_curr_round_number(page_source) -> int:
        pos = page_source.find('Pairings round ')
        if pos != -1:
            match = re.search(r'\d+', page_source[pos+len('Pairings round ')])
            if match:
                return int(match.group())
        print("ERROR: some goes wrong, can't find rounds count.")
        return 0

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re

from Source.Tournament import Tournament
from Source.LegendaryBase import LegendaryBase

class MeleeParser:

    def __init__(self, url: str, lb: LegendaryBase):
        print('MeleeParser __init__')
        self.url = url
        self.tr = Tournament()
        self.lb = lb

    def parse_tournament(self):
        print('MeleeParser parse_tournament')
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(15)

        try:
            driver.get(self.url)
            # driver.get("view-source:" + self.url)
        except TimeoutException:
            pass  # print('page load not finished and try parse')
        except InvalidArgumentException:
            print(f"ERROR: problem driver.get({self.url})")
            exit(1)

        time.sleep(7)
        self.tr.roundsCount = self.parse_round_count(driver.page_source)
        for i in range(1, self.tr.roundsCount+1):
            print(i)
            xpath = f"//button[@class='btn btn-gray round-selector'][@data-name='Round {i}'][@data-is-started='True']"
            button = driver.find_element(By.XPATH, xpath)
            actions = ActionChains(driver)
            actions.scroll_to_element(button).perform()
            time.sleep(0.5)
            actions.move_to_element(button).click().perform()
            time.sleep(0.5)
            button.click()
            time.sleep(0.5)
            self.parse_matches(driver.page_source, i)

        return [self.tr.roundsCount, self.tr.rounds]

    @staticmethod
    def is_bye(text: str):
        if -1 != text.find('was assigned a bye'):
            return True
        return False

    @staticmethod
    def is_won(text: str):
        if -1 != text.find('won'):
            return True
        return False

    @staticmethod
    def is_draw(text: str):
        if -1 != text.find('Draw'):
            return True
        return False

    @staticmethod
    def is_play_draw(text: str):
        if -1 != text.find('0-0-3'):
            return False
        return True

    def parse_matches(self, text, roundNum):
        # start parings
        # startTxt = '<tr role="row" class="odd"><td class="TableNumber-column sorting_1">-</td><td class=" Teams-column">    <div class="match-table-teams-container">'
        #             <tr role="row" class="odd"><td class="TableNumber-column sorting_1">1</td><td class=" Teams-column">    <div class="match-table-teams-container">
        start_txt = '</td><td class=" Teams-column">    <div class="match-table-teams-container">'
        # end parings

        # players in paring 1 or 2
        # </td><td class=" ResultString-column">Oleg Lyalin was assigned a bye</td>
        # result
        # ('ResultString-column">(.+?)</td>', text)
        # data-type="player" href="/Profile/Index/(.+?)">
        # ResultString-column">(.+?)</td>

        round_ = Tournament.Round()

        start_pos = text.find(start_txt)
        finish_all = re.search("Displaying.*matche", text)
        finish_pos = finish_all.start()
        # print(startPos)
        # print(finishPos)
        # print(text[start_pos:finish_pos])
        # exit(0)
        new_text = text[start_pos:finish_pos]
        pos = 0

        pattern = re.compile('data-type="player" href="/Profile/Index/.*>(.+?)<svg class=".*')
        players_list = re.findall(pattern, new_text)
        # print("      player list:")
        # for result in players_list:
        #     print(result)

        # print('------------------------------------------')
        results = re.findall('ResultString-column">(.+?)</td>', text)
        pos_in_players_list = 0
        # print(players_list[pos_in_players_list])
        for result in results:
            # берём результат
                # bye:: Имя was assigned a bye
                    # 1 игрок нет матча
                # won:: Имя won d-d-d
                    # 2 игрока
                # Draw:: d-d-d Draw if 0-0-3 => id не считаем
                    # 2 игрока
            if self.is_bye(result):
                # print(result)
                pos_in_players_list = pos_in_players_list + 1
            elif self.is_won(result):
                # print(result)
                m = Tournament.Match()
                m.player1 = players_list[pos_in_players_list]
                pos_in_players_list = pos_in_players_list + 1
                m.player2 = players_list[pos_in_players_list]
                pos_in_players_list = pos_in_players_list + 1
                res = result[-6:].split('-')
                # print(res)
                m.result = [int(res[0]), int(res[1])]
                round_.matches.append(m)
            elif self.is_draw(result):
                # print(result)
                if self.is_play_draw(result):
                    m = Tournament.Match()
                    m.player1 = players_list[pos_in_players_list]
                    pos_in_players_list = pos_in_players_list + 1
                    m.player2 = players_list[pos_in_players_list]
                    pos_in_players_list = pos_in_players_list + 1
                    res = result[0:6].split('-')
                    # print(res)
                    m.result = [int(res[0]), int(res[1])]
                    round_.matches.append(m)
                else:
                    # print(result)
                    pos_in_players_list = pos_in_players_list + 2
        # print('------------------------------------------')
        self.tr.rounds.append(round_)
        # print(round_)

    def parse_round_count(self, text):
        # <button class="btn btn-gray round-selector"
        result = re.findall('<button class="btn btn-gray round-selector', text)
        # print(result)
        res = len(result)/2
        # print(f"FDA {res}")
        return int(res)

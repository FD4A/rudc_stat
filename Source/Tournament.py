import json
import io

from Source.LegendaryBase import LegendaryBase
from Source.PlayerGeneralObject import PlayerGeneralObject


class Tournament:
    class Match:
        def __init__(self):
            self.player1 = 'player1'
            self.player2 = 'player2'
            self.general1 = 'general1'
            self.general2 = 'general2'
            self.result = []  # in reality this is fixed set
            # [0,0] [1,0] [0,1] [1,1], [2,1] [1,2], [2,0] [0,2], bye and id

        def __str__(self):
            str_ = f"{self.player1}::{self.general1} vs {self.player2}::{self.general2}, {self.result[0]} - {self.result[1]}"
            return str_

    class Round:
        def __init__(self):
            self.matches = []

        def __str__(self):
            str_ = ''
            for match in self.matches:
                str_ += f"{match}\n"
            return str_

    def __init__(self):
        self.organizer = 'Noname'
        self.location = 'Nowhere'
        self.level = 'Regular'  # regular-open-pub-testing?
        self.date = 'YYYY_MM_DD'
        self.roundsCount = 0
        self.players = []
        self.rounds = []  # Round( matches: []), match: player1, player2, general1, general2, result[X1, X2]
        self.url = ""

    def __str__(self):
        str_ = ''
        str_ += f"{self.location}_{self.level}_{self.date}\n"
        for pl in self.players:
            str_ += f"{pl}\n"
        str_ += f"\n"
        str_ += f"rounds = {self.roundsCount}\n"
        for i, round_ in enumerate(self.rounds):
            str_ += f"Round{i+1}\n{round_}\n"
        return str_

    def form_name(self):
        return f"{self.location}-{self.date}-{self.level}-{self.organizer}-players[{len(self.players)}]"

    def form_json_filename(self):
        return self.form_name()+".json"

    def form_stat_filename(self):
        return self.form_name()+".txt"

    def dump_to_json(self, out_dir='./', filename=''):
        dump_pl = []
        for pl in self.players:
            dump_pl.append([pl[0], pl[1]])

        dump_rounds = []
        for round_ in self.rounds:
            dump_match = []
            for match in round_.matches:
                dump_match.append([match.player1, match.player2, match.general1, match.general2, match.result])
            dump_rounds.append(dump_match)

        dump_data = {'date': self.date,
                     'location': self.location,
                     'level': self.level,
                     'organizer': self.organizer,
                     'roundsCount': self.roundsCount,
                     'players': dump_pl,
                     'rounds': dump_rounds,
                     'url': self.url
                     }

        if filename == '':
            filename = self.form_json_filename()
        with io.open(f"{out_dir}{filename}", 'w', encoding='utf8') as outfile:
            str_ = json.dumps(dump_data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)

    @staticmethod
    def load_from_json(filename):
        tr = Tournament()
        with io.open(f"{filename}", 'r', encoding='utf8') as fd:
            data = json.load(fd)
            tr.date = data['date']
            tr.location = data['location']
            tr.level = data['level']
            tr.roundsCount = data['roundsCount']
            tr.players = data['players']
            tr.organizer = data['organizer']
            try:
                tr.url = data['url']
            except Exception:
                pass

            for r in data['rounds']:
                round_ = Tournament.Round()
                for m in r:
                    match_ = Tournament.Match()
                    match_.player1 = m[0]
                    match_.player2 = m[1]
                    match_.general1 = m[2]
                    match_.general2 = m[3]
                    match_.result = m[4]
                    round_.matches.append(match_)
                tr.rounds.append(round_)
        return tr

    class Date:
        def __init__(self, str_):
            split_date = str_.split('_')
            self.yyyy = int(split_date[0])
            self.mm = int(split_date[1])
            self.dd = int(split_date[2])

        def before_date(self, in_date):
            """ expect date like string in format YYYY_MM_DD"""
            if self.yyyy < in_date.yyyy:
                return True
            elif self.yyyy == in_date.yyyy:
                if self.mm < in_date.mm:
                    return True
                elif self.mm == in_date.mm:
                    if self.dd <= in_date.dd:
                        return True
            return False

        def after_date(self, in_date):
            """ expect date like string in format YYYY_MM_DD"""
            if self.yyyy > in_date.yyyy:
                return True
            elif self.yyyy == in_date.yyyy:
                if self.mm > in_date.mm:
                    return True
                elif self.mm == in_date.mm:
                    if self.dd >= in_date.dd:
                        return True
            return False

        def __str__(self):
            return f"{str(self.yyyy).zfill(4)}-{str(self.mm).zfill(2)}-{str(self.dd).zfill(2)}"

    def before_date(self, input_date='9999_99_99'):
        """ expect date like string in format YYYY_MM_DD"""
        return Tournament.Date(self.date).before_date(Tournament.Date(input_date))

    def after_date(self, input_date='0000_00_00'):
        return Tournament.Date(self.date).after_date(Tournament.Date(input_date))

    @staticmethod
    def get_min_max_date(dates: list):
        D = []
        for d in dates:
            D.append(Tournament.Date(d))
        min_date = Tournament.Date('9999_99_99')
        max_date = Tournament.Date('0000_00_00')
        for d in D:
            if d.before_date(min_date):
                min_date = d
            if d.after_date(max_date):
                max_date = d
        return [min_date, max_date]

    def get_participant_general(self, name: str):
        for pl in self.players:
            if pl[0] == name:
                return pl[1]
        return None

    def set_players_generals(self, players: list, lb: LegendaryBase):
        self.players.clear()
        for item in players:
            # fix literals in generals name
            if lb.legend.get(item[1]) is None:
                candidates = lb.get_closest_candidate(item[1])
                self.replace_general_name_in_rounds(item[1], candidates[0][1])
                item[1] = candidates[0][1]
            self.players.append([item[0], item[1]])

        for round_ in self.rounds:
            for m in round_.matches:
                for item in players:
                    if m.player1 == item[0]:
                        m.general1 = item[1]
                    if m.player2 == item[0]:
                        m.general2 = item[1]

    def set_generals_by_players(self, players: list):
        for round_ in self.rounds:
            for m in round_.matches:
                for item in players:
                    if m.player1 == item[0]:
                        m.general1 = item[1]
                    if m.player2 == item[0]:
                        m.general2 = item[1]

    def replace_general_name_in_rounds(self, old_general_name, new_general_name):
        for round_ in self.rounds:
            for m in round_.matches:
                if m.general1 == old_general_name:
                    m.general1 = new_general_name
                if m.general2 == old_general_name:
                    m.general2 = new_general_name

    def fix_generals_names(self, legendary_base: LegendaryBase):
        str_ = ''
        ret = True
        for pl in self.players:
            pgo = PlayerGeneralObject(f"{pl[0]}+ :: + {pl[1]}", legendary_base)
            pl[1] = pgo.command_zone
        return [ret, str_]

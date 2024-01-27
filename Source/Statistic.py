import json
import io

from Source.Tournament import Tournament


class Matchup:
    def __init__(self, general, score1, score2):
        self.vs_general = general
        self.own_score = score1
        self.vs_score = score2
        self.win = self.lose = self.draw = 0
        if score1 > score2:
            self.win = 1
        elif score2 > score1:
            self.lose = 1
        else:
            self.draw = 1

    def set(self, general, score1, score2, win, lose, draw):
        self.vs_general = general
        self.own_score = score1
        self.vs_score = score2
        self.win = win
        self.lose = lose
        self.draw = draw

    def add(self, other):
        self.own_score += other.own_score
        self.vs_score += other.vs_score
        self.win += other.win
        self.lose += other.lose
        self.draw += other.draw

    def __str__(self):
        magic_len = 32
        cz_plain = self.vs_general.replace(' :++: ', '+')
        cz_plain = cz_plain.replace(' :+: ', '+')
        cz_plain = cz_plain.split('+')
        str_ = f"{'vs ':>10}{(cz_plain[0][:magic_len]).ljust(magic_len)} (w:{self.win} l:{self.lose} d:{self.draw}), ({self.own_score}/{self.vs_score})"
        for item in cz_plain[1:]:
            str_ += f"\n{'  + ':>10}{item.ljust(magic_len)[:magic_len]}"
        return str_

class GeneralStat:
    def __init__(self, general_: str):
        self.general = general_
        self.pick_total = 0
        self.matches_total = 0
        self.win = 0
        self.lose = 0
        self.draw = 0
        self.match_wrate = 0
        self.match_lrate = 0
        self.match_drate = 0
        self.games_total = 0
        self.game_win = 0
        self.game_lose = 0
        self.game_wrate = 0
        self.game_lrate = 0
        self.matchups = {}

    def recalc_rates(self):
        self.match_wrate = 100 * self.win / self.matches_total
        self.match_lrate = 100 * self.lose / self.matches_total
        self.match_drate = 100 * self.draw / self.matches_total
        self.game_wrate = 100 * self.game_win / self.games_total
        self.game_lrate = 100 * self.game_lose / self.games_total

    def add_match(self, vs_general, score1, score2):
        matchup = self.matchups.get(vs_general)
        self.matches_total += 1
        self.games_total += score1 + score2
        if score1 + score2 == 0:
            self.games_total += 1
        self.game_win += score1
        self.game_lose += score2
        if score1 > score2:
            self.win += 1
        elif score2 > score1:
            self.lose += 1
        else:
            self.draw += 1
        if matchup is None:
            matchup = Matchup(vs_general, score1, score2)
        else:
            matchup.add(Matchup(vs_general, score1, score2))
        self.recalc_rates()
        self.matchups.update({vs_general: matchup})

    def __str__(self):
        return self.to_str()

    def to_str(self, full=True):
        magic_len = 32  # replace by max length general
        cz_plain = self.general.replace(' :++: ', '+')
        cz_plain = cz_plain.replace(' :+: ', '+')
        cz_plain = cz_plain.split('+')
        str_ = f"{(cz_plain[0]).ljust(magic_len)[:magic_len]} "
        str_ += f"matches:{str(self.matches_total).ljust(4):<4} "
        str_ += f"WM:{self.match_wrate:>6.2f}%  LM:{self.match_lrate:>6.2f}%  DM:{self.match_drate:>6.2f}% "
        str_ += f"(wm:{str(self.win).ljust(3)} lm:{str(self.lose).ljust(3)} dm:{(str(self.draw)+')').ljust(3)} "
        str_ += f"games:{self.games_total:<4} "
        str_ += f"WG:{self.game_wrate:>6.2f}% LG:{self.game_lrate:>6.2f}% "
        str_ += f"(wg:{self.game_win:>4} lg:{self.game_lose:>4}) pick: {self.pick_total:<4}"
        for item in cz_plain[1:]:
            str_ += f"\n{('  + '+item).ljust(magic_len)[:magic_len]}"
        str_ += '\n'
        if not full:
            return str_
        for matchup in self.matchups.values():
            str_ += f"{matchup}\n"
        return str_


class Statistic:
    def __init__(self):
        self.generalStat = {}
        self.tournaments_names = []

    def general_pick(self, tr: Tournament):
        for item in tr.players:
            gs = self.generalStat.get(item[1])
            if gs is None:
                gs = GeneralStat(item[1])
            gs.pick_total += 1
            self.generalStat.update({item[1]: gs})

    def add_tournament(self, tr: Tournament, exclude_generals: list):
        self.tournaments_names.append(tr.form_name())
        self.general_pick(tr)
        for r in tr.rounds:
            for m in r.matches:
                skip = False
                for ex_gen in exclude_generals:
                    if m.general1 == ex_gen or ex_gen == m.general2:
                        skip = True
                        break
                if not skip:
                    self.add_match(m.general1, m.general2, m.result[0], m.result[1])
        self.generalStat = dict(sorted(self.generalStat.items(), key=lambda item: item[0]))

    def add_match(self, general1: str, general2: str, score1: int, score2: int):
        if general1 == 'general1' or general2 == 'general2':
            return
        if general1 == 'unknown' or general2 == 'unknown':
            return
        if general1 == general2:
            return  # no mirror in stat, because this move rates to 50%

        gs = self.generalStat.get(general1)
        gs.add_match(general2, score1, score2)
        self.generalStat.update({general1: gs})

        gs = self.generalStat.get(general2)
        gs.add_match(general1, score2, score1)
        self.generalStat.update({general2: gs})

    def get_generals(self):
        str_ = ''
        for i, elem in enumerate(self.generalStat.values()):
            str_ += f"{i+1} :: {elem.general}\n"
        return str_

    def get_general_stat(self, num: int):
        i = 1
        str_ = None
        for elem in self.generalStat.values():
            if num == i:
                str_ = f"{elem}"
                break
            i += 1
        return str_

    def dump_to_json(self, filename='RuDcStatAll.json'):
        dump_data = []
        for gs in self.generalStat.values():
            g = dict()
            g['name'] = gs.general
            g['pick_total'] = gs.pick_total
            g['matches_total'] = gs.matches_total
            g['win'] = gs.win
            g['lose'] = gs.lose
            g['draw'] = gs.draw
            g['match_wrate'] = gs.match_wrate
            g['match_lrate'] = gs.match_lrate
            g['match_drate'] = gs.match_drate
            g['games_total'] = gs.games_total
            g['game_win'] = gs.game_win
            g['game_lose'] = gs.game_lose
            g['game_wrate'] = gs.game_wrate
            g['game_lrate'] = gs.game_lrate
            g['matchups'] = []
            for mch in gs.matchups.values():
                m = dict()
                m['vs_general'] = mch.vs_general
                m['own_score'] = mch.own_score
                m['vs_score'] = mch.vs_score
                m['win'] = mch.win
                m['lose'] = mch.lose
                m['draw'] = mch.draw
                g['matchups'].append(m)
            dump_data.append(g)

        with io.open(f"{filename}", 'w', encoding='utf8') as outfile:
            str_ = json.dumps(dump_data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)

    @staticmethod
    def load_from_json(filename):
        stat = Statistic()
        with io.open(f"{filename}", 'r', encoding='utf8') as fd:
            data = json.load(fd)
            for elem in data:
                gs = GeneralStat(elem['name'])
                gs.general = elem['name']
                gs.pick_total = elem['pick_total']
                gs.matches_total = elem['matches_total']
                gs.win = elem['win']
                gs.lose = elem['lose']
                gs.draw = elem['draw']
                gs.match_wrate = elem['match_wrate']
                gs.match_lrate = elem['match_lrate']
                gs.match_drate = elem['match_drate']
                gs.games_total = elem['games_total']
                gs.game_win = elem['game_win']
                gs.game_lose = elem['game_lose']
                gs.game_wrate = elem['game_wrate']
                gs.game_lrate = elem['game_lrate']
                for mch in elem['matchups']:
                    m = Matchup(mch['vs_general'], 0, 0)
                    m.set(mch['vs_general'], mch['own_score'], mch['vs_score'],
                          mch['win'], mch['lose'], mch['draw'])
                    gs.matchups[mch['vs_general']] = m
                stat.generalStat[elem['name']] = gs
        return stat

    def get_tournaments_names(self):
        str_ = ''
        self.tournaments_names.sort()
        for elem in self.tournaments_names:
            str_ += f"{elem}\n"
        str_ += '\n\n'
        return str_

    def __str__(self):
        str_ = ''
        for elem in self.generalStat.values():
            str_ += f"{elem}"
            str_ += '\n'
        return str_

    def to_str(self, sort_type, full=False):
        str_ = ''
        ret = []
        if sort_type == 'matches_total':
            for elem in self.generalStat.values():
                ret.append([elem.matches_total, elem])
                ret.sort(key=lambda item: item[0], reverse=True)
        if sort_type == 'matches_win':
            for elem in self.generalStat.values():
                ret.append([elem.match_wrate, elem])
                ret.sort(key=lambda item: item[0], reverse=True)
        if sort_type == 'matches_loss':
            for elem in self.generalStat.values():
                ret.append([elem.match_lrate, elem])
                ret.sort(key=lambda item: item[0], reverse=True)
        if sort_type == 'matches_draw':
            for elem in self.generalStat.values():
                ret.append([elem.match_drate, elem])
                ret.sort(key=lambda item: item[0], reverse=True)

        if sort_type == 'games_total':
            for elem in self.generalStat.values():
                ret.append([elem.games_total, elem])
                ret.sort(key=lambda item: item[0], reverse=True)
        if sort_type == 'games_win':
            for elem in self.generalStat.values():
                ret.append([elem.game_wrate, elem])
                ret.sort(key=lambda item: item[0], reverse=True)
        if sort_type == 'games_loss':
            for elem in self.generalStat.values():
                ret.append([elem.game_lrate, elem])
                ret.sort(key=lambda item: item[0], reverse=True)

        if sort_type == '' or sort_type == 'name':
            for elem in self.generalStat.values():
                ret.append([elem.games_total, elem])

        for elem in ret:
            str_ += f"{elem[1].to_str(full)}"

        return str_

    def to_html(self, filename, short=True):
        with open(f"{filename}", 'w', encoding='utf-8') as fd:
            fd.write('<!DOCTYPE html PUBLIC"-//W3C//DTD HTML 4.01 Transitional//EN">')
            fd.write('<html>')
            fd.write('<head>')
            fd.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">')
            fd.write('<title>RuDc stats</title>')
            fd.write('<style>')
            fd.write('h1{')
            fd.write('color: #4C4C4C;')
            fd.write('padding-bottom: 20px;')
            fd.write('margin-bottom: 20px;')
            fd.write('border-bottom: 2px solid #BEBEBE;')
            fd.write('text-align: center;')
            fd.write('}')
            fd.write('pre{')
            fd.write('font-size: 14px;')
            fd.write('}')
            fd.write('</style>')
            fd.write('</head>')
            fd.write('<body>')

            fd.write('<h1>RuDc</h1>')

            fd.write('<h2>Tournaments List</h2>')
            # add data about each tournament
            # <details>
            # <summary>tournament_name</summary>
            # <pre>some_tournament_text</pre>
            # </details>

            str_ = self.get_tournaments_names()
            fd.write(f"<pre>{str_}</pre>")

            fd.write('<h2>Stats</h2>')
            if short:
                str_ = self.to_str_only_generals(False)
            else:
                str_ = f"{self}"
            fd.write(f"<pre>{str_}</pre>")

            fd.write('</body>')
            fd.write('</html>')

# Fields Legend:
# Name Date Place General PlayerLocation-? Empty result_roundN opponent_roundN...
# Result Legend:
# '21' win 2:1,
# '20' win 2:0,
# '2' lose 0:2
# '12' lose 1:2
# 'id' split
# '11' draw 1:1
# 'bye' opponent bye,

from Source.Tournament import Tournament
from Source.LegendaryBase import LegendaryBase
from Source.PlayerGeneralObject import PlayerGeneralObject


class KrasnodarFileLine:
    def __init__(self, line: str):
        fields = line.split('\t')
        # print(fields)
        self.name = fields[0]
        tmp = fields[1].replace('/','_')
        tmp = tmp.split('_')
        tmp.reverse()
        # print(tmp)
        tmp[0] = str(int(tmp[0])+2000)
        self.date = f"{tmp[0]}_{tmp[1]}_{tmp[2]}"
        self.general = fields[3]
        print(self.general)
        self.rounds = []
        rounds_count = (len(fields) - 6) // 2
        for i in range(0, rounds_count, 1):
            if fields[7+i*2] != '':
                self.rounds.append([fields[6+i*2], fields[7+i*2]])

    def __str__(self):
        str_ = ''
        str_ += f"{self.name}::{self.general}"
        for r in self.rounds:
            str_ += f"{r}"
        return str_


class KrasnodarParser:
    def __init__(self, lb: LegendaryBase):
        self.lb = lb

    def parse_tournament(self, data: list):
        kr_data = []
        for line in data:
            kr_data.append(KrasnodarFileLine(line))

        tr = Tournament()
        for item in kr_data:
            com_zone = PlayerGeneralObject(item.name + ' :: ' + item.general, self.lb)
            item.general = com_zone.command_zone
            tr.players.append([item.name, item.general])
            tr.roundsCount = max(tr.roundsCount, len(item.rounds))

        res_dict = {'21': [2, 1],
                    '12': [1, 2],
                    '20': [2, 0],
                    '2': [0, 2],
                    '02': [0, 2],
                    '01': [0, 1],
                    '10': [1, 0],
                    '1': [0, 1],
                    '11': [1, 1],
                    '00': [0, 0],
                    '0': [0, 0],
                    'id': [1, 1],
                    '4': [1, 1],
                    'bye': [2, 0],
                    '3': [2, 0],
                    }
        for i in range(0, tr.roundsCount):
            round_ = Tournament.Round()
            for item in kr_data:
                if len(item.rounds) < i + 1:
                    continue
                m = Tournament.Match()
                m.player1 = item.name
                m.general1 = item.general
                if item.rounds[i][0] == 'bye':
                    continue
                m.result = res_dict[item.rounds[i][0]]
                m.player2 = item.rounds[i][1]
                m.general2 = tr.get_participant_general(m.player2)
                if m.general2 is None:
                    print("player general not found!")
                    exit(1)

                if len(round_.matches) == 0:
                    round_.matches.append(m)
                    continue
                add = True
                for M in round_.matches:
                    if M.player1 == m.player2:
                        add = False
                        break
                if add:
                    round_.matches.append(m)
            tr.rounds.append(round_)
        return [tr.players, tr.roundsCount, tr.rounds]

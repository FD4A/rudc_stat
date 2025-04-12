from Source.Tournament import Tournament
from Source.LegendaryBase import LegendaryBase
from Source.PlayerGeneralObject import PlayerGeneralObject

from Source.parsers.LeagueParser import LeagueParser
from Source.parsers.KrasnodarParser import KrasnodarParser
from Source.parsers.AetherhubParser import AetherhubParser
from Source.parsers.TopdeckGG import TopdeckGGParser


class ParseRawTxtCommon:
    """
    linear parsing text file with tournament data, only Round part expect different for
    different data sources. In file:
        - expect tags location, level, date, organizer before tag players-generals
        - expect tag players-generals before tag Round
    """
    location_tag = 'location::'
    level_tag = 'level::'
    date_tag = 'date::'
    organizer_tag = 'organizer::'
    players_tag = 'players::generals'  # format depends on raw format, see parse_command_zone_line function
    round_tag = 'Round'  # format depends on raw format, use different parsers
    parser_league = 'league'
    parser_aetherhub = 'aetherhub'
    parser_Krasnodar = 'Krasnodar'
    parser_topdeckGG = 'topdeckGG'

    def __init__(self, parser_type: str, lb: LegendaryBase):
        self.parser_type = parser_type
        self.lb = lb
        self.data = None  # lines in file
        self.pos = 0  # pos in data <=> current line in file
        self.tr = Tournament()

    def get_tournament_from_txt(self, filename):
        self.tr = Tournament()
        with open(f"{filename}", 'r', encoding='utf-8') as fd:
            self.data = fd.read()
            self.data = self.data.split('\n')

        if self.parser_type == ParseRawTxtCommon.parser_league:
            self.get_common_data(ParseRawTxtCommon.players_tag)
            self.get_players_generals()
            [self.tr.rounds, self.tr.roundsCount] = LeagueParser.parse(self.data, self.pos, ParseRawTxtCommon.round_tag)
            self.tr.set_generals_by_players(self.tr.players)
        elif self.parser_type == ParseRawTxtCommon.parser_Krasnodar:
            self.get_common_data(ParseRawTxtCommon.round_tag)
            parser = KrasnodarParser(self.lb)
            [self.tr.players, self.tr.roundsCount, self.tr.rounds] = parser.parse_tournament(self.data[self.pos:])
            self.tr.set_generals_by_players(self.tr.players)
        elif self.parser_type == ParseRawTxtCommon.parser_aetherhub:
            self.get_common_data(ParseRawTxtCommon.players_tag)
            self.get_players_generals()
            self.tr.url = self.data[self.pos+1]
            parser = AetherhubParser(self.data[self.pos+1], self.lb)
            [self.tr.roundsCount, self.tr.rounds] = parser.parse_tournament()
            self.tr.set_generals_by_players(self.tr.players)
        elif self.parser_type == ParseRawTxtCommon.parser_topdeckGG:
            self.get_common_data(ParseRawTxtCommon.players_tag)
            self.get_players_generals()
            parser = TopdeckGGParser(self.data[self.pos+1])
            self.tr = parser.parse_tournament(self.tr)
            self.tr.fix_generals_names(self.lb)
            self.tr.set_generals_by_players(self.tr.players)
            self.tr.roundsCount = len(self.tr.rounds)
        else:
            print("ERROR: Unknown parser")
            exit(1)
        return self.tr

    def get_common_data(self, stop_tag):
        for line in self.data:
            self.pos += 1
            if 0 == line.find(self.date_tag):
                self.tr.date = line[len(self.date_tag):]
                continue
            if 0 == line.find(self.level_tag):
                self.tr.level = line[len(self.level_tag):]
                continue
            if 0 == line.find(self.organizer_tag):
                self.tr.organizer = line[len(self.organizer_tag):]
                continue
            if 0 == line.find(self.location_tag):
                self.tr.location = line[len(self.location_tag):]
                continue
            if 0 == line.find(stop_tag):
                break

    def get_players_generals(self):
        for line in self.data[self.pos:]:
            self.pos += 1
            if 0 == line.find(self.round_tag):
                self.pos -= 1
                break
            pgo = PlayerGeneralObject(line, self.lb)
            self.tr.players.append([pgo.player_name, pgo.command_zone])

from Source.Tournament import Tournament


class LeagueParser:
    class ParseMatchLine:
        def __init__(self):
            self.start_name1 = 7
            self.start_name2 = 36
            self.stop_name2 = 65
            self.start_res = 70
            self.stop_res = 73

        def get_name1_name2_result(self, str_: str):
            if len(str_) < self.stop_res:
                return None
            player1 = str_[self.start_name1:self.start_name2].strip()
            player2 = str_[self.start_name2:self.stop_name2].strip()
            tmp = str_[self.start_res:self.stop_res].split('-')
            match_result = [int(tmp[0]), int(tmp[1])]
            return [player1, player2, match_result]

    @staticmethod
    def parse(data: list, pos: int, round_tag: str):
        cur_round = -1
        pos -= 1
        mathc_line_parser = LeagueParser.ParseMatchLine()
        rounds = []
        for line in data[pos:]:
            if 0 == line.find(round_tag):
                cur_round += 1
                rounds.append(Tournament.Round())
                continue

            tr_match = Tournament.Match()
            ret = mathc_line_parser.get_name1_name2_result(line)
            if ret is not None:
                tr_match.player1, tr_match.player2, tr_match.result = ret[0], ret[1], ret[2]
                rounds[cur_round].matches.append(tr_match)

        rounds_count = cur_round + 1
        return [rounds, rounds_count]

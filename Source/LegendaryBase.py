from fuzzywuzzy import fuzz


class LegendaryBase:
    def __init__(self, folder: str):
        """
        :param filename: - file with legends names parsed from scryfall
        """
        self.legend = {}
        with open(f"{folder}/LegendsScryFall.txt", 'r', encoding='utf-8') as fd:
            data = fd.read()
            data = data.split('\n')
            for line in data:
                self.legend[line] = line

        self.backgrounds = {}
        with open(f"{folder}/Background.txt", 'r', encoding='utf-8') as fd:
            data = fd.read()
            data = data.split('\n')
            for line in data:
                [name, color_identity] = line.split(' :: ')
                self.backgrounds[name] = color_identity
        # print(self.backgrounds)

    def __str__(self):
        str_ = ''
        for item in self.legend.values():
            str_ += item + '\n'
        return str_

    def get_closest_candidate(self, bad_general_name: str, best_overlap_len=3):
        """
        find the best candidates for name replace
        :param bad_general_name: - input general name
        :param best_overlap_len:  - how much best candidates return
        :return: list of [overlap rate, name] in descending order by overlap rate
        """
        cut_ = len(bad_general_name)  # experimental for best lib result must be same length
        closest = [[0, ''] for _ in range(best_overlap_len)]
        for name in self.legend.values():
            cur_overlap_rate = fuzz.ratio(bad_general_name, name[:cut_])
            for candidate in closest:
                if cur_overlap_rate > candidate[0]:
                    candidate[0] = cur_overlap_rate
                    candidate[1] = name
                    break
        closest.sort(key=lambda item: item[0], reverse=True)
        return closest

    def check_general_name_and_return_fixed(self, general_name: str):
        if self.legend.get(general_name) is None:
            candidates = self.get_closest_candidate(general_name)
            return candidates[0][1]
        return general_name

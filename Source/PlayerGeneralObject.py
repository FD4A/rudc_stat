from Source.LegendaryBase import LegendaryBase


class PlayerGeneralObject:
    """
    input line: 'player_name :: general1 :+: general2 or background :++: companion'
    examples:
        PlayerName :: Karlov of the Ghost Council :++: Lurrus of the Dream-Den
        PlayerName :: Akiri, Line-Slinger :+: Silas Renn, Seeker Adept
        PlayerName :: Akiri, Line-Slinger :+: Francisco, Fowl Marauder :++: Lurrus of the Dream-Den
    """

    def __init__(self, str_: str, lb: LegendaryBase):
        self.command_zone = str_
        self.generals = []
        self.additions = []
        [self.player_name, command_line] = self.command_zone.split(' :: ')

        command_line = command_line.split(' :++: ')
        if len(command_line) > 1:
            for item in command_line[1:]:
                if lb is None:
                    self.additions.append(item)
                else:
                    self.additions.append(lb.check_general_name_and_return_fixed(item))

        gl = command_line[0].split(' :+: ')
        if lb is not None:
            for i, item in enumerate(gl):
                gl[i] = lb.check_general_name_and_return_fixed(item)

        self.generals.append(gl)
        if len(self.additions) != 0:
            self.generals.append(self.additions)

        # move names to line
        self.command_zone = self.generals[0][0]
        for item in self.generals[0][1:]:
            self.command_zone += f" :+: {item}"

        if len(self.generals) > 1:
            self.command_zone += f" :++: {self.generals[1][0]}"
            for item in self.generals[1][1:]:
                self.command_zone += item

    def get_like_complex_list(self):
        """
        :return: [player_name, [[general1, general2 or somthing else, ...], [companion and other additions]]]
        """
        return [self.player_name, self.generals]

from collections import namedtuple
from Source.LegendaryBase import LegendaryBase

GetParams = namedtuple('GetParams', ['date_after', 'date_before', 'open', 'regular', 'other',
                       'league', 'full_stat', 'min_players', 'min_match_count', 'sort_type',
                       'mach_threshold_for_full_matchup', 'location',])


class RequestFrom:
    first_time = True
    default_date_after = '2023_06_01'
    default_date_before = '2025_01_01'
    legend_base = None

    def __init__(self, legend_base: LegendaryBase):
        RequestFrom.legend_base = legend_base
        self.date_after = RequestFrom.default_date_after
        self.date_before = RequestFrom.default_date_before
        self.regular = 'checked'
        self.open = 'checked'
        self.league = 'checked'
        self.other = 'checked'
        self.full_stat = 'checked'
        self.sort_type_name = 'checked'
        self.location = 'all'
        self.loc_all = 'selected'
        self.loc_Barnaul = ''
        self.loc_Krasnodar = ''
        self.loc_Moscow = ''
        self.loc_Online = ''
        self.loc_RostovOnDon = ''
        self.loc_Saratov = ''
        self.loc_Spb = ''
        self.loc_Ussuriysk = ''
        self.loc_Volgograd = ''
        self.loc_Yekaterinburg = ''
        self.sort_type_matches_tot = ''
        self.sort_type_matches_win = ''
        self.sort_type_matches_loss = ''
        self.sort_type_matches_draw = ''
        self.sort_type_games_tot = ''
        self.sort_type_games_win = ''
        self.sort_type_games_loss = ''
        self.min_players_count = 4
        self.min_match_count = 1
        self.mach_threshold_for_full_matchup = 1

    @staticmethod
    def __check_min_players(min_pl, default_value=4):
        for i, alpha in enumerate(min_pl):
            if not alpha.isdigit():
                return default_value
        return int(min_pl)

    @staticmethod
    def __check_mach_threshold_for_full_matchup(mach_threshold_for_full_matchup, default_value=1):
        for i, alpha in enumerate(mach_threshold_for_full_matchup):
            if not alpha.isdigit():
                return default_value
        return int(mach_threshold_for_full_matchup)

    @staticmethod
    def __check_min_match_count(min_match_count, default_value=1):
        for i, alpha in enumerate(min_match_count):
            if not alpha.isdigit():
                return default_value
        return int(min_match_count)

    @staticmethod
    def __check_date(date, default_date):
        if date[0].isdigit() and\
           date[1].isdigit() and\
           date[2].isdigit() and\
           date[3].isdigit() and \
           (date[4] == '_' or date[4] == ':' or date[4] == '-' or date[4] == '.') and\
           date[5].isdigit() and\
           date[6].isdigit() and \
           (date[7] == '_' or date[7] == ':' or date[7] == '-' or date[7] == '.') and\
           date[8].isdigit() and\
           date[9].isdigit():
            return f"{date[0:4]}_{date[5:7]}_{date[8:10]}"
        return default_date

    def parse_params(self, plist):
        print(plist)
        date_after = RequestFrom.default_date_after
        date_before = RequestFrom.default_date_before
        self.league = ''
        self.open = ''
        self.regular = ''
        self.other = ''
        self.full_stat = ''
        self.location = ''
        self.loc_all = ''
        self.loc_Barnaul = ''
        self.loc_Krasnodar = ''
        self.loc_Moscow = ''
        self.loc_Online = ''
        self.loc_RostovOnDon = ''
        self.loc_Saratov = ''
        self.loc_Spb = ''
        self.loc_Ussuriysk = ''
        self.loc_Volgograd = ''
        self.loc_Yekaterinburg = ''
        self.sort_type_name = ''
        self.sort_type_matches_tot = ''
        self.sort_type_matches_win = ''
        self.sort_type_matches_loss = ''
        self.sort_type_matches_draw = ''
        self.sort_type_games_tot = ''
        self.sort_type_games_win = ''
        self.sort_type_games_loss = ''
        self.min_match_count = 1
        self.min_players_count = 4
        self.mach_threshold_for_full_matchup = 1
        for item in plist:
            if 0 == item.find("date_after"):
                date_after = RequestFrom.__check_date(item[len("date_after")+1:], RequestFrom.default_date_after)
            if 0 == item.find("date_before"):
                date_before = RequestFrom.__check_date(item[len("date_before")+1:], RequestFrom.default_date_before)
            if 0 == item.find("TrTypeRegular"):
                self.regular = 'checked'
            if 0 == item.find("TrTypeOther"):
                self.other = 'checked'
            if 0 == item.find("TrTypeOpen"):
                self.open = 'checked'
            if 0 == item.find("TrTypeLeague"):
                self.league = 'checked'
            if 0 == item.find("min_players"):
                self.min_players_count = RequestFrom.__check_min_players(item[len("min_players")+1:])
            if 0 == item.find("mach_threshold_for_full_matchup"):
                self.mach_threshold_for_full_matchup = RequestFrom.__check_mach_threshold_for_full_matchup(item[len("mach_threshold_for_full_matchup")+1:])
            if 0 == item.find("min_match_count"):
                self.min_match_count = RequestFrom.__check_min_match_count(item[len("min_match_count")+1:])
            if 0 == item.find("FullStat"):
                self.full_stat = 'checked'
            if 0 == item.find("Location"):
                self.location = item[len("Location")+1:]
                if self.location == 'all':
                    self.loc_all = 'selected'
                if self.location == 'Barnaul':
                    self.loc_Barnaul = 'selected'
                if self.location == 'Krasnodar':
                    self.loc_Krasnodar = 'selected'
                if self.location == 'Moscow':
                    self.loc_Moscow = 'selected'
                if self.location == 'Online':
                    self.loc_Online = 'selected'
                if self.location == 'RostovOnDon':
                    self.loc_RostovOnDon = 'selected'
                if self.location == 'Saratov':
                    self.loc_Saratov = 'selected'
                if self.location == 'Spb':
                    self.loc_Spb = 'selected'
                if self.location == 'Ussuriysk':
                    self.loc_Ussuriysk = 'selected'
                if self.location == 'Volgograd':
                    self.loc_Volgograd = 'selected'
                if self.location == 'Yekaterinburg':
                    self.loc_Yekaterinburg = 'selected'
            if 0 == item.find("SortType"):
                if "Name" == item[len("SortType")+1:]:
                    self.sort_type_name = 'checked'
                if "MatchesTot" == item[len("SortType") + 1:]:
                    self.sort_type_matches_tot = 'checked'
                if "WinMatches" == item[len("SortType") + 1:]:
                    self.sort_type_matches_win = 'checked'
                if "LoseMatches" == item[len("SortType") + 1:]:
                    self.sort_type_matches_loss = 'checked'
                if "DrawMatches" == item[len("SortType")+1:]:
                    self.sort_type_matches_draw = 'checked'
                if "GamesTot" == item[len("SortType")+1:]:
                    self.sort_type_games_tot = 'checked'
                if "WinGames" == item[len("SortType")+1:]:
                    self.sort_type_games_win = 'checked'
                if "LoseGames" == item[len("SortType")+1:]:
                    self.sort_type_games_loss = 'checked'
        self.date_after = date_after
        self.date_before = date_before
        if RequestFrom.first_time:
            RequestFrom.first_time = False
            self.league = 'checked'
            self.open = 'checked'
            self.regular = 'checked'
            self.other = 'checked'
            self.full_stat = ''
            self.sort_type_name = 'checked'
            self.min_players_count = 4
            self.min_match_count = 1
            self.location = 'all'
            self.loc_all = 'selected'
            self.loc_Barnaul = ''
            self.loc_Krasnodar = ''
            self.loc_Moscow = ''
            self.loc_Online = ''
            self.loc_RostovOnDon = ''
            self.loc_Saratov = ''
            self.loc_Spb = ''
            self.loc_Ussuriysk = ''
            self.loc_Volgograd = ''
            self.loc_Yekaterinburg = ''

    def get_sort_type(self):
        value = ''
        if self.sort_type_name == 'checked':
            value = 'name'
        if self.sort_type_matches_tot == 'checked':
            value = 'matches_total'
        if self.sort_type_matches_win == 'checked':
            value = 'matches_win'
        if self.sort_type_matches_loss == 'checked':
            value = 'matches_loss'
        if self.sort_type_matches_draw == 'checked':
            value = 'matches_draw'
        if self.sort_type_games_tot == 'checked':
            value = 'games_total'
        if self.sort_type_games_win == 'checked':
            value = 'games_win'
        if self.sort_type_games_loss == 'checked':
            value = 'games_loss'
        print(value)
        return value

    def get_params_to_filtration(self):
        return GetParams(date_after=self.date_after,
                         date_before=self.date_before,
                         open=True if self.open == 'checked' else False,
                         regular=True if self.regular == 'checked' else False,
                         other=True if self.other == 'checked' else False,
                         league=True if self.league == 'checked' else False,
                         full_stat=True if self.full_stat == 'checked' else False,
                         sort_type=self.get_sort_type(),
                         min_players=self.min_players_count,
                         min_match_count=self.min_match_count,
                         mach_threshold_for_full_matchup=self.mach_threshold_for_full_matchup,
                         location=self.location,
                         )

    def get_http_form(self):
        req_form = f'<form id="stat" action="">' \
                   f'<p> Date from: <input type="text" name="date_after" minlength="10" maxlength="10" value="{self.date_after}">' \
                   f'to: <input type="text" name="date_before" minlength="10" maxlength="10" value="{self.date_before}"></p>' \
                   f'<p><input type="checkbox" id="TrTypeRegular" name="TrTypeRegular" {self.regular}>' \
                   f'<label for="TrTypeRegular"> Regular</label>' \
                   f'<input type="checkbox" id="TrTypeOpen" name="TrTypeOpen" {self.open}>' \
                   f'<label for="TrTypeOpen"> Open</label>' \
                   f'<input type="checkbox" id="TrTypeLeague" name="TrTypeLeague" {self.league}>' \
                   f'<label for="TrTypeLeague"> League</label>' \
                   f'<input type="checkbox" id="TrTypeOther" name="TrTypeOther" {self.other}>' \
                   f'<label for="TrTypeLeague"> Other</label></p>' \
                   f'<label for="fruits">Choose location:</label>' \
                   f'<select id="Location" name="Location">' \
                   f'<option {self.loc_all} value="all">all</option>' \
                   f'<option {self.loc_Barnaul} value="Barnaul">Barnaul</option>' \
                   f'<option {self.loc_Krasnodar} value="Krasnodar">Krasnodar</option>' \
                   f'<option {self.loc_Moscow} value="Moscow">Moscow</option>' \
                   f'<option {self.loc_Online} value="Online">Online</option>' \
                   f'<option {self.loc_RostovOnDon} value="RostovOnDon">RostovOnDon</option>' \
                   f'<option {self.loc_Saratov} value="Saratov">Saratov</option>' \
                   f'<option {self.loc_Spb} value="Spb">Spb</option>' \
                   f'<option {self.loc_Ussuriysk} value="Ussuriysk">Ussuriysk</option>' \
                   f'<option {self.loc_Volgograd} value="Volgograd">Volgograd</option>'\
                   f'<option {self.loc_Yekaterinburg} value="Yekaterinburg">Yekaterinburg</option>' \
                   f'</select>' \
                   f'<p> Minimum players count in tournament: <input type="text" name="min_players" minlength="1" maxlength="2" value="{self.min_players_count}"></p>' \
                   f'<p> Show generals with match count more than: <input type="text" name="min_match_count" minlength="1" maxlength="3" value="{self.min_match_count}"></p>' \
                   f'<p> Show in full stat matchup with more than ~ matches: <input type="text" name="mach_threshold_for_full_matchup" minlength="1" maxlength="3" value="{self.mach_threshold_for_full_matchup}"></p>' \
                   f'<input type="checkbox" id="FullStat" name="FullStat" {self.full_stat}>' \
                   f'<label for="FullStat"> Full stat</label></p>' \
                   f'<button type="submit" name="Send">Send</button>' \
                   f'<p>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="Name" {self.sort_type_name}/><label for ="Name">-------------------------------------------</label>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="MatchesTot" {self.sort_type_matches_tot}/><label for="MatchesTot">---------------</label>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="WinMatches" {self.sort_type_matches_win}/><label for ="WinMatches">--------------</label>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="LoseMatches" {self.sort_type_matches_loss}/><label for ="LoseMatches">------------</label>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="DrawMatches" {self.sort_type_matches_draw}/><label for ="DrawMatches">-----------------------------------</label>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="GamesTot" {self.sort_type_games_tot}/><label for="GamesTot">--------------</label>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="WinGames" {self.sort_type_games_win}/><label for ="WinGames">--------------</label>' \
                   f'<input onchange="this.form.submit()" type="radio" id="" name="SortType" value="LoseGames" {self.sort_type_games_loss}/><label for ="LoseGames">------------------------</label>' \
                   f'</p>' \
                   f'</form>'
        return req_form

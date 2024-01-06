from reqForm import GetParams
from Source.Statistic import Statistic


def make_stat(get_params: GetParams, tournament_list):
    start_date = get_params.date_after
    finish_date = get_params.date_before
    stat = Statistic()
    for tournament in tournament_list:
        if tournament.before_date(finish_date) and tournament.after_date(start_date):
            if (tournament.level == 'Regular' and get_params.regular) or \
               (tournament.level == 'Open' and get_params.open) or \
               (tournament.level == 'Other' and get_params.other) or \
               (tournament.level == 'League' and get_params.league):
                if len(tournament.players) >= get_params.min_players:
                    stat.add_tournament(tournament, get_params.exclude_generals)
    for_delete = []
    for elem in stat.generalStat.values():
        if elem.matches_total < get_params.min_match_count:
            for_delete.append(elem.general)
    for item in for_delete:
        del stat.generalStat[item]
    return stat

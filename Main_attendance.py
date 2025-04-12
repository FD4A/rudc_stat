import argparse
from glob import glob

from Source.Tournament import Tournament

def update_visit_list(tournament, VisitList):
    for item in tournament.players:
        player = item[0]
        if player not in VisitList:
            VisitList[player] = 1
        else:
            VisitList[player] += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser('RuDcStat')
    parser.add_argument('--tournament_folder', default='tournaments_json')
    parser.add_argument('--start_date', default='2024_12_07')  # 0000_00_00 2024_09_00 2024_12_07
    parser.add_argument('--finish_date', default='9999_99_99')
    args = parser.parse_args()

    tournament_dir = './' + args.tournament_folder
    start_date = args.start_date
    finish_date = args.finish_date

    tournament_list = glob(tournament_dir + '/*.json')

    VisitList = {}
    tournament_filenames = []
    for tournament_filename in tournament_list:
        tournament = Tournament.load_from_json(tournament_filename)
        if tournament.location != 'Spb':
            continue
        if not (tournament.before_date(finish_date) and tournament.after_date(start_date)):
            continue
        tournament_filenames.append(f'{tournament_filename.replace("./tournaments_json/",""):64} {tournament.url}')
        # print(tournament_filename)
        update_visit_list(tournament, VisitList)

    tournament_filenames.sort()
    for item in tournament_filenames:
        print(f"{item}")

    print(f" ")
    VisitList = dict(sorted(VisitList.items(), key=lambda item: item[1], reverse=True))
    for item in VisitList:
        print(f"{item}:{VisitList[item]}")

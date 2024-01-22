import argparse
from glob import glob


from Source.Statistic import Statistic
from Source.Tournament import Tournament
from Source.LegendaryBase import LegendaryBase


if __name__ == '__main__':
    parser = argparse.ArgumentParser('RuDcStat')
    parser.add_argument('--tournament_folder', default='tournaments_json')
    parser.add_argument('--statistic_folder', default='statistic_json')
    parser.add_argument('--start_date', default='0000_00_00')  # 0000_00_00 2023_11_08
    parser.add_argument('--finish_date', default='9999_99_99')
    parser.add_argument('--out_path', default='./Stat/')
    args = parser.parse_args()

    tournament_dir = './' + args.tournament_folder
    stat_dir = args.statistic_folder
    start_date = args.start_date
    finish_date = args.finish_date
    out_path = args.out_path

    tournament_list = glob(tournament_dir + '/*.json')

    stat = Statistic()
    lb = LegendaryBase('./ScryfallData')

    save_date = []
    save_name = []
    for tournament_filename in tournament_list:
        tournament = Tournament.load_from_json(tournament_filename)
        # in json must be already fixed names
        # [ok, error_string] = tournament.fix_generals_names(lb)
        # if not ok:
        #     print(f"Fail check general names for tournament [{tournament_filename}]")
        #     print(error_string)
        #     exit(1)

        one_tournament_stat = Statistic()
        one_tournament_stat.add_tournament(tournament, [])
        one_stat_str = f"{one_tournament_stat}"
        with open(f"{stat_dir}/{tournament.form_stat_filename()}", 'w', encoding='utf-8') as fd:
            fd.write(one_stat_str)

        if tournament.before_date(finish_date) and tournament.after_date(start_date):
            stat.add_tournament(tournament, [])
            save_date.append(tournament.date)

    suffix_date = '_from_'+start_date if start_date != parser.get_default('start_date') else ''
    suffix_date = suffix_date + '_to_'+finish_date if finish_date != parser.get_default('finish_date') else ''
    if suffix_date == '':
        [min_date, max_date] = Tournament.get_min_max_date(save_date)
        suffix_date = f"_from_{min_date}_to_{max_date}"

    stat_tr_names = stat.get_tournaments_names()
    with open(f"{out_path}/Stat_full_{suffix_date}.txt", 'w', encoding='utf-8') as fd:
        fd.write(stat_tr_names)
        stat_str = f"{stat}"
        fd.write(stat_str)

    with open(f"{out_path}/Stat_short_{suffix_date}.txt", 'w', encoding='utf-8') as fd:
        fd.write(stat_tr_names)
        stat_str = stat.to_str(sort_type='name', full=False)
        fd.write(stat_str)

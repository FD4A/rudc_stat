from glob import glob

from Source.ParseRawTxtCommon import ParseRawTxtCommon
from Source.LegendaryBase import LegendaryBase


legendary_base = LegendaryBase('./ScryfallData')
out_folder = './tournaments_json/'

# # online league
# filenames = glob('./RawData/OnlineLeague/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_league, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     tournament.dump_to_json(out_folder)
#
# # Krasnodar data
# filenames = glob('./RawData/Krasnodar_data/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_Krasnodar, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     tournament.dump_to_json(out_folder)

# Spb data
filenames = glob('RawData/Spb_data/2024*.txt')
for filename in filenames:
    parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
    tournament = parser.get_tournament_from_txt(filename)
    print(tournament)
    tournament.dump_to_json(out_folder)

# # Ussuriysk_data data
# filenames = glob('RawData/Ussuriysk_data/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)
#
# # RostovOnDon_data data
# filenames = glob('RawData/RostovOnDon_data/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)
#
# # RostovOnDon_data data
# filenames = glob('RawData/Volgograd_data/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

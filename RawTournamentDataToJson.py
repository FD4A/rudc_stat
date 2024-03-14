from glob import glob

from Source.ParseRawTxtCommon import ParseRawTxtCommon
from Source.LegendaryBase import LegendaryBase


legendary_base = LegendaryBase('./ScryfallData')
out_folder = './tournaments_json/'

# online league
# filenames = glob('RawData/OnlineLeague/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_league, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     tournament.dump_to_json(out_folder)

# # Krasnodar data
# filenames = glob('./RawData/Krasnodar_data/Krasnodar_2024_01_28.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_Krasnodar, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# Spb data
filenames = glob('RawData/Spb_data/2024_03_14*.txt')
for filename in filenames:
    parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
    tournament = parser.get_tournament_from_txt(filename)
    print(tournament)
    tournament.dump_to_json(out_folder)

# # Ussuriysk_data data
# filenames = glob('RawData/Ussuriysk_data/2024_03_02_Ussuriysk_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Volgograd data
# filenames = glob('RawData/Volgograd_data/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)
#

# # RostovOnDon_data data
# filenames = glob('RawData/RostovOnDon_data/2024_03_03*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Barnaul_data data
# filenames = glob('RawData/Barnaul_data/2024_02_09_Barnaul_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

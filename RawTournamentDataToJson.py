from glob import glob

from Source.ParseRawTxtCommon import ParseRawTxtCommon
from Source.LegendaryBase import LegendaryBase


legendary_base = LegendaryBase('./ScryfallData')
out_folder = './tournaments_json/'

# # online league
# filenames = glob('RawData/OnlineLeague/Spring_Deadly_Rollick_FOIL_League_2024.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_league, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     tournament.dump_to_json(out_folder)

# # Krasnodar data
# filenames = glob('./RawData/Krasnodar_data/Krasnodar_2024_06_09.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_Krasnodar, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Saratov data
# filenames = glob('./RawData/Saratov_data/*.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Spb data
# filenames = glob('RawData/Spb_data/2024_07_11_Spb_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# Moscow data
# filenames = glob('RawData/Moscow_data/2024_03_24_Moscow_Open_Swiss.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Ussuriysk_data data
# filenames = glob('RawData/Ussuriysk_data/2024_07_07_Ussuriysk_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# Volgograd data
filenames = glob('RawData/Volgograd_data/2024_07_14_Volgograd_Regular.txt')
for filename in filenames:
    parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
    tournament = parser.get_tournament_from_txt(filename)
    print(tournament)
    tournament.dump_to_json(out_folder)

# # RostovOnDon_data data
# filenames = glob('RawData/RostovOnDon_data/2024_06_29_RostovOnDon_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Barnaul_data data
# filenames = glob('RawData/Barnaul_data/2024_06_20_Barnaul_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Yekaterinburg data (TOPDECK)
# filenames = glob('RawData/Yekaterinburg_data/2024_06_23_Yekaterinburg_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_topdeckGG, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Yekaterinburg data (AHUB)
# filenames = glob('RawData/Yekaterinburg_data/2024_06_23_Yekaterinburg_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

# # Novorossiysk_data data
# filenames = glob('RawData/Novorossiysk/2024_06_14_Novorossiysk_Regular.txt')
# for filename in filenames:
#     parser = ParseRawTxtCommon(ParseRawTxtCommon.parser_aetherhub, legendary_base)
#     tournament = parser.get_tournament_from_txt(filename)
#     print(tournament)
#     tournament.dump_to_json(out_folder)

Stat - статистика генералов в формате Russian Duel Commander. За различные даты и с различными фильтрами.

https://docs.google.com/spreadsheets/d/1DvFNChZnR7nNllr1f1KuMhM9f5BAowict7X3iPGXR3E/edit#gid=1969611537 - данные в гугл таблицах.

statistic_json - статистика сформированная по каждому отдельному турниру.

tournaments_json - турниры приведённые к обобщённому виду.

RawData - первичные данные о турнирах по которым происходит обработка.

ScryFallData - различные артефакты от парсинга scryfall. В частности файл по которому сверяются имена генералов для
автоматического исправления опечаток.

Source - питоновские исходники.

Main_FormStatFromTournamentsJson.py - конвертация турниров, приведённых к обобщённому виду в статистику.

ParseScryfallLegendary.py - парсинг scryfall.

RawTournamentDataToJson.py - конвертация RawData в обобщённый вид турниров.

Server - попытка запилить сервер, который будет отдавать статистику по заданным критериям фильтрации.

str_list_ = [
"""Поляков Герман :: G'Raha, Scion Reborn
Мещеряков Максим :: Kefka, Court Mage
Циулин Иван :: Azusa, Lost but Seeking
Матюнин Антон :: Taii Waiki Perfect Shot
Майоров Влад :: Grist, the Hunger Tide
Павликов Владислав :: Hidetsugu and Kairi
Третьяков Дмитрий :: Flubs, the Fool
Сайфутдинов Тимур :: Yoshimaru, Ever Faithful :+: Kraum, Ludevic's Opus
Кузьмин Руслан :: Tifa Lockhart
Ревин Владимир :: Cecil, Dark Knight
Стрельцов Артем :: Bruse Tarl, Boorish Herder :+: Thrasios, Triton Hero
Костин Андрей :: Imskir Iron-Eater
Барабаш Валентин :: Mm'menon, the Right Hand
Лагерев Леонид :: Slimefoot and Squee
Булочко Михаил :: Iron Man, Titan of Innovation
Дартау Сергей :: Phelia, Exuberant Shepherd"""
]

# print(str_list_)
str_list = str_list_[0].split('\n')
# print(str_list)

for i in range(len(str_list)):
    str_list[i] = str_list[i].split(' :: ')
# str_list.sort(key=lambda x: x[1], reverse=False)
# for i in range(len(str_list)):
#     print(str_list[i][1])

str_list_new = []
for i in range(len(str_list)):
    str_list_new.append(str_list[i][1])
# print(str_list_new)

str_list_new2 = []
for i in range(len(str_list_new)):
    str_list_new2.append(str_list_new.count(str_list_new[i]))

str_list_new3 = []
for i in range(len(str_list_new)):
    str_list_new3.append([str_list_new[i], str_list_new2[i]])
str_list_new3.sort(key=lambda x: (-x[1], x[0]))
# str_list_new3.sort(key=lambda x: x[0], reverse=False)

data = {}
for i in range(len(str_list_new3)):
    data.update({str_list_new3[i][0]: str_list_new3[i][1]})
# s = set(str_list_new3)
# print(data)

sum = 0
for k, v in data.items():
    print(v, k)
    sum += v
print(sum)


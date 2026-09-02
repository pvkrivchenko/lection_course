# Напишите генератор generate_random_name(), используя модуль random,
# который генерирует два слова из латинских букв от 1 до 15 символов, разделенных пробелами
# Например при исполнении следующего кода:
# gen = generate_random_name()
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
#
# Выводится:
# tahxmckzexgdyt ocapwy
# dxqebbukr jg
# aym jpvezfqexlv
# iuy qnikkgxvxfxtxv

import random

# Здесь пишем код


def generate_random_name():
    """
    Генератор случайных имён.

    Эта функция является генератором, который бесконечно генерирует случайные имена,
    состоящие из двух слов, разделённых пробелом. Каждое слово создаётся из
    случайного набора букв английского алфавита и имеет длину от 1 до 15 символов.
    """
    alfavit = 'abcdefghijklmnopqrstuvwxyz'
    while True:
        word1 = ''.join(random.choice(alfavit) for _ in range(random.randint(1, 15)))
        word2 = ''.join(random.choice(alfavit) for _ in range(random.randint(1, 15)))
        yield f"{word1} {word2}"


gen = generate_random_name()

print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
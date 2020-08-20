from math import ceil

from numpy.random import randint


def rangeToStr(x, y): return ' '.join(map(str, range(x, y)))


def generateTasks(n):
    with open(f'instances/{n}.txt', 'w') as file:
        file.write(f'{n}\n')
        for _ in range(n):
            p = randint(1, 15)  # processing time
            r = randint(0, 2 * n)  # ready time
            d = r + p + randint(0, p)  # due time
            file.write(f'{p} {r} {d}\n')


def generateResults(n):
    with open(f'{n}.txt', 'w') as file:
        file.write(f'0\n')
        q = ceil(n / 4)
        for i in range(3):
            file.write(rangeToStr(q * i + 1, q * (i + 1) + 1) + '\n')
            file.write(rangeToStr(q * 3 + 1, n + 1))


def generateAllTasks():
    for n in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
        generateTasks(n)


def generateAllResults():
    for n in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
        generateResults(n)

from dataclasses import dataclass


def load_line(file):
    return [int(i) for i in file.readline().strip().split(' ')]


@dataclass
class Task:
    p: int  # processing time
    r: int  # ready time
    d: int  # due time
    i: int  # id


# I had to write my own argmin and argmax functions as we
# weren't allowed to used any of non-built-in libs like numpy
def argmin(arr):
    return min(enumerate(arr), key=lambda x: x[1])[0]


def argmax(arr):
    return max(enumerate(arr), key=lambda x: x[1])[0]

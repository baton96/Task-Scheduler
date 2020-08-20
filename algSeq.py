import sys
from dataclasses import dataclass


@dataclass
class Task:
    p: int  # processing time
    r: int  # ready time
    d: int  # due time
    i: int  # id


def loadLine(file):
    return [int(i) for i in file.readline().strip().split(' ')]


# I had to write my own argmin and argmax functions as we
# weren't allowed to used any of non-built-in libs like numpy
def argmin(arr):
    return min(enumerate(arr), key=lambda x: x[1])[0]


def algList():
    with open(sys.argv[1], 'r') as file:
        n = loadLine(file)[0]
        tasks = [Task(i=i, *loadLine(file)) for i in range(n)]
    tasks = sorted(tasks, key=lambda x: x.r)

    awaiting = []
    schedules = [[], [], [], []]
    timers = [0, 0, 0, 0]
    criterium = 0
    counter = 0
    it = 0

    while True:
        timerId = argmin(timers)
        if it != n:
            for i in range(it, n):
                if tasks[i].r <= timers[timerId]:
                    awaiting += [tasks[i]]
                else:
                    it = i
                    break
            else:
                it = n
        if not awaiting:
            timers[timerId] = tasks[it].r
            for i in range(it, n):
                if tasks[i].r <= timers[timerId]:
                    awaiting += [tasks[i]]
                else:
                    it = i
                    break
            else:
                it = n
        awaiting.sort(key=lambda x: (min(0, timers[timerId] + x.p - x.d), -x.p))
        popped = awaiting.pop()
        schedules[timerId] += [popped]
        timers[timerId] = max(timers[timerId], popped.r) + popped.p
        criterium += max(0, timers[timerId] - popped.d)
        counter += 1
        if counter == n:
            break

    with open(sys.argv[2], 'w') as output:
        output.write(
            str(criterium) + '\n' +
            '\n'.join([
                ' '.join([
                    str(task.i + 1) for task in schedule
                ]) for schedule in schedules
            ])
        )


algList()

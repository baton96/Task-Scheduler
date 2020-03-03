from copy import deepcopy
from time import time
import sys

def loadLine(file):
    return [int(i) for i in file.readline().strip().split(' ')]

def argmin(arr, key=lambda x: x[1]):
    return min(enumerate(arr), key=key)[0]

def argmax(arr, key=lambda x: x[1]):
    return max(enumerate(arr), key=key)[0]

def algList():
    with open(sys.argv[1], 'r') as file:
        n = loadLine(file)[0]
        tasks = [loadLine(file) + [i] for i in range(n)]
    tasks = sorted(tasks, key=lambda x: x[1])

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
                if tasks[i][1] <= timers[timerId]:
                    awaiting += [tasks[i]]
                else:
                    it = i
                    break
            else:
                it = n
        if not awaiting:
            timers[timerId] = tasks[it][1]
            for i in range(it, n):
                if tasks[i][1] <= timers[timerId]:
                    awaiting += [tasks[i]]
                else:
                    it = i
                    break
            else:
                it = n
        awaiting.sort(key=lambda x: (min(0, timers[timerId] + x[0] - x[2]), -x[0]))
        popped = awaiting.pop()
        schedules[timerId] += [popped]
        timers[timerId] = max(timers[timerId], popped[1])  + popped[0]
        criterium += max(0, timers[timerId] - popped[2])
        counter += 1
        if counter == n:
            break

    with open(sys.argv[2], 'w') as output:
        output.write(
            str(criterium) + '\n' +
            '\n'.join([
                ' '.join([
                        str(task[3] + 1) for task in schedule
                    ]) for schedule in schedules
            ])
        )

algList()
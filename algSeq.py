import sys

from utils import argmin, loadLine, Task


def algList():
    with open(sys.argv[1], 'r') as file:
        n = loadLine(file)[0]
        tasks = [Task(*loadLine(file), i) for i in range(n)]
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

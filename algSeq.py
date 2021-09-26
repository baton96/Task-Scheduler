from utils import argmin, load_line, Task
import sys


def alg_list():
    with open(sys.argv[1], 'r') as file:
        n = load_line(file)[0]
        tasks = [Task(*load_line(file), i) for i in range(n)]
    tasks = sorted(tasks, key=lambda task: task.r)

    schedules = [[], [], [], []]
    timers = [0, 0, 0, 0]
    criterium = 0
    awaiting = []
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
        awaiting.sort(key=lambda task: (min(0, timers[timerId] + task.p - task.d), -task.p))
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


alg_list()

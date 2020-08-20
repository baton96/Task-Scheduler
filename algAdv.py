import sys
from copy import deepcopy
from time import time


def loadLine(file):
    return [int(i) for i in file.readline().strip().split(' ')]


def argmin(arr, key=lambda x: x[1]):
    return min(enumerate(arr), key=key)[0]


def argmax(arr, key=lambda x: x[1]):
    return max(enumerate(arr), key=key)[0]


def verify(schedules, env):
    result = 0
    for schedule in schedules:
        timer = 0
        for taskId in (i[3] + 1 for i in schedule):
            task = env['originalTasks'][taskId - 1]
            timer = max(timer, task[1]) + task[0]
            result += max(0, timer - task[2])
    return result


def algAdv(forbidden, env):
    schedules = deepcopy(env['schedules'])
    awaiting = deepcopy(env['awaiting'])
    started = deepcopy(env['started'])
    timers = deepcopy(env['timers'])
    counter = env['counter']
    n = env['n']
    applyForbidden = True
    while True:
        if applyForbidden:
            applyForbidden = False
            timerId = argmin([timer for timer in timers if timer != timers[forbidden]] or [0])
        else:
            timerId = argmin(timers)
        if (time() - env['start']) * 100 > env['n']: return
        ready = [task for task in awaiting if task[1] <= timers[timerId]]
        if not ready:
            popped = min(
                [task for task in awaiting if task[1] > timers[timerId]],
                key=lambda x: x[1]
            )
            timers[timerId] = popped[1]
        else:
            popped = max(
                ready,
                key=lambda x: (min(0, timers[timerId] + x[0] - x[2]), -x[0])
            )
        awaiting.remove(popped)
        schedules[timerId] += [popped]
        actualStart = max(timers[timerId], popped[1])
        started[timerId] += [actualStart]
        timers[timerId] = actualStart + popped[0]
        counter += 1
        if counter == n:
            criterium = verify(schedules, env)
            if criterium < env['bestCriterium']:
                env['bestCriterium'] = criterium
                env['bestSchedules'] = deepcopy(schedules)
                env['schedules'] = schedules
                env['started'] = started
                env['awaiting'] = []
                env['counter'] = counter
                env['timers'] = timers
                env['break'] = True
            return


def algList():
    env = {'start': time(), 'break': False}
    with open(sys.argv[1], 'r') as file:
        n = loadLine(file)[0]
        env['originalTasks'] = [loadLine(file) + [i] for i in range(n)]
    tasks = sorted(env['originalTasks'], key=lambda x: x[1])

    awaiting = []
    schedules = [[], [], [], []]
    started = [[], [], [], []]
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
        started[timerId] += [max(timers[timerId], popped[1])]
        timers[timerId] = max(timers[timerId], popped[1]) + popped[0]
        criterium += max(0, timers[timerId] - popped[2])
        counter += 1
        if counter == n:
            break

    env['bestCriterium'] = criterium
    env['bestSchedules'] = deepcopy(schedules)
    env['schedules'] = schedules
    env['started'] = started
    env['awaiting'] = []
    env['counter'] = counter
    env['timers'] = timers
    env['n'] = n

    while True:
        for _ in range(env['n']):
            poppedId = argmax(j[-1] if j else -1 for j in env['started'])
            popped = env['schedules'][poppedId].pop()
            env['started'][poppedId].pop()
            env['awaiting'] += [popped]
            if env['started'][poppedId]:
                env['timers'][poppedId] = env['started'][poppedId][-1] + env['schedules'][poppedId][-1][0]
            else:
                env['timers'][poppedId] = 0
            env['counter'] -= 1
            algAdv(poppedId, env)
            if env['break']:
                env['break'] = False
                break
            if (time() - env['start']) * 100 > env['n']:
                with open(sys.argv[2], 'w') as output:
                    output.write(str(env['bestCriterium']) + '\n' +
                                 '\n'.join([' '.join([str(i[3] + 1) for i in schedule]) for schedule in
                                            env['bestSchedules']]))
                return
        else:
            with open(sys.argv[2], 'w') as output:
                output.write(str(env['bestCriterium']) + '\n' +
                             '\n'.join(
                                 [' '.join([str(i[3] + 1) for i in schedule]) for schedule in env['bestSchedules']]))
            return


algList()

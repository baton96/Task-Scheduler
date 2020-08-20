import sys
from copy import deepcopy
from time import time

from utils import argmax, argmin, loadLine, Task


def verify(schedules, env):
    result = 0
    for schedule in schedules:
        timer = 0
        for taskId in (i.i + 1 for i in schedule):
            task = env['originalTasks'][taskId - 1]
            timer = max(timer, task.r) + task.p
            result += max(0, timer - task.d)
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
        ready = [task for task in awaiting if task.r <= timers[timerId]]
        if not ready:
            popped = min(
                [task for task in awaiting if task.r > timers[timerId]],
                key=lambda x: x.r
            )
            timers[timerId] = popped.r
        else:
            popped = max(
                ready,
                key=lambda x: (min(0, timers[timerId] + x.p - x.d), -x.p)
            )
        awaiting.remove(popped)
        schedules[timerId] += [popped]
        actualStart = max(timers[timerId], popped.r)
        started[timerId] += [actualStart]
        timers[timerId] = actualStart + popped.p
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
        env['originalTasks'] = [Task(*loadLine(file), i) for i in range(n)]
    tasks = sorted(env['originalTasks'], key=lambda x: x.r)

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
        started[timerId] += [max(timers[timerId], popped.r)]
        timers[timerId] = max(timers[timerId], popped.r) + popped.p
        criterium += max(0, timers[timerId] - popped.d)
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
                env['timers'][poppedId] = env['started'][poppedId][-1] + env['schedules'][poppedId][-1].p
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

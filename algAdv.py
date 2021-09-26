from utils import argmax, argmin, load_line, Task
from copy import deepcopy
from time import time
import sys


def verify(schedules, env):
    result = 0
    for schedule in schedules:
        timer = 0
        for task_id in (task.i + 1 for task in schedule):
            task = env['originalTasks'][task_id - 1]
            timer = max(timer, task.r) + task.p
            result += max(0, timer - task.d)
    return result


def alg_adv(forbidden, env):
    schedules = deepcopy(env['schedules'])
    awaiting = deepcopy(env['awaiting'])
    started = deepcopy(env['started'])
    timers = deepcopy(env['timers'])
    counter = env['counter']
    n = env['n']
    apply_forbidden = True
    while True:
        if apply_forbidden:
            timer_id = argmin([timer for timer in timers if timer != timers[forbidden]] or [0])
            apply_forbidden = False
        else:
            timer_id = argmin(timers)
        if (time() - env['start']) * 100 > env['n']:
            return
        ready = [task for task in awaiting if task.r <= timers[timer_id]]
        if ready:
            popped = max(
                ready,
                key=lambda task: (min(0, timers[timer_id] + task.p - task.d), -task.p)
            )
        else:
            popped = min(
                [task for task in awaiting if task.r > timers[timer_id]],
                key=lambda task: task.r
            )
            timers[timer_id] = popped.r
        awaiting.remove(popped)
        schedules[timer_id] += [popped]
        actual_start = max(timers[timer_id], popped.r)
        started[timer_id] += [actual_start]
        timers[timer_id] = actual_start + popped.p
        counter += 1
        if counter == n:
            criterium = verify(schedules, env)
            if criterium < env['bestCriterium']:
                env.update({
                    'bestSchedules': deepcopy(schedules),
                    'bestCriterium': criterium,
                    'schedules': schedules,
                    'started': started,
                    'counter': counter,
                    'timers': timers,
                    'awaiting': [],
                    'break': True
                })
            return


def save_results(env):
    with open(sys.argv[2], 'w') as output:
        output.write(
            str(env['bestCriterium']) + '\n' +
            '\n'.join([' '.join([str(i[3] + 1) for i in schedule]) for schedule in env['bestSchedules']])
        )


def alg_list():
    env = {'start': time(), 'break': False}
    with open(sys.argv[1], 'r') as file:
        n = load_line(file)[0]
        env['originalTasks'] = [Task(*load_line(file), i) for i in range(n)]
    tasks = sorted(env['originalTasks'], key=lambda x: x.r)

    schedules = [[], [], [], []]
    started = [[], [], [], []]
    timers = [0, 0, 0, 0]
    criterium = 0
    awaiting = []
    counter = 0
    it = 0

    while True:
        timer_id = argmin(timers)
        if it != n:
            for i in range(it, n):
                if tasks[i].r <= timers[timer_id]:
                    awaiting += [tasks[i]]
                else:
                    it = i
                    break
            else:
                it = n
        if not awaiting:
            timers[timer_id] = tasks[it].r
            for i in range(it, n):
                if tasks[i].r <= timers[timer_id]:
                    awaiting += [tasks[i]]
                else:
                    it = i
                    break
            else:
                it = n
        awaiting.sort(key=lambda x: (min(0, timers[timer_id] + x.p - x.d), -x.p))
        popped = awaiting.pop()
        schedules[timer_id] += [popped]
        started[timer_id] += [max(timers[timer_id], popped.r)]
        timers[timer_id] = max(timers[timer_id], popped.r) + popped.p
        criterium += max(0, timers[timer_id] - popped.d)
        counter += 1
        if counter == n:
            break
    env.update({
        'bestSchedules': deepcopy(schedules),
        'bestCriterium': criterium,
        'schedules': schedules,
        'started': started,
        'counter': counter,
        'timers': timers,
        'awaiting': [],
        'n': n
    })

    while True:
        for _ in range(env['n']):
            popped_id = argmax(j[-1] if j else -1 for j in env['started'])
            popped = env['schedules'][popped_id].pop()
            env['started'][popped_id].pop()
            env['awaiting'] += [popped]
            if env['started'][popped_id]:
                env['timers'][popped_id] = env['started'][popped_id][-1] + env['schedules'][popped_id][-1].p
            else:
                env['timers'][popped_id] = 0
            env['counter'] -= 1
            alg_adv(popped_id, env)
            if env['break']:
                env['break'] = False
                break
            if (time() - env['start']) * 100 > env['n']:
                save_results(env)
                return
        else:
            save_results(env)
            return


alg_list()

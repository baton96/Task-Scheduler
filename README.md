# SHORT VERSION
My task scheduling algorithms produced the best results for **_xx/xx (xx%)_** of the input instances among all sequential (assigning tasks one by one) algorithms and for yy/yy (yy%)  of the input instances among all advanced (allowing post-optimization) algorithms proposed by my x colleagues in laboratory group.
# LONG VERSION
# GOAL
Our goal was to propose an algorithm assigning n indivisible tasks Tj (described by the duration pj, ready time rj and expected finish time dj) to 4 identical, parallel machines and determining the order of their execution on the machines minimizing the sum of delays ΣDj between expected finish time dj and actual finish time Cj given the formula Dj = max(0, Cj-dj). In order to compare algorithms proposed within my group we had to standardize their input and output format.
# INPUT
First we had to generate instances and save it in a text file with the following format:
```
n
p1 r1 d1
p2 r2 d2
… … …
pn rn dn
```
(number of tasks n in the first line the and in every other line duration pj, ready time rj and expected finish time dj separated by a spaces)

Each person in my group generated (and made available to everyone) 10 instances of the problem for the number of tasks n equal to 50, 100, 150, 200, 250, 300, 350, 400, 450 and 500.
# OUTPUT
Our algorithms had to return a solution in the form of a text file with the following format:
```
ΣDj
T1.1 T1.2 …
T2.1 T2.2 …
T3.1 T3.2 …
T4.1 T4.2 …
```
(sum of delays in the first line and in the next 4 lines task sequences assigned to each machine, separated by spaces separated by spaces where tasks are represented by the line number of their appearance in the input file)
# VERIFIER
In order to to verify correctness (correct sum of delays for the given instance and schedule) of the solution we had to propose veryfier.
# BASE ALGORITHM
Base algorithm had to return solution containing all the tasks in the ascending order divided in a way that first three machines are assigned with ⌈n/4⌉ tasks and last machine with remaining tasks. Solution has to start with the sum of delays Dj, in the first line, calculated for the given instance and schedule. Solution for n=10 looks as follows: 
```
ΣDj
1 2 3
4 5 6
7 8 9
10
```
# SEQUENTIAL ALGORITHM
Sequential algorithm had to be a simple heuristic performing n iterations while selecting one task from the set of an unscheduled tasks in each iteration and assigning it to the one of the machines. Algorithm design had to include a proposal of a way how to organize and select tasks. As a report we had to provide a brief description of the algorithm, in particular the description of the task selection rules and the machine selection rules. My sequential algorithm works as follows:
1. Load input instance
2. Sort tasks by their ready time in ascending order
3. Enter infinite loop
4. **_Choose machine with the earliest ready time (ready to start next task)_**
5. Gather in an awaiting queue tasks ready at the moment of chosen machine’s ready time
6. If there are no tasks in the awaiting queue set the ready time of the chosen machine to the ready time of the task, which will be ready the soonest within unscheduled tasks, and again gather in an awaiting queue tasks ready at the new moment of chosen machine’s ready time
7. **_Within awaiting tasks assign to the chosen machine task with the highest potential delay and if multiple tasks have the same potential delay choose the shortest one_**
8. Shift the ready time of the chosen machine by the duration of the assigned task
9. If all the tasks have been assigned exit the loop, otherwise go to the beginning of the loop
10. Save the assignments to the output file and exit

In a report we had to present a table containing results of the sequential algorithm (sum of delays SEQ and runtime in ms) and comparison with the base algorithm results BASE for the generated instances. My table of results looks as follows:
n | runtime | SEQ | BASE | (BASE–SEQ)/SEQ*100% |
- | - | - | - | - |
50 | 2 | 68 | 2475 | 3539,71%
100 | 3 | 596 | 14356 | 2308,72%
150 | 4 | 297 | 30621 | 10210,10%
200 | 5 | 355 | 62750 | 17576,06%
250 | 7 | 1338 | 105479 | 7783,33%
300 | 8 | 1818 | 140465 | 7626,35%
350 | 9 | 1081 | 199317 | 18338,21%
400 | 10 | 1979 | 274755 | 13783,53%
450 | 11 | 3707 | 346451 | 9245,86%
500 | 13 | 2809 | 408297 | 14435,32%

We also had to provide total runtime (**_72 ms_**) and the average value of the last column (**_10484,72%_**).
# ADVANCED ALGORITHM
Our advanced algorithm could be any algorithm that solves the analyzed problem including algorithms optimizing solutions obtained from sequential algorithm.  One of the restrictions was that algorithm had to work within the 10*n ms time limit where n is the number of tasks. Advanced algorithm chosen by me was based on a Tabu search, because in every optimizing iteration I forbid one move (assigning given task to a given machine). My advanced algorithm works as follows:
1. Follow steps 1-9 of the sequential algorithm
2. Save in the memory information about the context of the obtained solution such as assignments, awaiting queue, machine ready times and task start times
3. For each task (from the latest to the earliest start time) create a copy of the context of the obtained solution so that it corresponds to the situation before the given task was assigned and then follow the sequential algorithm steps in the given context forbidding selection of the originally used machine in the first iteration
4. If the sum of delays for the new solution is smaller than the current minimum, overwrite current minimum with the new solution
5. If the runtime limit of 10*n ms, where n is the number of tasks, has been exceeded save the best assignments to the output file and exit

In a report we had to present a table containing results of the advanced algorithm (sum of delays ADV and runtime in ms) and comparison with the sequential algorithm results SEQ for the generated instances. My table of results looks as follows:
n | runtime | ADV | SEQ | (SEQ–ADV)/ADV*100%
- | - | - | - | -
50 | 156 | 61 | 68 | 11,48%
100 | 733 | 455 | 596 | 30,99%
150 | 1512 | 283 | 297 | 4,95%
200 | 2010 | 306 | 355 | 16,01%
250 | 2365 | 1066 | 1338 | 25,52%
300 | 3002 | 1379 | 1818 | 31,83%
350 | 3507 | 850 | 1081 | 27,18%
400 | 4013 | 1503 | 1979 | 31,67%
450 | 4504 | 2760 | 3707 | 34,31%
500 | 5014 | 2145 | 2809 | 30,96%

We also had to provide total runtime (**_26,816 s_**) and the average value from of last column (**_24,49%_**).

# TESTS
# TODO
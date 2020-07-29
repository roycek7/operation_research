"""
Minimal Studying
In order to graduate from State University, Angie Warner needs to pass at least one of the three subjects she is taking
this semester. She is now enrolled in Algebra, Calculus, and Statistics. Angie’s busy schedule of extra-curricular
activities allows her to spend only 4 hours per week on studying. Angie's probability of passing each course depends
on the number of hours she spends studying for the course, as follows:
                            Probability of Passing
Hours of study per week     Algebra Calculus Statistics
0                            .20      .25       .10
1                            .30      .30       .30
2                            .35      .33       .40
3                            .38      .35       .45
4                            .40      .38       .50


How many hours per week Angie should spend studying each subject.

"""
passprob = [
    [0.2, 0.3, 0.35, 0.38, 0.4],
    [0.25, 0.3, 0.33, 0.35, 0.38],
    [0.1, 0.3, 0.4, 0.45, 0.5],
]


def MinFail(j, s):
    if j == 2:
        return 1 - passprob[j][s], s, 0
    else:
        return min(((1 - passprob[j][a]) * MinFail(j + 1, s - a)[0], a, s - a) for a in range(0, s + 1))


def MinFailSolution():
    s = 4
    for j in [0, 1, 2]:
        v = MinFail(j, s)
        print(v[1], 'hours for subject', j)
        s = v[2]


MinFailSolution()

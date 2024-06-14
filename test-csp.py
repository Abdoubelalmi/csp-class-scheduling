import numpy as np
import time
import random
from tabulate import tabulate

# New data provided
MODULES = [
    'Securite_lecture', 'Securite_td', 'Methodes_formelles_lecture', 'Methodes_formelles_td',
    'Analyse_numerique_lecture', 'Analyse_numerique_td', 'Entrepreneuriat_lecture',
    'Recherche_operationnelle_lecture', 'Recherche_operationnelle_td',
    'Distributed_architecture_lecture', 'Distributed_architecture_td',
    'Reseaux_lecture', 'Reseaux_td', 'Reseaux_tp', 'AI_lecture', 'AI_td', 'AI_tp'
]

TEACHERS = {
    'Mme. Zaidi': ['Reseaux_tp'],
    'Dr. Issadi': ['Recherche_operationnelle_lecture', 'Recherche_operationnelle_td'],
    'Dr. Zedek': ['Methodes_formelles_lecture', 'Methodes_formelles_td'],
    'Mr. Sahli': ['Reseaux_td'],
    'Mme. Hamma': ['AI_tp'],
    'Dr. Djenadi': ['Distributed_architecture_lecture', 'Distributed_architecture_td'],
    'Dr. Lekehali': ['AI_lecture', 'AI_td'],
    'Dr. Alkama': ['Analyse_numerique_lecture', 'Analyse_numerique_td'],
    'Dr. Kaci': ['Entrepreneuriat_lecture'],
    'M. Abbas && Mme. Ladlani': ['AI_tp'],
    'Mme. Djenane': ['Securite_td'],
    'Dr. Zenadji': ['Reseaux_lecture', 'Reseaux_td'],
    'Mme. Khelouf': ['Securite_td'],
    'Mme. Kassa': ['Securite_td'],
    'Dr. Saba': ['Analyse_numerique_td'],
    'Dr. Djebari': ['Securite_lecture'],
    'M. Bechar': ['AI_tp']
}

GROUPS = [f'Group{num}' for num in range(1, 7)]
TD_ROOMS = [f"TD{room}" for room in range(1, 26)]
TP_ROOMS = [f"TP{room}" for room in range(1, 12)]
LECTURE_ROOMS = [f"Amphi{room}" for room in range(7, 8)]
CLASSROOMS = TD_ROOMS + TP_ROOMS + LECTURE_ROOMS
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

# Time slots for each day
TIME_SLOTS = [
    '08.30 to 10.00',
    '10.10 to 11.40',
    '11.50 to 13.20',
    '13.30 to 15.00',
    '15.10 to 16.40'
]

class Schedule:
    n_days = len(DAYS)
    n_lessons = len(TIME_SLOTS)
    total_lessons = n_days * n_lessons

    teachers = list(TEACHERS.keys())
    n_teachers = len(teachers)
    n_groups = len(GROUPS)
    n_rooms = len(CLASSROOMS)
    n_subjects = len(MODULES)

    def __init__(self):
        self.rooms = CLASSROOMS
        self.groups = GROUPS
        self.subjects = MODULES

        # room destinations (lectures, labs, etc.)
        self.rooms_dests = ["lec" if "Amphi" in room else "lab" if "TP" in room else "td" for room in self.rooms]

        # subjects teacher can teach
        self.teacher_specs = {teacher: set(subjects) for teacher, subjects in TEACHERS.items()}

        # subjects group is being taught (assuming each group has a subset of modules)
        self.learning_plan = [{module for module in MODULES if random.random() < 0.3} for _ in self.groups]

        # room per lesson per group
        self.rpl = [[None] * self.n_groups for _ in range(self.total_lessons)]

        # subject per lesson per group
        self.spl = [[None] * self.n_groups for _ in range(self.total_lessons)]

        # teacher per lesson per group
        self.tpl = [[None] * self.n_groups for _ in range(self.total_lessons)]

        self.cnt = 0

    def is_complete(self):
        return all([not any(lg is None for lg in l) for l in self.rpl])

    def check_constraints(self):
        self.cnt += 1

        if self.is_complete():
            for g in range(self.n_groups):
                class_types_per_subjects = {s: set() for s in self.learning_plan[g]}
                for l in range(self.total_lessons):
                    class_types_per_subjects[self.spl[l][g]].add(self.rooms_dests[self.rpl[l][g]])
                if any([len(s) != 2 for s in class_types_per_subjects.values()]):
                    return False

        for tpg in self.tpl:
            for i in range(self.n_groups - 1):
                if tpg[i] is not None and tpg[i] in tpg[i + 1:]:
                    return False

        for rpg in self.rpl:
            for i in range(self.n_groups - 1):
                if rpg[i] is not None and rpg[i] in rpg[i + 1:]:
                    return False

        return True

    def setter(self, l, g, t, r, s):
        self.tpl[l][g] = t
        self.rpl[l][g] = r
        self.spl[l][g] = s

    def select_unassigned_var(self):
        for l in range(self.total_lessons):
            for g in range(self.n_groups):
                if self.tpl[l][g] is None:
                    return l, g

    def degree_heuristic(self):
        none_list = []
        for l in range(self.total_lessons):
            none_list.append(sum([self.tpl[l][g] is None for g in range(self.n_groups)]))
        l = none_list.index(max(none_list))
        for g in range(self.n_groups):
            if self.tpl[l][g] is None:
                return l, g

    def mrv(self):
        for d in range(self.n_days):
            for l in range(self.n_lessons):
                l = d * self.n_lessons + l
                for g in range(self.n_groups):
                    if self.tpl[l][g] is None:
                        return l, g

    def order_domain_vals(self, g):
        for t in random.sample(self.teachers, self.n_teachers):
            available_subjects = list(self.learning_plan[g].intersection(self.teacher_specs[t]))
            for r in random.sample(range(self.n_rooms), self.n_rooms):
                for s in random.sample(available_subjects, len(available_subjects)):
                    yield t, r, s

    def lcv(self, g):
        teacher_scores = []
        for t in self.teachers:
            teacher_scores.append([0, t])
            for gi in range(self.n_groups):
                if gi != g:
                    teacher_scores[-1][0] += len(self.teacher_specs[t].intersection(self.learning_plan[gi]))
        for _, t in sorted(teacher_scores, key=lambda sc: sc[0]):
            available_subjects = list(self.learning_plan[g].intersection(self.teacher_specs[t]))
            for r in random.sample(range(self.n_rooms), self.n_rooms):
                for s in random.sample(available_subjects, len(available_subjects)):
                    yield t, r, s

    def forward_check(self, l, g):
        for t in random.sample(self.teachers, self.n_teachers):
            if t not in self.tpl[l]:
                available_subjects = list(self.learning_plan[g].intersection(self.teacher_specs[t]))
                for r in random.sample(range(self.n_rooms), self.n_rooms):
                    if r not in self.rpl[l]:
                        for s in random.sample(available_subjects, len(available_subjects)):
                            yield t, r, s

    def ac3(self):
        queue = []
        for l in range(self.total_lessons):
            for g1 in range(self.n_groups):
                for g2 in range(g1 + 1, self.n_groups):
                    queue.append((l, g1, g2))

        while queue:
            l, g1, g2 = queue.pop(0)
            if self.remove_inconsistent_val(l, g1, g2):
                for g in range(self.n_groups):
                    if g != g1:
                        queue.append((l, g1, g))

    def remove_inconsistent_val(self, l, g1, g2):
        good_subjects = set()
        bad_subjects = set()
        for t, r, s in self.order_domain_vals(g1):
            self.setter(l, g1, t, r, s)
            if self.check_constraints():
                constraints_checker = []

                for t, r, s in self.order_domain_vals(g2):
                    self.setter(l, g2, t, r, s)
                    constraints_checker.append(self.check_constraints())
                    self.setter(l, g2, None, None, None)

                if not any(constraints_checker):
                    bad_subjects.add(s)
                else:
                    good_subjects.add(s)
            self.setter(l, g1, None, None, None)
        subjects_to_remove = bad_subjects.difference(good_subjects)
        for s in subjects_to_remove:
            self.learning_plan[g1].remove(s)
        return len(subjects_to_remove) > 0

    def backtracking(self):
        var = self.select_unassigned_var()  # self.mrv()  # self.degree_heuristic()

        if var is None:
            return True

        l, g = var

        for t, r, s in self.order_domain_vals(g):  # self.forward_check(l, g): # self.lcv(g): #self.forward_check(l, g):
            self.setter(l, g, t, r, s)

            if self.check_constraints():
                res = self.backtracking()
                if res:
                    return True
            self.setter(l, g, None, None, None)
        return False

    def print(self):
        table = dict(indices=["Day", "Group"] + [slot for slot in TIME_SLOTS])
        for d in range(self.n_days):
            table[(d, 0)] = [DAYS[d]]
            for g in range(1, self.n_groups):
                table[(d, g)] = [""]
            for g in range(self.n_groups):
                table[(d, g)].append(GROUPS[g])
                for l in range(self.n_lessons):
                    l = d * self.n_lessons + l
                    lesson = (f"{self.subjects[self.spl[l][g]]}\n"
                              f"({self.rooms_dests[self.rpl[l][g]]})\n"
                              f"Room: {self.rooms[self.rpl[l][g]]}\n"
                              f"Prof.: {self.tpl[l][g]}")
                    table[(d, g)].append(lesson)
            table[(d, -1)] = [""] * (2 + self.n_lessons)
        print(tabulate(table, tablefmt="fancy_grid"))

# Run the schedule generation
csp = Schedule()
print("Start!")
start = time.time()
csp.backtracking()
print(f"Success! Time spent: {time.time() - start} s.")
print(f"Constraints checked {csp.cnt} times!")
csp.print()

import logging


class Student(object):
    def __init__(self):
        self.ID = 0
        self.Start_time = ''
        self.Completion_time = ''
        self.Email = ''
        self.Name = ''
        self.Student_ID = ''
        self.Workshop = ''
        self.Preferred_teammates = ''
        self.Preferred_project_option = ''
        self.Preferred_tech = ''
        self.Timezone = ''
        self.Preferred_week_days = ''
        self.Preferred_day_night_times = ''


def group_students(students):
    workshops = dict()
    for student in students:
        if student.Workshop in workshops:
            workshops[student.Workshop] += 1
        else:
            workshops[student.Workshop] = 1

    workshop_team_sizes = {}
    for wk, cnt in workshops.items():
        logging.warning(f'{wk}: {cnt}')
        if cnt > 35:
            raise Exception('Max students in a workshop exceed 35!')

        for team_size in [5, 6, 7]:
            team_cnt = float(cnt) / team_size
            # Max 5 teams in a workshop
            if team_cnt > 5:
                continue
            else:
                workshop_team_sizes[wk] = team_size
                break

    workshop_groups = {}
    for wk, team_size in workshop_team_sizes.items():
        groups = []
        group = []
        for student in students:
            if student.Workshop != wk:
                continue
            if len(group) < team_size:
                group.append(student)
            else:
                groups.append(group.copy())
                group.clear()

        workshop_groups[wk] = groups

    # print
    for wk, groups in workshop_groups.items():

        i = 1
        for group in groups:
            logging.warning(f'Workshop: [{wk}] Group[{i}]')
            i = i + 1
            for student in group:
                logging.warning(f'\t\t student: [{student.Student_ID}] {student.Name}')

    return workshop_groups

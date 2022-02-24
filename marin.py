from read import read_file

tab_file_to_read = ["input/a_an_example.in.txt",
                "input/b_better_start_small.in.txt",
                "input/c_collaboration.in.txt",
                "input/d_dense_schedule.in.txt",
                "input/e_exceptional_skills.in.txt",
                "input/f_find_great_mentors.in.txt" ]

indice_file = 0

file_input = tab_file_to_read[indice_file]
readed_file = read_file(file_input)

nb_contributors = readed_file.c
print("nb_contributors = ", nb_contributors)
dict_contributors = readed_file.contributors
print("dict_contributors = ", dict_contributors)
nb_projects = readed_file.p
print("nb_projects = ", nb_projects)
projects = readed_file.projects
print("projects = ", projects)

list_projects = projects.items()
print("list_projects = ", list_projects)

time_start = 0
nb_contributors_available = nb_contributors
def score_project(project, time_start, nb_contributors_available):
    #print("project in score_project = ", project)
    #print("skill_required = ", project.skill_required)
    days = project.d
    score = project.s
    best_before = project.b
    nb_roles = project.r

    if nb_roles > nb_contributors_available:
        return 0
    if (time_start + days) <= best_before:
        return score/(nb_roles*days)
    else:
        return (score - (best_before - time_start - days))/(nb_roles*days)

def naive_assign_contrib_to_project(project, map_map_skill):
    list_skill_needed = project[1].skill_required
    print("project = ", project)
    print("list_skill_needed = ", list_skill_needed)

    result_list = []

    for skill in list_skill_needed:
        print("skill = ", skill)
        current_name_skill = list(skill.keys())[0]
        current_level_skill = list(skill.values())[0]
        sub_map_current_skill = map_map_skill[current_name_skill]
        found_contrib_for_skill = False
        for skill_level in range(current_level_skill, 11): # We check from current level to 10...
            set_list_contrib = sub_map_current_skill[skill_level]
            if len(set_list_contrib) > 0:
                result_list.append((next(iter(set_list_contrib)), current_name_skill))
                found_contrib_for_skill = True

        if not found_contrib_for_skill:
            print("Pas possible!!!")
            return False, result_list

    print("Normalement on est bon")
    return True, result_list

sorted_project = sorted(list_projects, key=lambda x: score_project(x[1], time_start, nb_contributors_available), reverse=True)
print("sorted_project = ", sorted_project)

naive_assign_contrib_to_project(sorted_project[0], None, None)


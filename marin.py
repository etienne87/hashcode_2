from read import read_file
from etienne import make_map_of_skills, remove_contrib_from_skill_map, update_contributors

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
    #print("project = ", project)
    #print("list_skill_needed = ", list_skill_needed)

    result_list = []

    for skill in list_skill_needed:
        #print("skill = ", skill)
        current_name_skill = list(skill.keys())[0]
        current_level_skill = list(skill.values())[0]
        sub_map_current_skill = map_map_skill[current_name_skill]
        #print("sub_map_current_skill = ", sub_map_current_skill)
        found_contrib_for_skill = False
        for skill_level in range(current_level_skill, 11): # We check from current level to 10...
            set_list_contrib = sub_map_current_skill[skill_level]
            if len(set_list_contrib) > 0:
                result_list.append((next(iter(set_list_contrib))))#, current_name_skill))
                found_contrib_for_skill = True
                break

        if not found_contrib_for_skill:
            #print("Pas possible!!!")
            return False, result_list

    #print("Normalement on est bon")
    return True, result_list


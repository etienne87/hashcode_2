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
        return score/(nb_roles*days + best_before-time_start-days)
    else:
        return (score - (best_before - time_start - days))/(nb_roles*days)

def naive_assign_contrib_to_project(project, map_map_skill, contributors):
    list_skill_needed = project[1].skill_required
    #print("project = ", project)
    #print("list_skill_needed = ", list_skill_needed)

    result_list = []

    chosen_set = set()
    for skill in list_skill_needed:
        #print("skill = ", skill)
        current_name_skill = list(skill.keys())[0]
        current_level_skill = list(skill.values())[0]
        sub_map_current_skill = map_map_skill[current_name_skill]
        #print("sub_map_current_skill = ", sub_map_current_skill)
        found_contrib_for_skill = False

        minimal_skil_level = current_level_skill
        for contrib_already_chosen in chosen_set:
            if current_name_skill in contributors[contrib_already_chosen] and contributors[contrib_already_chosen][current_name_skill] >= current_level_skill:
                minimal_skil_level = current_level_skill - 1
                #print("We can mentor")
                break

        for skill_level in range(minimal_skil_level, 11): # We check from current level to 10...
            set_list_contrib = sub_map_current_skill[skill_level]
            for contrib_name in set_list_contrib:
                if contrib_name not in chosen_set:
                    result_list.append(contrib_name)#, current_name_skill))
                    chosen_set.add(contrib_name)
                    found_contrib_for_skill = True
                    break
            if found_contrib_for_skill:
                break

        if not found_contrib_for_skill:
            #print("Pas possible!!!")
            return False, result_list

    #print("Normalement on est bon")
    return True, result_list


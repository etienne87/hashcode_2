from read import read_file
from etienne import make_map_of_skills, remove_contrib_from_skill_map, update_contributors
import argparse
from pathlib import Path

def score_project(project, time_start, nb_contributors_available):
    #print("project in score_project = ", project)
    #print("skill_required = ", project.skill_required)
    days = project.d
    score = project.s
    best_before = project.b
    nb_roles = project.r

    # return -days + score/100

    if nb_contributors_available < nb_roles:
        return -100000

    if (time_start + days) <= best_before:
        return score/(nb_roles*days)
    else:
        return (score - (time_start + days - best_before))/(nb_roles*days)

def score_project_compute_score(project, time_start, nb_contributors_available):
    #print("project in score_project = ", project)
    #print("skill_required = ", project.skill_required)
    days = project.d
    score = project.s
    best_before = project.b
    nb_roles = project.r

    #if nb_roles > nb_contributors_available:
    #    return 0
    if (time_start + days) <= best_before:
        return score
    else:
        return max(0,(score - (time_start + days - best_before)))

def naive_assign_contrib_to_project(project, map_map_skill, contributors, available_contributors):
    list_skill_needed = project[1].skill_required
    #print("project = ", project)
    #print("list_skill_needed = ", list_skill_needed)

    result_list = []

    chosen_set = set()
    list_name_skill_needed = [list(dict_skill_needed.keys())[0] for dict_skill_needed in list_skill_needed]
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
            if skill_level == 0:
                set_list_contrib = set()
                # print("On veut former un mec la!")
                for available_contributor in available_contributors:
                    if available_contributor not in chosen_set:
                        if current_name_skill not in contributors[available_contributor]:
                            set_list_contrib.add(available_contributor)
                            break

            else:
                set_list_contrib = sub_map_current_skill[skill_level]
            current_contrib = None
            max_skill_usefull = -10
            for contrib_name in set_list_contrib:

                if contrib_name not in chosen_set:
                    nb_skill_contrib = 0
                    for skill_contrib in contributors[contrib_name]:
                        if skill_contrib in list_name_skill_needed:
                            nb_skill_contrib += 1

                    if nb_skill_contrib > max_skill_usefull:
                        found_contrib_for_skill = True
                        current_contrib = contrib_name
                        max_skill_usefull = nb_skill_contrib

            if found_contrib_for_skill:
                result_list.append(current_contrib)  # , current_name_skill))
                chosen_set.add(current_contrib)
                break

        if not found_contrib_for_skill:
            #print("Pas possible!!!")
            return False, result_list

    #print("Normalement on est bon")
    return True, result_list

def main():
    parser = argparse.ArgumentParser(description='input')

    # parser.add_argument('--input_fname', default="input/a_an_example.in.txt")
    parser.add_argument('--input_fname', default="input/b_better_start_small.in.txt")
    # parser.add_argument('--input_fname', default="input/c_collaboration.in.txt")
    # parser.add_argument('--input_fname', default="input/d_dense_schedule.in.txt")
    # parser.add_argument('--input_fname', default="input/e_exceptional_skills.in.txt")
    # parser.add_argument('--input_fname', default="input/f_find_great_mentors.in.txt")
    parser.add_argument('--output-fname')

    args = parser.parse_args()

    input_fname = args.input_fname
    if args.output_fname is None:
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True, parents=True)
        output_fname = str(output_dir / Path(input_fname).name.replace('in', 'out'))
    else:
        output_fname = args.output_fname

    print(f"input fname: {input_fname}")
    print(f"output_fname: {output_fname}")


    data = read_file(input_fname)
    current_time = 0
    projects = data.projects
    skill_map = make_map_of_skills(data)
    contributors = data.contributors
    list_projects = projects.items()

    nb_contributors_available= 10**5

    project_end_dates = []

    projects_done = set()

    output_projects = []

    total_score = 0

    search_project = True

    print("skill_map = ", skill_map)


if __name__ == "__main__":
    main()

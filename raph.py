import argparse
from etienne import update_contributors
import read
from pathlib import Path
from collections import defaultdict
import write
from marin import naive_assign_contrib_to_project, score_project
import heapq

def make_map_of_skills(data):
    skill_map = defaultdict(dict)
    for contrib_name,skill_set in data.contributors.items():
        for skill_name, value in skill_set.items():
            if value not in skill_map[skill_name]:
                skill_map[skill_name][value] = set()
            skill_map[skill_name][value].add(contrib_name)
    return skill_map


def remove_contrib_from_skill_map(skill_map, contrib, skillset):
    for skill_name, skill_value in skillset.items():
        skill_map[skill_name][skill_value].remove(contrib)




def main():
    parser = argparse.ArgumentParser(description='input')

    parser.add_argument('input_fname')
    parser.add_argument('--output-fname', default=None)

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


    data = read.read_file(input_fname)
    current_time = 0
    projects = data.projects
    skill_map = make_map_of_skills(data)
    contributors = data.contributors
    list_projects = projects.items()

    nb_contributors_available= 10**5

    project_end_dates = []

    projects_done = set()

    output_projects = []

    sorted_projects = sorted(list_projects, key=lambda x: score_project(x[1], current_time, nb_contributors_available), reverse=True)

    search_project = True

    while current_time < 10**6:
        if len(project_end_dates)>0:
            (first_end_date, tuple_project, project_contribs) = project_end_dates[0]
            while current_time >= first_end_date:
                search_project = True
                (first_end_date, tuple_project, project_contribs) = heapq.heappop(project_end_dates)
                update_contributors(tuple_project[1].skill_required, project_contribs, contributors, skill_map)
                if len(project_end_dates)>0:
                    (first_end_date, tuple_project, project_contribs) = project_end_dates[0]
                else:
                    break

        if search_project:
            search_project = False
            for project in sorted_projects:
                project_name = project[0]
                if project_name in projects_done:
                    continue
                valid, project_contribs = naive_assign_contrib_to_project(project, map_map_skill=skill_map)
                if not valid:
                    continue
                output_projects.append((project_name, project_contribs))
                projects_done.add(project_name)
                for contrib in project_contribs:
                    remove_contrib_from_skill_map(skill_map, contrib, contributors[contrib])
                project_end_date = current_time + project[1].d
                heapq.heappush(project_end_dates, (project_end_date,project, project_contribs))

        current_time += 1





#    result = compute_result(data)
#
    # result = [{'WebServer': ['Bob', 'Anna']}, {'Logging': ['Anna']}, {'WebChat': ['Maria', 'Bob']}]

    write.write_result(output_projects, output_fname)

#    expected_score = scoring.compute_score(data, result)
#    print(f"Expected score is {expected_score}")





if __name__ == "__main__":
    main()
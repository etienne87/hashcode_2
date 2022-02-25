import argparse

from etienne import update_contributors, make_map_of_skills, remove_contrib_from_skill_map
import read
from pathlib import Path
from collections import defaultdict
import write
from marin import naive_assign_contrib_to_project, score_project, score_project_compute_score
import heapq





def main():
    parser = argparse.ArgumentParser(description='input')

    # parser.add_argument('--input_fname', default="input/a_an_example.in.txt")
    # parser.add_argument('--input_fname', default="input/b_better_start_small.in.txt")
    parser.add_argument('--input_fname', default="input/c_collaboration.in.txt")
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

    total_score = 0

    search_project = True

    while current_time < 10**15:
        print(len(project_end_dates))
        if len(project_end_dates) == 0 and search_project==False:
            break
        if len(project_end_dates)>0:
            (first_end_date, tuple_project, project_contribs) = heapq.heappop(project_end_dates)
            current_time = first_end_date
            search_project = True
            update_contributors(tuple_project[1].skill_required, project_contribs, contributors, skill_map)
            while len(project_end_dates)>0 and (project_end_dates[0][0] <= current_time):
                print("C est mieux de faire ca!!")
                (first_end_date, tuple_project, project_contribs) = heapq.heappop(project_end_dates)
                current_time = first_end_date
                search_project = True
                update_contributors(tuple_project[1].skill_required, project_contribs, contributors, skill_map)
            # if len(project_end_dates)>0 and project_end_dates[0][0] <= current_time:
            #     print("Y a un probleme, project_end_dates[0][0] = ", project_end_dates[0][0], " et current_time = ", current_time)

        if search_project:
            sorted_projects = sorted(list_projects, key=lambda x: score_project(x[1], current_time, nb_contributors_available), reverse=True)
            search_project = False
            for project in sorted_projects:
                project_name = project[0]
                if project_name in projects_done:
                    continue
                valid, project_contribs = naive_assign_contrib_to_project(project, map_map_skill=skill_map,contributors=contributors)
                if not valid:
                    continue
                if current_time + project[1].d <= project[1].b:
                    total_score += project[1].s
                else:
                    total_score += max(0, project[1].s - ((current_time + project[1].d)- project[1].b ))
                #print(project)
                #print("TIME TIME", current_time)
                print("TOTAL SCORE", total_score)
                #print("project found")
                output_projects.append((project_name, project_contribs))
                projects_done.add(project_name)
                for contrib in project_contribs:
                    remove_contrib_from_skill_map(skill_map, contrib, contributors[contrib])
                project_end_date = current_time + project[1].d
                heapq.heappush(project_end_dates, (project_end_date,project, project_contribs))

        current_time += 1

    print(total_score)



#    result = compute_result(data)
#
    # result = [{'WebServer': ['Bob', 'Anna']}, {'Logging': ['Anna']}, {'WebChat': ['Maria', 'Bob']}]

    write.write_result(output_projects, output_fname)

#    expected_score = scoring.compute_score(data, result)
#    print(f"Expected score is {expected_score}")





if __name__ == "__main__":
    main()

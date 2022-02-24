import argparse
import read
from pathlib import Path
from collections import defaultdict
#import write
#import scoring
#from laurent import compute_result
from etienne import *






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

    skill_map = make_map_of_skills(data)
    print('num skills: ', len(skill_map.keys()))

    selected = list(data.contributors.keys())[:3]

    for project_name, project_data in data.projects.items():
        update_contributors(project_data.skill_required, selected, data.contributors, skill_map) 

    # verify remove_contrib_from_skill_map
    # for contrib_name, skill_set in data.contributors.items():
    #     remove_contrib_from_skill_map(skill_map, contrib_name, skill_set)
    # print(skill_map)
    

#    result = compute_result(data)
#
#    write.write_result(result, output_fname)

#    expected_score = scoring.compute_score(data, result)
#    print(f"Expected score is {expected_score}")





if __name__ == "__main__":
    main()

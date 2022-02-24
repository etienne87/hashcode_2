import argparse
import read
from pathlib import Path
from collections import defaultdict
#import write
import write
#import scoring

#from laurent import compute_result

def make_map_of_skills(data):
    skill_map = defaultdict(dict)
    for contrib_name,skill_set in data.contributors.items(): 
        for skill_name, value in skill_set.items():
            if value not in skill_map[skill_name]:
                skill_map[skill_name][value] = set()
            skill_map[skill_name][value].add(contrib_name)
    return skill_map



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
    print(skill_map)
#    result = compute_result(data)
#
    result = [{'WebServer': ['Bob', 'Anna']}, {'Logging': ['Anna']}, {'WebChat': ['Maria', 'Bob']}]

    write.write_result(result, output_fname)

#    expected_score = scoring.compute_score(data, result)
#    print(f"Expected score is {expected_score}")





if __name__ == "__main__":
    main()

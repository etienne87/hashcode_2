import argparse
import read
from pathlib import Path
#import write
#import scoring

#from laurent import compute_result



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
#    result = compute_result(data)
#
#    write.write_result(result, output_fname)

#    expected_score = scoring.compute_score(data, result)
#    print(f"Expected score is {expected_score}")





if __name__ == "__main__":
    main()

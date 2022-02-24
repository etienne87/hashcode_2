from typing import List, Dict

def write_result(projects: List[Dict], output_fname: str):
    """
    Dump results intop a file

    Example:
    projects  : 
[('WebServer', ['Bob', 'Anna']), ('Logging', ['Anna']), ('WebChat', ['Maria', 'Bob'])]

    would output:

    3
    WebServer
    Bob Anna
    Logging
    Anna
    WebChat
    Maria Bob
    """
    nb_completed_projects = len(projects)

    with open(output_fname, 'w') as f:
        f.write(str(nb_completed_projects))
        f.write('\n')
        for p_name, contributors in projects:
            f.write(p_name)
            f.write('\n')
            f.write(' '.join(contributors))
            f.write('\n')





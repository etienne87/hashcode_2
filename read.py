from types import SimpleNamespace

def read_file(filename):
    r = SimpleNamespace()
    with open(filename, 'r') as f:
        r.c, r.p = [int(x) for x in f.readline().strip().split()]
        contributors = []
        for contrib_lines in range(r.c):
            name, nb_skills = f.readline().strip().split()
            nb_skills = int(nb_skills)
            skills = {}
            for _ in range(nb_skills):
                skill_name, skill_level = f.readline().strip().split()
                skill_level = int(skill_level)
                skills[skill_name] = skill_level
            contributors.append({name: skills})
        projects = []
        for p_num in range(r.p):
            line = f.readline().strip().split()
            p_name = line[0]
            numbers = [int(x) for x in line[1:]]

            project = SimpleNamespace()
            project.d, project.s, project.b, project.r = numbers

            skills_required = []
            for _ in range(project.r):
                skill_required, skill_level_required = f.readline().strip().split()
                skill_level_required = int(skill_level_required)
                skills_required.append({skill_required: skill_level_required})

            project.skill_required = skill_required
            projects.append(project)




        r.contributors = contributors
        r.projects = projects



        #r.L = []
        #r.D = []
        #for client_num in range(r.C):
        #    r.L.append(list(set([str(x) for x in f.readline().strip().split(' ')[1:]])))
        #    r.D.append(list(set([str(x) for x in f.readline().strip().split(' ')[1:]])))

        #r.L_ingredients = set.union(*[set(x) for x in r.L])
        #r.D_ingredients = set.union(*[set(x) for x in r.D])
        #r.ingredients = r.L_ingredients.union(r.D_ingredients)

    print(r)
    return r


if __name__ == '__main__':
    r = read_file('input/a_an_example.in.txt')
    print(r)

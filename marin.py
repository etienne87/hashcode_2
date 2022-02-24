from read import read_file

tab_file_to_read = ["input/a_an_example.in.txt",
                "input/b_better_start_small.in.txt",
"input/c_collaboration.in.txt",
"input/d_dense_schedule.in.txt",
"input/e_exceptional_skills.in.txt",
"input/f_find_great_mentors.in.txt" ]

indice_file = 0

file_input = tab_file_to_read[indice_file]
readed_file = read_file(file_input)

nb_contributors = readed_file.c
print("nb_contributors = ", nb_contributors)
dict_contributors = readed_file.contributors
print("dict_contributors = ", dict_contributors)
nb_projects = readed_file.p
print("nb_projects = ", nb_projects)
projects = readed_file.projects
print("projects = ", projects)

def score_project(project, time_start):
    days = project.d
    score = project.s
    best_before = project.b
    nb_roles = project.r

    if time_start + days <
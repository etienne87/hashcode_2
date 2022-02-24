from collections import defaultdict

def make_map_of_skills(data):
    skill_map = defaultdict(lambda:defaultdict(set))
    for contrib_name,skill_set in data.contributors.items():
        for skill_name, value in skill_set.items():
            skill_map[skill_name][value].add(contrib_name)
    return skill_map


def remove_contrib_from_skill_map(skill_map, contrib, skillset):
    for skill_name, skill_value in skillset.items():
        skill_map[skill_name][skill_value].remove(contrib)


def update_contributors(skills_required, selected, contributors, skill_map):
    for contrib_name, skill in zip(selected, skills_required):
        skill_name, skill_value = list(skill.items())[0]
        if skill_name not in contributors[contrib_name]:
            contributors[contrib_name][skill_name] = 1
        elif contributors[contrib_name][skill_name] <= skill_value:
            if skill_value < 10:
                contributors[contrib_name][skill_name] += 1

    for contrib_name in selected:
        for skill in contributors[contrib_name]:
            value = contributors[contrib_name][skill]
            skill_map[skill][value].add(contrib_name)

def update_contributors2(skills_required, selected, contributors, skill_map):
    for contrib_name in selected:
        for skill in skills_required:
            skill_name, skill_value = list(skill.items())[0]
            if skill_name not in contributors[contrib_name]:
                contributors[contrib_name][skill_name] = 1
            elif contributors[contrib_name][skill_name] <= skill_value:
                contributors[contrib_name][skill_name] += 1


        for skill in contributors[contrib_name]:
            value = contributors[contrib_name][skill]
            skill_map[skill][value].add(contrib_name)

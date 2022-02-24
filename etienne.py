from collections import defaultdict

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


def update_contributors(skills_required, selected, contributors, skill_map):
    for contrib_name in selected:
        for skill_name in skills_required.keys():
            old_value = contributors[contrib_name][skill_name]
            skill_map[skill_name][old_value].remove(contrib_name)
            skill_map[skill_name][old_value+1].add(contrib_name)
            contributors[contrib_name][skill_name] += 1

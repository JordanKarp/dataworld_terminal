from classes.person import Person


# local_cond = lambda p: p.home and p.home.state == company.hq.state
# regional_cond = lambda p: p.home and p.home.zipcode[0] == company.hq.zipcode[0]
# gender_cond = lambda p, gender: p.gender == gender


def is_gender(gender, person_id, pop_dict):
    return pop_dict[person_id].gender == gender


def get_gendered_pop(gender, population: list[Person]):
    return [p for p in population if p.gender == gender]


def get_regional_pop(zips, population: list[Person]):
    return [p for p in population if p.home and p.home.zipcode[0] in zips]


def get_state_pop(states, population: list[Person]):
    return [p for p in population if p.home and p.home.state in states]


def get_pop_with_siblings(population: list[Person]):
    return [p for p in population if p.siblings]


def get_pop_with_parents(population: list[Person]):
    return [p for p in population if p.parent_a and p.parent_b]

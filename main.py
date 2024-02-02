from generators.personGenerator import PersonGenerator

# seed = "ABC123"
seed = None

pg = PersonGenerator(seed)

new_person = pg.new()
print(new_person)

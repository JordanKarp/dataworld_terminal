from generators.populationGenerator import PopulationGenerator

# seed = "ABC123"
seed = None

pg = PopulationGenerator(seed)

pg.create()
# pg.print_pop()
pg.csv_pop()

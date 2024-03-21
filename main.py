from generators.dataSourceGenerator import DataSourceGenerator
from generators.companiesGenerator import CompaniesGenerator
from generators.populationGenerator import PopulationGenerator

INIT_POP = 500
INIT_GEN = 3
INIT_COMP = 200


def main(seed=None):
    pg = PopulationGenerator(seed)
    pop = pg.create(INIT_POP, INIT_GEN)

    cg = CompaniesGenerator()
    cg.create(INIT_COMP)
    cg.load_population(pop)
    cg.add_employees()
    cg.add_clients()
    comps = cg.return_companies()

    dsg = DataSourceGenerator(pop, comps, seed)

    dsg.populate_sources()
    dsg.export()


if __name__ == "__main__":
    seed = "ABC123"
    # seed = None
    main(seed)

from generators.dataSourceGenerator import DataSourceGenerator
from generators.companiesGenerator import CompaniesGenerator
from generators.populationGenerator import PopulationGenerator


def main(seed=None):
    pg = PopulationGenerator(seed)
    pop = pg.create(3)

    cg = CompaniesGenerator()
    cg.create()
    cg.load_population(pop)
    cg.add_employees()
    cg.add_clients()
    comps = cg.return_companies()

    dsg = DataSourceGenerator(pop, comps, seed)

    cg.comanies_to_csv()
    pg.population_to_csv()
    dsg.generate_data_source_lists(output="CSV")


if __name__ == "__main__":
    seed = "ABC123"
    # seed = None
    main(seed)

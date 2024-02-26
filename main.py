from generators.companyGenerator import CompanyGenerator
from generators.dataSourceGenerator import DataSourceGenerator
from generators.companiesGenerator import CompaniesGenerator
from generators.populationGenerator import PopulationGenerator


def main(seed=None):
    pg = PopulationGenerator(seed)
    pop = pg.create()

    cg = CompaniesGenerator()
    cg.create()
    cg.load_population(pop)
    comps = cg.add_employees()

    # dsg = DataSourceGenerator(seed)
    # dsg.add_population(pop)
    # dsg.add_companies(comps)

    cg.csv_eco()
    pg.csv_pop()
    # dsg.csv_all_data_sources()


if __name__ == "__main__":
    seed = "ABC123"
    # seed = None
    main(seed)

from generators.companyGenerator import CompanyGenerator
from generators.dataSourceGenerator import DataSourceGenerator
from generators.economyGenerator import CompaniesGenerator
from generators.populationGenerator import PopulationGenerator


def main(seed=None):
    pg = PopulationGenerator(seed)
    pop = pg.create()
    # pg.print_pop()

    # cg = CompanyGenerator()
    # print(cg.new())

    eg = CompaniesGenerator()
    eg.create()
    eg.add_employees(pop)
    # eg.print_eco()
    eg.csv_eco()

    pg.csv_pop()

    # dsg = DataSourceGenerator(seed)
    # dsg.add_population(pop)
    # dsg.print_all_data_sources()
    # dsg.csv_all_data_sources()


if __name__ == "__main__":
    seed = "ABC123"
    # seed = None
    main(seed)

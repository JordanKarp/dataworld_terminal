from generators.populationGenerator import PopulationGenerator

# from generators.companyGenerator import CompanyGenerator
from generators.dataSourceGenerator import DataSourceGenerator


def main(seed=None):
    pg = PopulationGenerator(seed)
    pop = pg.create()
    # pg.print_pop()
    pg.csv_pop()

    # cg = CompanyGenerator()
    # print(cg.new_company())

    dsg = DataSourceGenerator(seed)
    dsg.add_population(pop)

    # dsg.print_all_data_sources()
    dsg.csv_all_data_sources()


if __name__ == "__main__":
    seed = "ABC123"
    main(seed)

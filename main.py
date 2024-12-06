from generators.dataSourceGenerator import DataSourceGenerator
from generators.webpageGenerator import WebpageGenerator
from generators.companiesGenerator import CompaniesGenerator
from generators.locationGenerator import LocationGenerator
from generators.populationGenerator import PopulationGenerator
from generators.missionGenerator import MissionGenerator
from generators.transactionGenerator import TransactionsGenerator
from generators.mapGenerator import MapGenerator

INIT_POP = 10
INIT_GEN = 3
INIT_COMP = 1
INIT_MISSIONS = 10
INIT_TRANSACTION_YEARS = 1

# TOWN_FILE = "baxter_center.json"
# TOWN_FILE = "bridgewater_city.json"
TOWN_FILE = "test.json"


def main(seed=None):

    lg = LocationGenerator(seed)
    locations, roads, dimensions = lg.generate_locations_from_town(TOWN_FILE)
    # for loc in locations:
    #     print(loc)
    pg = PopulationGenerator(seed, locations)
    population = pg.create(INIT_POP, INIT_GEN)

    map_gen = MapGenerator(seed)
    custom_maps = map_gen.create(locations, roads, dimensions)
    print(custom_maps)
    # cg = CompaniesGenerator(seed, locations)
    # cg.create(INIT_COMP)
    # cg.load_population(population)
    # cg.add_employees()
    # cg.add_favorite_companies()
    # companies = cg.return_companies()

    # tg = TransactionsGenerator(population, companies, seed)
    # tg.generate(INIT_TRANSACTION_YEARS)

    # mGen = MissionGenerator(population, companies, seed)
    # missions = mGen.generate_missions(INIT_MISSIONS)

    # dsg = DataSourceGenerator(population, companies, locations, None, seed)
    # dsg.populate_sources()
    # dsg.export()
    # dsg.print_table()

    # webgen = WebpageGenerator(population, companies, missions, seed)
    # webgen.gen_all()
    # webgen.export_websites()


if __name__ == "__main__":
    seed = "ABC123"
    # seed = None
    main(seed)

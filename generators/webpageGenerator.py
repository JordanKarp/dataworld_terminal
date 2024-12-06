from faker import Faker
from itertools import groupby
import json
from pathlib import Path

from classes.website import Website
from utilities.objects_to_table import objects_to_table

DATA_SOURCE_RESULTS_PATH = Path("results")


class WebpageGenerator:
    def __init__(self, pop, comp, missions, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.webpages = []
        self.pop = pop
        self.comp = comp
        self.missions = missions

    def gen_all(self):
        self.gen_index()
        self.gen_mission_pages()
        self.gen_social_media_pages()
        self.gen_phonebook()
        self.gen_industry_directory()
        self.gen_company_homepages()
        # self.gen_motor_vehicles_department()
        return self.webpages

    def gen_single_page(self, slug, url, title, searchable, page_type, html, data=None):
        page = Website(slug, url, title, searchable, page_type, html, data)
        self.webpages.append(page)

    def gen_index(self):
        index_html = (
            "<body>"
            "<font size='6'>Welcome to Dataworld!</font><br><br>"
            "Welcome to Dataworld, where debts become opportunities!<br><br>"
            "Helpful getting started links:<br>"
            " - <a href='dataworld~missions'>Available Missions</a><br>"
            " - <a href='social'>Social Connect</a>- A social media page for citizens<br>"
            " - <a href='phonebook'>PhoneBook</a> -  Name, Phone Number, and Address lookup tool<br>"
            " - <a href='companybook'>CompanyBook</a> -  PhoneBook for Companies<br>"
            " - <a href='mvd'>TODO Motor Vechicles Department</a> - Car registration records<br>"
            " - <a href='banks'>TODO Bank Records</a><br>"
            " - <a href='phone'>TODO Phone Records</a><br>"
            "<br>"
            "Best of luck to you and happy solving!<br>"
            "Dataworld"
            "</body>"
        )
        self.gen_single_page(
            slug="index",
            url="www.dataworld.com/",
            title="Dataworld Homepage",
            searchable=True,
            page_type="Webpage",
            html=index_html,
        )

    def gen_mission_pages(self):
        # Mission table page
        full = objects_to_table(self.missions)
        m_table = [[full[0][2], full[0][4], "Information"]]
        for row in full[1:]:
            m_table.append(
                [
                    row[2],
                    row[4],
                    f"<a href='dataworld~missions~{row[0]}'>More info</a>",
                ]
            )

            "<body><font color='#c4f3fc'><font size='6'><b>Mission One Info</b></font><br><br>Find Dog Owners!<br><br><p>The Psychology Lab is seeking dog owners to participate in a new research project. Please submit 5 different dog owners to be asked to participate.</p><br><br><a href='accept_mission~M1'>Accept Mission</a></font</body>"
            # Mission More info page
            self.gen_single_page(
                slug=f"dataworld~missions~{row[0]}",
                url=f"www.dataworld.com/missions/{row[0]}",
                title=f"{row[0]}: {row[2]}",
                searchable=False,
                page_type="Webpage",
                html=(
                    "<body>"
                    "<a href='dataworld~missions'><-Back To Mission</a><br><br>"
                    f"<b>Mission ID:</b> {row[0]}<br>"
                    f"<b>Mission Status:</b> {row[1].name}<br>"
                    "<br>"
                    f"<b>Title:</b> {row[2]}<br>"
                    f"<b>Reward:</b> {row[4]}<br>"
                    f"<b>Info:</b> {row[3]}<br>"
                    f'<b><a href="dataworld~missions~{row[0]}~accept">Accept Mission</a><b><br>'
                    "<br>"
                    "<br>"
                    "<br>"
                    "<br>"
                    "<br>"
                    f"Solution (TO BE REMOVED): {row[5]}"
                    "</body>"
                ),
            )
            # Mission Accept Page
            self.gen_single_page(
                slug=f"dataworld~missions~{row[0]}~accept",
                url=f"www.dataworld.com/missions/{row[0]}/accept",
                title=f"{row[0]}: {row[1]}",
                searchable=False,
                page_type="Accept",
                html="",
                data={
                    "id": row[0],
                    "status": row[1],
                    "title": row[2],
                    "text": row[3],
                    "reward": row[4],
                    "_solution": row[5],
                },
            )
        # Mission Table homepage
        self.gen_single_page(
            slug="dataworld~missions",
            url="www.dataworld.com/missions",
            title="Missions",
            searchable=False,
            page_type="Table",
            html=m_table,
        )

    def gen_company_homepages(self):
        for c in self.comp.values():
            # Homepage
            self.gen_single_page(
                slug=c.slug,
                url=f"www.{c.slug}.com/",
                title=c.name,
                searchable=True,
                page_type="Webpage",
                html=c.homepage_html,
            )
            # About Us
            self.gen_single_page(
                slug=f"{c.slug}~about",
                url=f"www.{c.slug}.com/about",
                title=f"{c.name}: About",
                searchable=False,
                page_type="Webpage",
                html=c.about_html,
            )
            # Contact Us
            self.gen_single_page(
                slug=f"{c.slug}~contact",
                url=f"www.{c.slug}.com/contact",
                title=f"{c.name}: Contact",
                searchable=False,
                page_type="Webpage",
                html=c.contact_html,
            )
            # CompanyBook Page
            company_book_html = (
                "<body>"
                f"<font size=6> {c.name} Company Information</font><br><br>"
                f"<b>Homepage:</b> <a href={c.slug}>www.{c.slug}.com</a><br>"
                f"<b>Industry:</b> {c.industry}<br>"
                f"<b>Founded:</b> {c.founded}<br>"
                f"<b>Number of Clients:</b> {c.num_clients}<br>"
                f"<b>Client Scope:</b> {c.client_scope}<br>"
                f"<b>Slogan:</b> {c.slogan}<br>"
                f"<b>Products:</b> {c.products}<br>"
                f"<b>Employees:</b> {c.num_employees_hired}<br>"
                f"<b>Hiring:</b> {c.room_to_hire}<br>"
                f"<b>Locations:</b><br>"
                f"{'<br>   '.join(l.location.address for l in c.locations)}<br>"
            )
            self.gen_single_page(
                slug=f"companybook~{c.slug}",
                url=f"www.companybook.com/{c.slug}",
                title=f"CompanyBook: {c.name}",
                searchable=True,
                page_type="Webpage",
                html=company_book_html,
            )

    def gen_social_media_pages(self):
        self.gen_single_page(
            slug="social",
            url="www.social-connect.com/",
            title="Social Connect: Search",
            searchable=True,
            page_type="Searchpage",
            html="Social Connect - Your place to connect! Search for a person here.",
        )

        pop = [p for p in self.pop.values() if p.social_connect]
        for p in pop:
            person_html = (
                "<body>"
                f"<font size='6'>Social Connect</font><br>"
                "<br>"
                f"<font size='5'><b><u>{p.name}</u></b></font><br>"
                f"<b>Full Name:</b> {p.full_name}<br>"
                f"<b>Age:</b> {p.age}<br>"
                f"<b>Gender:</b> {p.gender}<br>"
                f"<b>Height:</b> {p.format_height}<br>"
                f"<b>Weight:</b> {p.format_weight}<br>"
                f"<b>Hair Color:</b> {p.hair_color}<br>"
                f"<b>Eye Color:</b> {p.eye_color}<br>"
                f"<b>Sexual Orientation:</b> {p.sexual_orientation}<br>"
                f"<b>Blood Type:</b> {p.blood_type}<br>"
                "<br>"
                f"<b>Employer:</b> {p.employer}<br>"
                f"<b>Role:</b> {p.role}<br>"
                "<br>"
                f"<b>Traits:</b> {', '.join([p.positive_traits, p.neutral_traits, p.negative_traits])}<br>"
                f"<b>Family:</b>  {', '.join(f.name for f in p.list_of_family)} <br>"
                f"<b>Favorite Companies:</b>  {', '.join(self.comp[p.favorites[f][0]].name for f in p.favorites)} <br>"
                f"<b>Friends:</b>  {', '.join(f.name for f in p.friends)} <br>"
                "<br>"
                f"<b>Posts:</b><br><br>"
                f"{'<br>'.join([str(p) for p in p.social_connect.posts])}"
                "</body>"
            )

            self.gen_single_page(
                slug=f"social~{p.name_slug}",
                url=f"www.social-connect.com/{p.name_slug}",
                title=f"Social Connect: {p.name}",
                searchable=True,
                page_type="Webpage",
                html=person_html,
            )

    def gen_industry_directory(self):
        sorted_companies = sorted(self.comp.values(), key=lambda c: c["industry"])
        homepage_html = (
            "<body><font face='roboto'> <font size=6> Industries </font><br><br>"
        )
        for industry, industry_group in groupby(
            sorted_companies, key=lambda c: c["industry"]
        ):
            homepage_html += f"<a href='companybook~{industry}'>{industry}</u><br>"
            industry_html = f"<body><font size=5>Companies in {industry}</font><br><br>"
            for num, comp in enumerate(industry_group, 1):

                industry_html += f"  {num}. <a href={comp.slug}>{comp.name}</a><br>"
            self.gen_single_page(
                slug=f"companybook~{industry}",
                url=f"www.companybook.com/{industry}",
                title=f"Industry List: {industry}",
                searchable=True,
                page_type="Webpage",
                html=industry_html,
            )
        homepage_html += "</font><body>"

        self.gen_single_page(
            slug="companybook",
            url="www.companybook.com/",
            title="Company Book",
            searchable=True,
            page_type="Webpage",
            html=homepage_html,
        )

    def gen_phonebook(self):
        pop = sorted(
            self.pop.values(),
            key=lambda p: (p["last_name"], p["first_name"], p["middle_name"]),
        )
        html = "<body><font face='roboto'>"
        html += f"<b>{'Name'.ljust(17)} {'Phone Number'.center(15)}    {'Address'.center(25)}</b><br>"
        html += f"<b>{'____'.ljust(17)} {'____________'.center(15)}    {'_______'.center(25)}</b><br>"
        html += "".join(
            f"<b>{str(p.last_name_first_initial.ljust(17))}</b> {str(p.phone_number)}   {str(p.home.short_addr)}<br>"
            for p in pop
            if p.home and p.phone_number and p.is_alive
        )
        html += "</font></body>"
        self.gen_single_page(
            slug="phonebook",
            url="www.phonebook.com",
            title="PhoneBook",
            page_type="Webpage",
            html=html,
            searchable=True,
        )

    def gen_motor_vehicles_department(self):
        # car_pop = sorted(
        #     [p for p in self.pop.values() if p.vehicle],
        #     key=lambda p: (p["vehicle"]["vin"]),
        # )
        pop = {k: p for k, p in self.pop.items() if p.vehicle and p.is_alive}
        car_table = [
            [
                "License Plate #",
                "VIN",
                "Make",
                "Model",
                "Year",
                "Color",
                "Body Type",
                "Owner",
            ]
        ]

        for p in pop.values():
            car_row = [
                str(p.vehicle.license_plate_num),
                str(p.vehicle.vin),
                str(p.vehicle.make),
                str(p.vehicle.model),
                str(p.vehicle.year),
                str(p.vehicle.color),
                str(p.vehicle.body_type),
                str(p.name),
            ]
            car_table.append(car_row)
        # pre_table = objects_to_table(car_pop)

        # for row in pre_table:
        #     car_table.append([row[0], row[1], row[2]])

        # # html = f"<b>{'VIN'.center(17)} {'Make'.center(8)} {'Model'.center(8)} {'Year'.center(8)} {'Body Type'.center(8)} {'Color'.center(8)}</b><br>"
        # # html += "".join(
        # #     f"<b>{p.vehicle.vin.ljust(17)}</b> {p.vehicle.make.ljust(8)} {p.vehicle.model.ljust(8)} {str(p.vehicle.year).ljust(8)} {p.vehicle.body_type.ljust(8)} {p.vehicle.color.ljust(8)}<br>"
        # #     for p in car_pop
        # #     if p.home and p.is_alive
        # # )
        # table = [
        #     ["License Plate #", "VIN", "Make", "Model", "Year", "Color", "Body Type"]
        # ]
        # table.extend(
        #     [
        #         p.vehicle.license_plate_num,
        #         p.vehicle.vin,
        #         p.vehicle.make,
        #         p.vehicle.model,
        #         p.vehicle.year,
        #         p.vehicle.color,
        #         p.vehicle.body_type,
        #     ]
        #     for p in car_pop
        #     if p.is_alive
        # )
        self.gen_single_page(
            slug="mvd",
            url="www.mvd.com/",
            title="Motor Vehicles Department: Search",
            searchable=True,
            page_type="Table",
            html=car_table,
        )

        #   def gen_vehicle_registrations(self):
        # fields = [
        #     "full_name",
        #     "vehicle~make",
        #     "vehicle~model",
        #     "vehicle~year",
        #     "vehicle~color",
        #     "vehicle~body_type",
        #     "vehicle~license_plate_num",
        #     "vehicle~vin",
        # ]
        # self._generate_data_source(
        #     "VehicleRegistrations",
        #     ["vehicle"],
        #     fields,
        #     self.population,
        #     self._get_additional_attr,
        # )

    def export_websites(self):
        web_data = {"webdata": {}}
        for site in self.webpages:
            web_data["webdata"][site.slug] = {
                "id_slug": site.slug,
                "url": site.url,
                "title": site.title,
                "searchable": site.searchable,
                "page_type": site.page_type,
                "html": site.html,
                "data": site.data or None,
            }
        with open(
            DATA_SOURCE_RESULTS_PATH / "web_data.json", "w", encoding="utf-8"
        ) as f:
            json.dump(web_data, f, indent=4)

        mission_data = {
            mission_id: {
                "id": mission.id,
                "status": mission.status.name,
                "title": mission.title,
                "text": mission.text,
                "reward": mission.reward,
                "_solution": mission._solution,
            }
            for mission_id, mission in self.missions.items()
        }
        with open(
            DATA_SOURCE_RESULTS_PATH / "mission_data.json", "w", encoding="utf-8"
        ) as f:
            json.dump(mission_data, f, indent=4)

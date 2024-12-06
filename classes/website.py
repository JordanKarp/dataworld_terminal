from dataclasses import dataclass


@dataclass
class Website:
    def __init__(
        self,
        slug,
        url,
        title,
        searchable=True,
        page_type="Webpage",
        # restricted=False,
        html="",
        data={},
    ):
        self.slug: str = slug
        self.url: str = url
        self.title: str = title
        self.searchable: bool = searchable
        self.page_type: str = page_type
        self.html: str = html
        self.data: dict = data
        # TODO Needs to be implemented
        # self.restricted: bool = restricted

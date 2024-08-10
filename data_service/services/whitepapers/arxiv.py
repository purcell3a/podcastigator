import re
from typing import List

import re
from typing import List
import requests
from bs4 import BeautifulSoup
from requests import Response

from data_service.whitepapers.arxiv.arXiv_category import ArXivCategory
from data_service.whitepapers.arxiv.arXiv_metadata import ArXivMetadata
from data_service.whitepapers.arxiv.white_paper_service import WhitePaperService


class ArXivService(WhitePaperService):
    BASE_URL = "https://arxiv.org"
    PDF_PATH = "/pdf/"
    SEARCH_API_URL = "https://export.arxiv.org/api/query"
    CATEGORY_TAXONOMY_URL = f"{BASE_URL}/category_taxonomy"

    def __init__(self):
        super().__init__()

    def get_white_paper(self, paper_id: str) -> bytes:
        url = self._build_pdf_url(paper_id)
        return self._fetch_pdf(url)

    def get_metadata(self, paper_id: str) -> ArXivMetadata:
        metadata_res = self._query_arxiv(f"id_list={paper_id}")
        return self._parse_metadata_xml(metadata_res.text)[0]

    def get_categories(self) -> List[ArXivCategory]:
        html_content = self._fetch_html(self.CATEGORY_TAXONOMY_URL)
        return self._parse_categories_html(html_content)

    def search_papers(self, query: str) -> List[ArXivMetadata]:
        search_res = self._query_arxiv(query)
        return self._parse_metadata_xml(search_res.text)

    def _build_pdf_url(self, paper_id: str) -> str:
        return f"{self.BASE_URL}{self.PDF_PATH}{paper_id}"

    def _fetch_pdf(self, url: str) -> bytes:
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"Successfully retrieved the PDF from {response.url}")
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve the PDF: {e}")

    def _query_arxiv(self, query: str) -> Response:
        url = f"{self.SEARCH_API_URL}?{query}"
        print(f"Querying arXiv with URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"Successfully retrieved search results for '{query}'.")
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve search results: {e}")

    def _fetch_html(self, url: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"Successfully retrieved HTML content from {url}")
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve HTML content: {e}")

    @staticmethod
    def _parse_metadata_xml(xml: str) -> List[ArXivMetadata]:
        soup = BeautifulSoup(xml, "xml")
        entries = soup.find_all("entry")
        metadata = []

        for entry in entries:
            metadata.append(ArXivMetadata(
                title=entry.find("title").text.strip().replace("\n", ""),
                id=entry.find("id").text.strip().split("/")[-1],
                released=entry.find("published").text.strip(),
                abstract=entry.find("summary").text.strip().replace("\n", " "),
                authors=[author.find("name").text.strip() for author in entry.find_all("author")],
                primary_category=entry.find("arxiv:primary_category")["term"],
            ))

        return metadata

    @staticmethod
    def _parse_categories_html(html: str) -> List[ArXivCategory]:
        soup = BeautifulSoup(html, "html.parser")
        categories = []

        category_taxonomy_list = soup.find_all("div", id="category_taxonomy_list")
        for category in category_taxonomy_list:
            for group_name_element in category.find_all("h2", class_="accordion-head"):
                category_name = group_name_element.text.strip()
                accordion_body = group_name_element.find_next_sibling("div", class_="accordion-body")

                if accordion_body:
                    topics = accordion_body.find_all("h4")
                    categories.extend(ArXivService._parse_category_topics(category_name, topics))

        return categories

    @staticmethod
    def _parse_category_topics(category_name: str, topics) -> List[ArXivCategory]:
        parsed_categories = []

        for topic in topics:
            parsed_topic = re.match(r"(.+?)\s*\((.+?)\)", topic.text)
            if parsed_topic:
                topic_id = parsed_topic.group(1).strip()
                topic_name = parsed_topic.group(2).strip()
                description = re.sub(r"\s+", " ", topic.find_next("p").text).strip()
                parsed_categories.append(ArXivCategory(
                    id=topic_id,
                    name=topic_name,
                    category=category_name,
                    description=description,
                ))

        return parsed_categories

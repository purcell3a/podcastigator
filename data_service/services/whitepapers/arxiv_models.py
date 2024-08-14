from pydantic import BaseModel
from typing import List

class ArXivCategory(BaseModel):
    id: str
    name: str
    category: str
    description: str

class ArXivMetadata(BaseModel):
    title: str
    id: str
    released: str
    abstract: str
    authors: list[str]
    primary_category: str

# Simple base class with abstract-like methods (no implementation in this class)
class WhitePaperService:
    def get_white_paper(self, paper_id: str):
        raise NotImplementedError("This method should be overridden in a subclass.")

    def get_metadata(self, paper_id: str):
        raise NotImplementedError("This method should be overridden in a subclass.")

    def get_categories(self):
        raise NotImplementedError("This method should be overridden in a subclass.")

    def search(self, query: str):
        raise NotImplementedError("This method should be overridden in a subclass.")

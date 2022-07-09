from requests import get as get_
from bs4 import BeautifulSoup 
import pdfplumber
from io import BytesIO

class BaseCollector:

    soup = BeautifulSoup

    def collect(self, num_collect):
        print(f'Collecting data for {self.name}')
        urls = self.get_urls(num_collect)
        files = self.download_files(urls)
        return files

    def download_files(self, urls):
        files = []
        for url in urls:
            response = self.get(url)
            content = BytesIO(response.content)
            files.append(content)
        return files

    def get(self, url, **kwargs):
        return get_(url, **kwargs)

class BaseConverter:


    def convert(self, file):
        pages = self.get_pages(file)
        scrubbed = self.scrub_pages(pages)
        text = self.get_text(scrubbed)
        return text

    def get_text(self, file):
        return file

    def scrub_pages(self, file):
        return file

    def get_pages(self, file):
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
        return pages

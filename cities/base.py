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
        data = self.get_file_data(pages)
        return data

    def get_file_data(self, files):
        return files

    def scrub_pages(self, file):
        return file

    def get_pages(self, file):
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
        return pages

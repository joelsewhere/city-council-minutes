from ..base import BaseCollector

class Collector(BaseCollector):

    root = 'https://www.moline.il.us/'
    url = root + 'Archive.aspx?AMID=36&Type=&ADID='
    name = 'Moline, IL'

    def get_urls(self, num_elements):
        print(self.url)
        archives = self.get(self.url)
        soup = self.soup(archives.text)
        spans = soup.find_all('span', {'class': 'archive'})
        anchors = [x.find('a') for x in spans]
        urls = [self.root + x.attrs.get('href') 
                for x in anchors 
                if x 
                if x.attrs.get('href') 
                if 'draft' not in x.text.lower()][1:]
        return urls[:num_elements]
        



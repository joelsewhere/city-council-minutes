from re import T
from ..base import BaseConverter

class Converter(BaseConverter):

    def get_pages(self, file):
        pages = super().get_pages(file)
        for idx, page in enumerate(pages):
            pages[idx] = page.filter(lambda x: x['bottom'] - x['top'] < 100)
        return pages

    def get_file_data(self, pages):
        data = {}
        last_location = None
        for page in pages:
            page_data, last_location = self.parse_page(page, last_location)
            data.update(page_data)
        return data

    def parse_page(self, page, last_location):
        words = page.extract_words(keep_blank_chars=True,
                                   extra_attrs=['fontname', 
                                                'size',
                                               ]
                                  )
        data = {}
        header = ''
        underlined = False
        for word in words:
            bold = 'bold' in word.get('fontname', '').lower()
            is_underlined = self.is_underlined(word, page)
            text = word.get('text').strip()
            if is_underlined:
                print(text)
                underlined = text
                header = ''
                data[underlined] = {'header_text': [],
                                    'subheaders': {}}
            elif bold and isinstance(underlined, bool):
                header = text
                data[header] = {'header_text': [],
                                'subheaders': {}}
            elif bold:
                data[underlined]['subheaders'][text] = []
            elif not (header or underlined):

                last_location[-1] = last_location[-1] + ' ' + text

            else:
                italisized = 'italic' in word.get('fontname', '').lower()
                if underlined and header:
                    location = data[underlined]['subheaders'][header]
                elif underlined and not header:
                    location = data[underlined]['header_text']
                else:
                    location = data[header]['header_text']
                if italisized and location and text:
                    location[-1] = location[-1] + ' ' + text
                elif text:
                    location.append(text)
        return data, location

    def is_underlined(self, word, page):
        def params(data):
            params = ['top',
                      'bottom',
                      'x1']
            return [data.get(x, 1000) for x in params]

        word_params = params(word)

        for rect in page.rects:
            rect_params = params(rect)
            top_diff = rect_params[0] - word_params[0]
            bottom_diff = word_params[1] - rect_params[1] 
            x1_diff = word_params[2] - rect_params[2]

            if abs(bottom_diff) < 1 and int(x1_diff) <= 3:
                print()
                print('Top:   ', top_diff)
                print('Bottom:', bottom_diff)
                print('x1:    ', x1_diff)
                return True

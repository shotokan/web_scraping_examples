import re
import json
import codecs

from bs4 import BeautifulSoup as bs, SoupStrainer


class Crawler:

    def __init__(self):
        self.page_content = None

    def _clean_html(self, html):
        """
        Utility function used to clean html. It closes tds tags.
        :param html:
        :return: string: represent the html
        """
        html = html.replace('</A>', '</div></td>')
        # Find all td tags without </td>
        regex = r'^<td>((.(?!</td>))*)$'
        # add </td> tag
        html = re.sub(regex, r'<td>\1</td>', html, flags=re.MULTILINE)
        return html

    def get_page(self, file_name, file_type):
        """
        Utility function which open a file and returns a beautifulsoup object.
        :param file_name: file name
        :param file_type: file type
        :return: beautifulsoup
        """
        try:
            with open('{}.{}'.format(file_name, file_type), 'r') as f:
                html = f.read()
                # It's necessary to clean up the html (some tags are not closed)
                html = self._clean_html(html)
                only_tables = SoupStrainer("table")
                self.page_content = Content(file_name)
                return bs(html, 'html.parser',  parse_only=only_tables)
        except Exception as exc:
            print(exc)
            raise exc

    def _get_table_by_text(self, page, pattern):
        """
        Utility function used to get a table element from a Beautiful Soup object, using a text pattern.
        Returns None if no object is found for the given selector
        """
        search_text = re.compile('^{0}'.format(pattern), re.IGNORECASE)
        table = page.find(text=search_text).find_parent('table')
        return table

    def _get_data(self, tr):
        """
        Utility function used to get values from a tr
        :param tr:
        :return: list: register values
        """
        tds = tr.find_all('td')
        values = []
        for i, td in enumerate(tds):
            if len(tds) - 1 == i:
                img = td.find('img') or ''
                values.append(str(img))
                link = td.find('a')
                if link is not None:
                    link = link.attrs['href']
                    if link is not None and link != '':
                        values.append(link)
                        # add new heading
                        self.page_content.add_heading('pdf_link')
                break
            values.append(td.get_text(strip=True).replace('\n', '').replace('\t', '').strip())
            # add values into content data
        return self.page_content.generate_data(values)

    def _get_headings(self, tr):
        """
        Utility function used to get heading values and return them into a list.
        :param tr:
        :return: list: headings
        """
        tds = tr.find_all('td')
        # add headings
        [self.page_content.add_heading(td.get_text(strip=True).strip()) for td in tds]

    def parse(self, page, text='Viewed'):
       """
       Function used to parse and save into a file, all values found in an Html.
       :param page: beautifulsoup object
       :param text: patter to search
       :return:
       """
       if self.page_content is None:
           raise Exception("Error, You must get a Page...")
       table = self._get_table_by_text(page, text)
       # search for all registers in the table
       trs = table.find_all('tr')
       headings = self._get_headings(trs[0])
       # Get a list with columns values
       values = [self._get_data(tr) for tr in trs[1:]]
       #self.page_content.generate_data(values)
       self.page_content.save_data()
       self.page_content = None


class Content:
    """
    Common base class for all tables/pages
    """
    def __init__(self, title):
        self.title = title
        self.data = []
        self.headings = {}

    def add_heading(self, heading):
        if heading != '':
            index = 0 if len(self.headings) == 0 else len(self.headings)
            self.headings[index] = heading

    def generate_data(self, values):
        """
        Function used to generate a dictionary and append it into a list.
        :param values: list of values
        :return: dictionary
        """
        register = dict()
        for index, value in enumerate(values):
            heading = self.headings[index]
            register[heading] = value
        self.data.append(register)
        return True

    def save_data(self):
        """
        Function used to save into a file all data found in a table.
        :return:
        """
        with open(self.title + '.json', 'wb') as f:
            print("Saving data: {}".format(self.title))
            json.dump(self.data, codecs.getwriter('utf-8')(f), ensure_ascii=False)


if __name__ == '__main__':
    files = ['q6-1', 'q6-2', 'q6-3']
    crawler = Crawler()
    for file in files:
        print("{} is opening.").format(file)
        page = crawler.get_page(file, 'html')
        print("Parsing data...")
        crawler.parse(page)
        print("Finished")



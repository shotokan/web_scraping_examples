import urllib2
import json
import io
import codecs
from bs4 import BeautifulSoup as bs


class Crawler:
    """
    Generator class to parse data from eapps.courts.state.va.us
    """

    def __init__(self, id=23800):
        self.content = Content()
        self.currentId = id
        self.MAX = id + 50

    def __iter__(self):
        return self

    def next(self):
        """ for python 2.7 """
        print('next')
        return self.__next__()

    def __next__(self):
        """ For python 3"""
        next_value = self.currentId
        if next_value >= self.MAX:
            # When 50 pages are reached all data is saved into a json file.
            if self._save('q4'):
                print("SAVED...")
            raise StopIteration
        self.currentId += 1
        url = 'https://eapps.courts.state.va.us/cav-public/caseInquiry/showCasePublicInquiry?caseId={}'
        soup = self._get_page(url, self.currentId)
        # Parse data from actual URL
        data = self._generate_data(soup)
        return data

    def _get_page(self, url, case_id):
        """
        Utility function which open a file and returns a beautifulsoup object.
        :param url:
        :param case_id: caseId to query
        :return:
        """
        try:
            url = url.format(case_id)
            req = urllib2.Request(url)
            print(url)
            response = urllib2.urlopen(req)
            return bs(response.read(), 'html.parser')
        except urllib2.URLError as err:
            print(err)
            raise err

    def _generate_data(self, soup):
        """
        Utility function used to get values (appellee, cav, appellant, date).
        :param soup:
        :return:
        """
        # Get table with appellee data
        grid_text = soup.find(id='listAllPartiesAPL').findAll(class_='gridText')
        appellant = ""
        for g in grid_text:
            # There could be several records with the appellant data, so we take the first which is not empty.
            appellant = g.text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            if appellant != "":
                break
        grid_text = soup.find(id='listAllPartiesAPE').findAll(class_='gridText')
        print(grid_text)
        appellee = ""
        for g in grid_text:
            # There could be several records with the appellee data, so we take the first which is not empty.
            appellee = g.text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            if appellee != "":
                break
        # Searching for cav
        cav = soup.find(id='caseStyle').text
        cav = cav.replace(' ', '').replace('\t', '')
        cav = cav.split('#')
        cav = cav[1].strip()
        # Searching for date
        date = soup.find(id='noticeOfAplDt').attrs['value']
        # Data is turned into a dictionary
        data_generated = self.content.generate_dict(appellee, appellant, cav, date)
        return data_generated

    def _save(self, title='q4'):
        try:
            self.content.save_data(title)
            return True
        except:
            return False


class Content:
    """
    Common base class for all tables/pages
    """
    def __init__(self):
        self.data = []
        self.index = 0

    def generate_dict(self, appellee, appellant, cav, date):
        self.index += 1
        my_dict = {
            'index': self.index,
            'appellee': appellee,
            'appellant': appellant,
            'cav': cav,
            'date': date
        }
        self.data.append(my_dict)
        return my_dict

    def save_data(self, file_name='default'):
        if len(self.data) > 0:
            with open(file_name + '.json', 'wb') as f:
                json.dump(self.data, codecs.getwriter('utf-8')(f), ensure_ascii=False)
        else:
            print("Empty")


if __name__ == '__main__':
    crawler = Crawler()

    # Generator is iterated
    for data in crawler:
        print(data)

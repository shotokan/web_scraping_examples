import urllib2
import json
import io
import codecs
from bs4 import BeautifulSoup as bs

# TODO: PENDING - the website is failing
class Crawler:

    def get_page(self, url, case_id):
        try:
            url = url.format(case_id)
            req = urllib2.Request(url)
            print(url)
            response = urllib2.urlopen(req)
            return bs(response.read(), 'html.parser')
        except urllib2.URLError as err:
            print(err)
            raise err

    def save_data(self, data, file_name='default'):
        with io.open(file_name + '.json', 'w',  encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

    def save_data2(self, data, file_name='default'):
        with open(file_name + '.json', 'wb') as f:
            json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)

    def generate_data(self, soup):
        grid_text = soup.find(id='listAllPartiesAPL').findAll(class_='gridText')
        print(grid_text)
        appellant = ""
        for g in grid_text:
            appellant = g.text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            if appellant != "":
                break
        grid_text = soup.find(id='listAllPartiesAPE').findAll(class_='gridText')
        print(grid_text)
        appellee = ""
        for g in grid_text:
            appellee = g.text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            if appellee != "":
                break
        cav = soup.find(id='caseStyle').text
        cav = cav.replace(' ', '').replace('\t', '')
        # cav = cav[1].replace(' ', '')
        print(cav)
        cav = cav.split('#')
        cav = cav[1].strip()
        date = soup.find(id='noticeOfAplDt').attrs['value']
        content = Content()
        content.generate_dict(appellee, appellant, cav, date)
        content.save_data2('q4')


class Content:

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

    def save_data2(self, file_name='default'):
        if len(self.data) > 0:
            with open(file_name + '.json', 'wb') as f:
                json.dump(self.data, codecs.getwriter('utf-8')(f), ensure_ascii=False)
        else:
            print("Empty")


if __name__ == '__main__':
    crawler = Crawler()
    url = 'https://eapps.courts.state.va.us/cav-public/caseInquiry/showCasePublicInquiry?caseId={}'
    for id in range(23800, 23851):
        soup = crawler.get_page(url, id)
        crawler.generate_data(soup)

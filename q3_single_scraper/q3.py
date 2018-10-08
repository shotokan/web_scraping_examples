import urllib2
import json
import io
import codecs
from bs4 import BeautifulSoup as bs


class Crawler:

    def get_page(self, url):
        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            return response.read()
        except urllib2.URLError as err:
            print(err)
            raise err

    def save_data(self, data, file_name='default'):
        with io.open(file_name + '.json', 'w',  encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

    def save_data2(self, data, file_name='default'):
        with open(file_name + '.json', 'wb') as f:
            json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)


class Content:
    """
    Common base class for all tables/pages
    """
    pass


if __name__ == '__main__':
    crawler = Crawler()
    html = crawler.get_page('https://eapps.courts.state.va.us/cav-public/caseInquiry/showCasePublicInquiry?caseId=23814')
    soup = bs(html, 'html.parser')
    grid_text = soup.find(id='listAllPartiesAPL').findAll(class_='gridText')
    print(grid_text)
    name = ""
    for g in grid_text:
        name = g.text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
        if name != "":
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
    #cav = cav[1].replace(' ', '')
    print(cav)
    cav = cav.split('#')
    cav = cav[1].strip()
    date = soup.find(id='noticeOfAplDt').attrs['value']
    my_dict = {
        'appellee': appellee,
        'appellant': name,
        'cav': cav,
        'date': date
    }
    crawler.save_data(my_dict, 'my_json')
    crawler.save_data2(my_dict, 'my_json2')

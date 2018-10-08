import urllib2
import urllib
import json
import io
import codecs
import urlparse
from bs4 import BeautifulSoup as bs


class Crawler:
    def __init__(self):
        pass

    def get_page(self, url, values=None):
        """
        Function used to download a website, and returns a beautifulsoup object. It can send form data as well.
        :param url:
        :param values:
        :return:
        """
        try:
            if values is not None:
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data)
            else:
                req = urllib2.Request(url)
            print("downloading website...")
            print(url)
            response = urllib2.urlopen(req)
            return bs(response.read(), 'html.parser')
            # return response.read()
        except urllib2.URLError as err:
            print(err)
            raise err

    def save_data(self, data, file_name='default'):
        """
        Function used to save data into a file.
        :param data:
        :param file_name:
        :return:
        """
        with io.open(file_name + '.html', 'w',  encoding='utf-8') as f:
            f.write(data)

    def save_data2(self, data, file_name='default'):
        """
        Function used to save a json file.
        :param data:
        :param file_name:
        :return:
        """
        with open(file_name + '.html', 'wb') as f:
            f.write(data)

    def get_form(self, page):
        """
        Function utility used to find a form element.
        :param page:
        :return:
        """
        form = page.find('form')
        return form

    def get_inputs(self, form):
        """
        Function utility used to find all inputs elements in a form.
        :param form:
        :return:
        """
        fields = form.findAll('input')
        formdata = dict((field.get('name'), field.get('value')) for field in fields)
        return formdata

    def click_checbox(self, formdata):
        """
        Function utility used to simulate a click on checkbox
        :param formdata:
        :return:
        """
        print("Checkbox clicked...")
        formdata['disclaimer'] = 'Y'
        return formdata

    def click_send_form(self, form):
        """
        Function utility used to generate the url to which the form will be sent.
        :param form:
        :return:
        """
        print("select continue")
        return urlparse.urljoin(URL, form['action'])


if __name__ == '__main__':
    crawler = Crawler()
    URL = 'http://casesearch.courts.state.md.us/casesearch/'
    page = crawler.get_page(URL)
    crawler.save_data2(str(page).strip(), 'q5-1')
    # Find form and parse it.
    form = crawler.get_form(page)
    formdata = crawler.get_inputs(form)
    formdata = crawler.click_checbox(formdata)
    # Select continue
    posturl = crawler.click_send_form(form)
    # Downloading next page
    page2 = crawler.get_page(posturl, formdata)
    crawler.save_data2(str(page2).strip(), 'q5-2')





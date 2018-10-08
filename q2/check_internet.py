import urllib2
import socket


def find_local_ip():
    """
    Function used to find local ip
    :return:
    """
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return "IP->{1}".format(hostname, ip)
    except socket.error as err:
        print(err)


def internet_on():
    """
    Function used to check if there is internet connection
    :return:
    """
    try:
        urllib2.urlopen('https://www.google.com/', timeout=3)
        return True
    except urllib2.URLError as err:
        print(err)
        return False


if __name__ == '__main__':
    print(find_local_ip())
    message = 'connected' if internet_on() else 'not connected'
    print(message)

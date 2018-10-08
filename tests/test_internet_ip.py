import unittest

from q2.check_internet import internet_on, find_local_ip


class InternetTestCase(unittest.TestCase):
    """
    Tests for q1/c.py
    """

    def test_connection(self):
        resp = internet_on()
        self.assertIsInstance(resp, bool)

    def test_ip(self):
        resp = find_local_ip()
        index = resp.find('IP->')
        self.assertIsNot(index, -1)

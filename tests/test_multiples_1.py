import unittest

from q1.c import find_multiples, _is_multiple_of_seven, _is_multiple_of_six


class MultiplesTestCase(unittest.TestCase):
    """
    Tests for q1/c.py
    """

    def test_is_multiple_of_six(self):
        """ is multiple of 6 """
        self.assertTrue(_is_multiple_of_six(6))

    def test_is_multiple_of_seven(self):
        self.assertTrue(_is_multiple_of_seven(7))

    def test_multiples_alarm(self):
        resp = find_multiples(12)
        self.assertEquals(resp, 'Alarm')

    def test_multiples_docket(self):
        resp = find_multiples(14)
        self.assertEquals(resp, 'Docket')

    def test_multiples_alarm_alarm(self):
        resp = find_multiples(42)
        self.assertEquals(resp, 'Docket Alarm')

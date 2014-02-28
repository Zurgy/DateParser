import pytest
from datetime import date
from date_parser import DateParser


class TestDateParser(object):
    @pytest.mark.parametrize("test_input,expected", [
        ('3 Jan 2014', (2014, 1, 3)),
            ('3rd Jan 2014', (2014, 1, 3)),
            ('Mon 24 Jan', (2014, 1, 24)),
            ('Friday 3rd January 2014', (2014, 1, 3)),
            ('Fri 3rd Jan', (2014, 1, 3)),
            ('28th Feb', (2014, 2, 28)),
            ('3 Jan', (2014, 1, 3)),
            ('Wednesday 26th Feb 2014', (2014, 2, 26))
    ])
    def test_simple_date(self, test_input, expected):
        date_parser = DateParser()
        result = date_parser.parse(test_input)
        assert result[0].date == date(*expected)
        print("{0} = {1}".format(test_input, result))

    @pytest.mark.parametrize("test_input,start_date,end_date", [
        ('From 3rd Jan until 14th', (2014, 1, 3), (2014, 1, 14)),
        ('12 - 25 Jan', (2014, 1, 12), (2014, 1, 25)),
        ('12 Jan - 25 Feb', (2014, 1, 12), (2014, 2, 25)),
        ('11 January 2014 until 14 February 2014', (2014, 1, 11), (2014, 2, 14))
    ])
    def test_date_range(self, test_input, start_date, end_date):
        date_parser = DateParser()
        result = date_parser.parse(test_input)
        assert result[0].start_date.date == date(*start_date)
        assert result[0].end_date.date == date(*end_date)
        print("{0} = {1}".format(test_input, result))

    def test_date_list(self):
        tests = [
            '3, 4, 5 January'
            '3, 5, 11 Jan, 6, 7 Feb'
        ]

    def test_open_ended_dates(self):
        tests = [
            'Unit 21st Jan',
            'From 11 Feb'
        ]
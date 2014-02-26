from datetime import date
from pyparsing import Group, Literal, Optional, Suppress, Word, nums, stringEnd


# SingleDate, DateRange, DateList
# InvalidDateException(day of week does not agree with date, day does not exist in month,
# year is not a leap year
# guessed_year = True

SHORT_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
LONG_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
               'October', 'November', 'December']


class SingleDate(object):
    def __init__(self, parse_result):

        if parse_result.month == '':
            month = 1
        elif len(parse_result.month) == 3:
            month = SHORT_MONTHS.index(parse_result.month) + 1
        else:
            month = LONG_MONTHS.index(parse_result.month) + 1

        year = int(parse_result.year) if parse_result.year is not '' else 2014

        self.date = date(year, month, int(parse_result.day[0]))

    def __repr__(self):
        return str(self.date)


class DateRange(object):
    def __init__(self, parse_result):
        self.start_date = parse_result.start_date
        self.end_date = parse_result.end_date

    def __repr__(self):
        return '{0} to {1}'.format(self.start_date, self.end_date)


class DateParser(object):
    @staticmethod
    def _build_literal(list_of_words):
        x = Literal(list_of_words[0])
        for s in list_of_words[1:]:
            x = x | Literal(s)

        return x

    @staticmethod
    def parse(date_string):
        # Parser for individual dates
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
                        'Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        suffixes = Literal('nd') | Literal('rd') | Literal('st') | Literal('th')

        day_of_month = Group(Word(nums) + Suppress(Optional(suffixes))).setResultsName('day')

        single_date = Optional(DateParser._build_literal(days_of_week)).setResultsName('dow') + day_of_month + \
                      Optional(DateParser._build_literal(LONG_MONTHS + SHORT_MONTHS)).setResultsName('month') + \
                      Optional(Word(nums)).setResultsName('year')
        single_date.setParseAction(SingleDate)



        # Parser for date ranges
        date_range_separators = DateParser._build_literal(['-', 'until', 'to'])
        date_range = Suppress(Optional('From')) + single_date.setResultsName('start_date') + \
                            Suppress(date_range_separators) + single_date.setResultsName('end_date')
        date_range.setParseAction(DateRange)


        date_parser = (date_range | single_date) + stringEnd

        result = date_parser.parseString(date_string)

        return result
        # TODO Validate year if exists
        # TODO Convert month into a integrate and validate


if __name__ == '__main__':
    parser = DateParser()
    print parser.parse('Monday 3 January')
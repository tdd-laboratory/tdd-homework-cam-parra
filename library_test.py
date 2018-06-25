import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''
# really? Why are you writing python code you three year old
BIRTHDAY = '''I was born on 2015-07-25.'''
class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)
    
    # Fourth unit test; prove that we can extract a date 
    def test_birthday(self):
        self.assert_extract(BIRTHDAY, library.dates_iso8601, '2015-07-25')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_max_dates(self):
        self.assert_extract("2013-13-32", library.dates_iso8601)

    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')


    def test_date_long_fmt(self):
        self.assert_extract('I was born on 25 January 2017.', library.dates_fmt2, '25 January 2017')

    def test_date_american_order_fmt(self):
        self.assert_extract('I was born on January 25 2017.', library.dates_fmt2, 'January 25 2017')

    def test_date_ordinals_order_fmt(self):
        self.assert_extract('I was born on January 25th 2017.', library.dates_fmt2, 'January 25th 2017')

    def test_seperated_date(self):
        self.assert_extract('I was born on January 25 of 2017.', library.dates_fmt2, 'January 25 2017')

    def test_dates_with_time_stamps(self):
        self.assert_extract("2018-06-22 18:22:19.123", library.dates_iso8601, "2018-06-22 18:22:19.123")

    def test_dates_with_commas(self):
        self.assert_extract("2018,06,22", library.dates_iso8601, "2018 06 22")

    def test_dates_with_commas_american(self):
        self.assert_extract("06,22,2018", library.dates_iso8601, "2018 06 22")

    def test_date_with_comma_fmt(self):
        self.assert_extract('I was born on Jan 25, 2017.', library.dates_fmt2, 'January 25, 2017')

    def test_date_with_day_first(self):
        self.assert_extract('I was born on 25 January 2017.', library.dates_fmt2, '25 January 2017')

    def test_date_without_space(self):
        self.assert_extract('I was born on Jan252017.', library.dates_fmt2, 'January 25 2017')


if __name__ == '__main__':
    unittest.main()


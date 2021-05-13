import datetime
import unittest
from typing import List

from tgt.daterange import DateRange


class TestDateRange(unittest.TestCase):

    def test_date_range_contains(self):
        d = DateRange('2020-04-01,2020-05-01..2020-05-20,2020-06-01..')
        self.assertTrue('2019-03-31' not in d)
        self.assertTrue('2020-03-31' not in d)
        self.assertTrue('2020-04-01' in d)
        self.assertTrue('2020-04-02' not in d)
        self.assertTrue('2020-05-01' in d)
        self.assertTrue('2020-05-10' in d)
        self.assertTrue('2020-05-20' in d)
        self.assertTrue('2020-05-21' not in d)
        self.assertTrue('2020-06-01' in d)
        self.assertTrue('2020-06-02' in d)
        self.assertTrue('2021-06-02' in d)

    def test_date_range_min_max(self):
        d = DateRange('2020-04-01,2020-05-01..2020-05-20,2020-06-01..')
        self.assertEqual(datetime.date.fromisoformat('2020-04-01'), d.min)
        self.assertEqual(None, d.max)
        d = DateRange('2020-04-01,2020-05-01..2020-05-20,2020-06-01..,2019-01-01')
        self.assertEqual(datetime.date.fromisoformat('2019-01-01'), d.min)
        self.assertEqual(None, d.max)
        d = DateRange('2020-04-01,2020-05-01..2020-05-20,2020-06-01..2020-06-15,2019-01-01')
        self.assertEqual(datetime.date.fromisoformat('2019-01-01'), d.min)
        self.assertEqual(datetime.date.fromisoformat('2020-06-15'), d.max)
        d = DateRange('2020-04-01,2020-05-01..2020-05-20,2031-03-15,2020-06-01..2020-06-15,..2019-01-01')
        self.assertEqual(None, d.min)
        self.assertEqual(datetime.date.fromisoformat('2031-03-15'), d.max)

    def test_date_range_iter(self):
        d = DateRange('2020-01-01..2020-01-04')
        self.assertEqual([
            datetime.date.fromisoformat('2020-01-01'),
            datetime.date.fromisoformat('2020-01-02'),
            datetime.date.fromisoformat('2020-01-03'),
            datetime.date.fromisoformat('2020-01-04'),
        ], [*iter(d)])
        d = DateRange('2020-01-01..')
        self.assertEqual([
            datetime.date.fromisoformat('2020-01-01'),
            datetime.date.fromisoformat('2020-01-02'),
            datetime.date.fromisoformat('2020-01-03'),
        ], [*d.iter(upper='2020-01-03')])

    def test_date_range_months(self):
        d = DateRange('2021-02')
        self.assertEqual(28, len([*d]))
        d = DateRange('2020-02')
        self.assertEqual(29, len([*d]))
        d = DateRange('2020-12')
        self.assertEqual(31, len([*d]))

    def test_date_range_month_bounds(self):
        d = DateRange('2020-01..2020-12')
        self.assertEqual(datetime.date.fromisoformat('2020-01-01'), d.min)
        self.assertEqual(datetime.date.fromisoformat('2020-12-31'), d.max)

    def test_date_range_itermonths(self):
        ranges: List[DateRange] = [*DateRange('2020-01..2020-12').itermonths()]
        self.assertEqual(12, len(ranges))
        for month, date_range in enumerate(ranges, start=1):
            self.assertEqual(1, date_range.min.day)
            self.assertEqual(month, date_range.min.month)
            self.assertEqual(month, date_range.max.month)

    def test_date_comparison(self):
        r1 = DateRange('..2021-08-01')

        self.assertTrue(datetime.date.fromisoformat('2021-07-01') <= r1)
        self.assertTrue(datetime.date.fromisoformat('2021-07-01') >= r1)
        self.assertFalse(datetime.date.fromisoformat('2021-07-01') < r1)
        self.assertFalse(datetime.date.fromisoformat('2021-07-01') > r1)

        self.assertTrue(datetime.date.fromisoformat('2021-08-01') <= r1)
        self.assertTrue(datetime.date.fromisoformat('2021-08-01') >= r1)
        self.assertFalse(datetime.date.fromisoformat('2021-08-01') < r1)
        self.assertFalse(datetime.date.fromisoformat('2021-08-01') > r1)

        self.assertFalse(datetime.date.fromisoformat('2021-08-02') <= r1)
        self.assertTrue(datetime.date.fromisoformat('2021-08-02') >= r1)
        self.assertFalse(datetime.date.fromisoformat('2021-08-02') < r1)
        self.assertTrue(datetime.date.fromisoformat('2021-08-02') > r1)

        r2 = DateRange('2020-07-01..2020-08-01')

        self.assertTrue(datetime.date.fromisoformat('2020-06-01') <= r2)
        self.assertFalse(datetime.date.fromisoformat('2020-06-01') >= r2)
        self.assertTrue(datetime.date.fromisoformat('2020-06-01') < r2)
        self.assertFalse(datetime.date.fromisoformat('2020-06-01') > r2)

        self.assertTrue(datetime.date.fromisoformat('2020-07-01') <= r2)
        self.assertTrue(datetime.date.fromisoformat('2020-07-01') >= r2)
        self.assertFalse(datetime.date.fromisoformat('2020-07-01') < r2)
        self.assertFalse(datetime.date.fromisoformat('2020-07-01') > r2)

        self.assertTrue(datetime.date.fromisoformat('2020-08-01') <= r2)
        self.assertTrue(datetime.date.fromisoformat('2020-08-01') >= r2)
        self.assertFalse(datetime.date.fromisoformat('2020-08-01') < r2)
        self.assertFalse(datetime.date.fromisoformat('2020-08-01') > r2)

        self.assertFalse(datetime.date.fromisoformat('2020-08-02') <= r2)
        self.assertTrue(datetime.date.fromisoformat('2020-08-02') >= r2)
        self.assertFalse(datetime.date.fromisoformat('2020-08-02') < r2)
        self.assertTrue(datetime.date.fromisoformat('2020-08-02') > r2)

        r3 = DateRange('2019-08-01..')

        self.assertTrue(datetime.date.fromisoformat('2019-07-01') <= r3)
        self.assertFalse(datetime.date.fromisoformat('2019-07-01') >= r3)
        self.assertTrue(datetime.date.fromisoformat('2019-07-01') < r3)
        self.assertFalse(datetime.date.fromisoformat('2019-07-01') > r3)

        self.assertTrue(datetime.date.fromisoformat('2019-08-01') <= r3)
        self.assertTrue(datetime.date.fromisoformat('2019-08-01') >= r3)
        self.assertFalse(datetime.date.fromisoformat('2019-08-01') < r3)
        self.assertFalse(datetime.date.fromisoformat('2019-08-01') > r3)

        self.assertTrue(datetime.date.fromisoformat('2019-08-02') <= r3)
        self.assertTrue(datetime.date.fromisoformat('2019-08-02') >= r3)
        self.assertFalse(datetime.date.fromisoformat('2019-08-02') < r3)
        self.assertFalse(datetime.date.fromisoformat('2019-08-02') > r3)

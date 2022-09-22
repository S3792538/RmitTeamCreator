import unittest

from TeamCreator.views import parse_csv_content
from TeamCreator.teams import group_students

class TestViews(unittest.TestCase):
    def test_parse_csv(self):
        with open(r'./TestInput/Team allocation preferences.csv', 'r') as f:
            csv = f.read()
            students = parse_csv_content(csv)
            self.assertTrue(len(students) > 100)


class TestTeams(unittest.TestCase):
    def test_grouping(self):
        with open(r'./TestInput/Team allocation preferences.csv', 'r') as f:
            csv = f.read()
            students = parse_csv_content(csv)
            groups = group_students(students)

            self.assertEqual(len(groups), 5)

if __name__ == '__main__':
    unittest.main()

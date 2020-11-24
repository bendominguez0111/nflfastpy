import unittest
import sys, os
import pandas as pd
import nflfastpy

class TestAllFunctions(unittest.TestCase):

    def test_dfs(self):

        version = nflfastpy.__version__

        df = nflfastpy.load_pbp_data(2020)
        self.assertEqual(type(df), pd.DataFrame)
        self.assertFalse(df.empty)

        df = nflfastpy.load_roster_data()
        self.assertEqual(type(df), pd.DataFrame)
        self.assertFalse(df.empty)

        df = nflfastpy.load_2020_roster_data()
        self.assertEqual(type(df), pd.DataFrame)
        self.assertFalse(df.empty)

        df = nflfastpy.load_team_logo_data()
        self.assertEqual(type(df), pd.DataFrame)
        self.assertFalse(df.empty)

        df = nflfastpy.load_schedule_data(2020)
        self.assertEqual(type(df), pd.DataFrame)
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()
import unittest
import pandas as pd
import sys
import os

# Add the project root to the path so we can import helpers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import helpers

class TestHelpers(unittest.TestCase):
    def test_aq_score_function(self):
        # aqs = (aq1 * 0.2) + (aq2 * 0.2) + ...
        result = helpers.aq_score_function(0.5, 0.5, 0.5, 0.5, 0.5)
        self.assertAlmostEqual(result, 0.5)

        result2 = helpers.aq_score_function(1, 0, 1, 0, 1)
        self.assertAlmostEqual(result2, 0.6)

    def test_convert_point_list_to_df(self):
        points = [(51.5, -0.1), (51.6, -0.2)]
        df = helpers.convert_point_list_to_df(points)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['Latitude', 'Longitude'])
        self.assertEqual(df.iloc[0]['Latitude'], 51.5)
        self.assertEqual(df.iloc[1]['Longitude'], -0.2)

    def test_greenspace_score_function(self):
        # test logic for greenspace_score_function
        # greenspace_score_function(aqs, pop_density, airport, water, building, green_space, railway_station, urban_area, dist_nearest_greenspace, popd_weight)
        score, penalty = helpers.greenspace_score_function(
            aqs=0.5, pop_density=0.5, airport=0, water=0, building=0,
            green_space=0, railway_station=0, urban_area=0, dist_nearest_greenspace=0, popd_weight=1.0
        )
        self.assertAlmostEqual(penalty, 1.25)
        
        self.assertAlmostEqual(score, 0.625)

if __name__ == '__main__':
    unittest.main()

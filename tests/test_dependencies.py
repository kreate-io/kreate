import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dependencies 

def test_match_charts():
        src_paths = ['./tests/data/src_pg.js', './tests/data/src_mongodb.js','./tests/data/src_mysql.js']

        charts = dependencies.Dependencies().match_charts(src_paths)
        
        assert charts
        assert len(charts) == 3

        assert charts[0]['chart'] == 'https://github.com/kubernetes/charts/blob/master/stable/postgresql/Chart.yaml'
        assert charts[1]['chart'] == 'https://github.com/kubernetes/charts/blob/master/stable/mongodb/Chart.yaml'
        assert charts[2]['chart'] == 'https://github.com/kubernetes/charts/tree/master/stable/mysql/Chart.yaml'
        
test_match_charts()

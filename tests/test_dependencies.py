import pytest
import sys
import os
from kreate import helm
from kreate import dependencies 
import logging

repo_name = "charts"
repo_url = "https://github.com/kubernetes/charts.git"
folders = ["stable", "incubator"]

def test_match_charts():
        src_paths = ['./tests/data/src_pg.js', './tests/data/src_mongodb.js','./tests/data/src_mysql.js']

        helm_charts = helm.Helm(repo_name, repo_url, folders, logging.getLogger())
        charts = helm_charts.get_helm_charts_details()
        charts = dependencies.Dependencies().match_charts(charts, src_paths)
        
        assert charts
        assert len(charts) == 3
        #assert 'postgres' in charts[0][0]['name']

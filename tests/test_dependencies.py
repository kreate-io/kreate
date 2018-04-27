import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

def test_dependency_to_keywords():
        dep_lines = [
                "const pg = require('pg');",
                "var MongoClient = require('mongodb').MongoClient;",
                "var mysql = require('mysql');",
                "using MySql.Data.MySqlClient",
                "using System.IO"
        ]

        expected_keywords = [
                [ 'pg'],
                ['mongoclient', 'mongodb'],
                ['mysql'],
                ['mysql', 'data', 'mysqlclient'],
                ['system', 'io']
        ]

        for i in range(0, len(dep_lines)):
                keywords = dependencies.Dependencies().__dependency_to_keywords__(dep_lines[i])
                assert set(keywords) == set(expected_keywords[i])

test_match_charts()
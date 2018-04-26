import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kreate import helm
from kreate import dependencies
import logging

repo_name = "charts"
repo_url = "https://github.com/kubernetes/charts.git"
folders = ["stable", "incubator"]

def test_flow():
    helm_charts = helm.Helm(repo_name, repo_url, folders, logging.getLogger())
    charts = helm_charts.get_helm_charts_details()
    deps = dependencies.Dependencies()
    results = deps.__match_charts__(1, charts, ['pg'])
    assert 'postgres' in results[0]['name']

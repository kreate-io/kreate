import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helm
import logging

repo_name = "charts"
repo_url = "https://github.com/kubernetes/charts.git"
folders = ["stable", "incubator"]


def test_flow():
    helm_charts = helm.Helm(repo_name, repo_url, folders, logging.getLogger())
    charts_details = helm_charts.get_helm_charts_details()
    assert(len(charts_details) > 0)

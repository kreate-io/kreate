from kreate import helm
from kreate import handler
import logging

repo_name = "charts"
repo_url = "https://github.com/kubernetes/charts.git"
folders = ["stable", "incubator"]


def test_flow():
    helm_charts = helm.Helm(repo_name, repo_url, folders, logging.getLogger())
    charts_details = helm_charts.get_helm_charts_details()
    handler_inst = handler.Handler()
    handler_inst.download_models()
    name = handler_inst.__generate_name__("stable/mysql")
    private_rep_name = handler_inst.__generate_name__("mysql")
    assert name == 'mysql-kreate'
    assert private_rep_name == 'mysql-kreate'


test_flow()

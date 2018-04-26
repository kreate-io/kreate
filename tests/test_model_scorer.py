from kreate import helm
from kreate import model_scorer
import logging

repo_name = "charts"
repo_url = "https://github.com/kubernetes/charts.git"
folders = ["stable", "incubator"]

def test_flow():
    helm_charts = helm.Helm(repo_name, repo_url, folders, logging.getLogger())
    charts = helm_charts.get_helm_charts_details()
    scorer = model_scorer.Scorer()
    results = scorer.predict_charts(charts, ['pg'])
    assert 'postgresql' in results

import helm
import codefinder

from knack.log import get_logger
logger = get_logger(__name__)


class Handler(object):

    def __init__(self):
        self.extensions = [".py", ".js", ".ts", ".go", ".cs", ".java"]
        
    def get_helm_charts_details(self, repo_name, repo_url, folders):
        self.helm_charts = helm.Helm(repo_name, repo_url, folders, logger)
        charts_details = self.helm_charts.get_helm_charts_details()
        return charts_details

    def install_helm_chart(self, name, chart_name, namespace):
        self.helm_charts.install_helm_chart(name, chart_name, namespace)

    def get_source_files(self, path):
        fileGetter = codefinder.CodeFinder(path, self.extensions)
        files = fileGetter.get_code_files()
        return files

import os
import re
import tempfile
import urllib.request

from knack.log import get_logger
from kreate import codefinder, dependencies, helm

logger = get_logger(__name__)


class Handler(object):

    def __init__(self):
        self.extensions = [".py", ".js", ".ts", ".go", ".cs", ".java", ".rb"]
        self.ignore_folders = ["node_modules", "vendor", "bin", "lib", "obj"]
        self.helm_charts = None

    @staticmethod
    def download_models():
        urllib.request.urlretrieve('https://github.com/kreate-io/kreate/raw/master/models/dependency_model.pkl',
                                   os.path.join(tempfile.gettempdir(), 'dependency_model.pkl'))

    def get_helm_charts_details(self, repo_name, repo_url, folders):
        self.helm_charts = helm.Helm(repo_name, repo_url, folders, logger)
        charts_details = self.helm_charts.get_helm_charts_details()
        return charts_details

    @staticmethod
    def match_source_to_charts(src_files, charts):
        depdendency_matcher = dependencies.Dependencies()
        matched_charts = depdendency_matcher.match_charts(charts, src_files)
        return matched_charts

    @staticmethod
    def __generate_name__(chart_name):
        name = re.search(r'(.*)/(.*)', chart_name)

        if name is not None:
            name = name.group(2)
        else:
            name = chart_name

        return name + '-kreate'

    def install_helm_chart(self, chart_name, namespace, dry_run):
        name = self.__generate_name__(chart_name)
        self.helm_charts.install_helm_chart(
            name, chart_name, namespace, dry_run)

    def get_source_files(self, path):
        fileGetter = codefinder.CodeFinder(
            path, self.extensions, self.ignore_folders)
        files = fileGetter.get_code_files()
        return files

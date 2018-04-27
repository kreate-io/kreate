import yaml
import git
import tempfile
import shutil
import os
import subprocess


class Helm(object):

    def __init__(self, repo_name, repo_url, folders, logger):
        self.tempdir = tempfile.gettempdir()
        self.charts_path = os.path.join(self.tempdir, repo_name)
        self.repo_url = repo_url
        self.folders = folders
        self.logger = logger

    def __clone_charts_repo(self):
        self.logger.debug("Cloning charts repo...")
        if os.path.exists(self.charts_path):
            shutil.rmtree(self.charts_path)

        git.Git(self.tempdir).clone(self.repo_url)
        delete_folders = list(set(os.listdir(self.charts_path)).difference(
            self.folders))  # Delete unnecessary folders
        for folder in delete_folders:
            joined_path = os.path.join(self.charts_path, folder)
            isfolder = os.path.isdir(joined_path)
            if isfolder:
                shutil.rmtree(joined_path)

    def __scan_charts(self):
        self.yaml_files = [os.path.join(root, name)
                           for root, dirs, files in os.walk(self.charts_path)
                           for name in files
                           if name == "Chart.yaml"]

    def get_helm_charts_details(self):
        self.__clone_charts_repo()
        self.__scan_charts()
        yaml_objects = []
        for chart in self.yaml_files:
            self.logger.debug("Parsing " + chart)
            with open(chart) as chartfile:
                data = yaml.safe_load(chartfile)
                yaml_objects.append(data)
                for folder in self.folders:
                    prefix = folder + "/" 
                    if prefix in chart: # TODO: Change Can break
                        data["fullname"] = prefix + data["name"]
                    self.logger.debug("Added " + data["name"])
                chartfile.close()
        shutil.rmtree(self.charts_path)
        return yaml_objects

    def install_helm_chart(self, name, chart_name, namespace="default"):
        command = "helm upgrade " + name + \
            " --install --namespace " + namespace + " " + chart_name
        subprocess.run(command, shell=True, check=True)

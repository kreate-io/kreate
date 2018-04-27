# Kreate: Fast deployment of code dependencies

[![image](https://travis-ci.org/kreate-io/kreate.svg?branch=master)](https://travis-ci.org/kreate-io/kreate)

Kreate allows developers to focus on code and not ops by identifying and deploying third party dependencies such as Databases, Caches and other persistent stores into any Kubernetes cluster.

*Kreate is experimental

[![asciicast](https://asciinema.org/a/178016.png)](https://asciinema.org/a/178016)

## Installation

#### Prerequisites 
* Kubernetes Cluster.
* Install and setup [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* Install and setup [helm](https://docs.helm.sh/using_helm/)
* Add helm's stable and incubator repos
```
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com
$ helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
```

### Docker
```
docker run -it -v ${HOME}:/root kreateio/kreate
```

**if you want to pick up the kubeconfig from your user environment, you can use -v ${HOME}:/root to mount $HOME as /root.**

### Windows, OSX and Linux

1. Install [Python 3.6.5](https://www.python.org/downloads/release/python-365/)
2. ```pip install kreate```

## Usage
```
kreate [ command ] {parameters}
 ```

### Getting started
For usage and help content, pass in the -h parameter, for example:
```
$ kreate -h
$ kreate deploy -h
```

#### Deploy environment
```
$ kreate deploy --path "path_to_your_code_folder"
```
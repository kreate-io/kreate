import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import chart_model
import os
import model_scorer

class Dependencies:
    __chart_model__ = chart_model.ChartModel()
    __SCORE_THRESHOLD__ = 0.6

    def match_charts(self, src_paths):
        dep_lines = self.__extract_dependency_lines__(src_paths)

        dependencies = []
        for dep_line in dep_lines:
            dep_keywords = self.__dependency_to_keywords__(dep_line)
            dep_keyword_scores = self.__chart_model__.score_keywords(dep_keywords)

            dependencies.append({
                'line': dep_line,
                'keyword_scores': dep_keyword_scores
            })
                
        charts = []
        for dep in dependencies:
            top_keywords = self.__filter_keywords__(dep)
            chart = self.__get_chart__(top_keywords)

            charts.append({
                'dependency_line': dep['line'],
                'chart': chart
            })

        return charts

    def __extract_dependency_lines__(self, src_paths):
        scorer = model_scorer.Scorer()
        dep_lines = []

        for src_path in src_paths:
            src_lines = []
            if os.path.isfile(src_path):        
                with open(src_path, 'r') as f:
                    #src_lines = list(f) 
                    src_lines = f.read().splitlines()
                    dep_lines = dep_lines + scorer.predict_dependencies(src_lines)

        return dep_lines
    
    def __dependency_to_keywords__(self, dep_line):
        dep_line = dep_line.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(dep_line)

        keywords = []
        for token in tokens:
            #remove stop words
            if(not token in nltk.corpus.stopwords.words('english') and not token in keywords):
                keywords.append(token)
    
        return keywords

    def __filter_keywords__(self, dependency):
        filtered_keywords = []

        for kw in dependency['keyword_scores']:
            if(kw['score'] >= self.__SCORE_THRESHOLD__):
                filtered_keywords.append(kw)
        
        #sort by score decending (in place)
        filtered_keywords.sort(key=lambda kw: kw['score'], reverse=True)
        return filtered_keywords

    
    def __get_chart__(self, keywords):
        #todo: replace with a call to Tomer's code
        for kw in keywords:
            if 'pg' == kw['keyword']:
                return 'https://github.com/kubernetes/charts/blob/master/stable/postgresql/Chart.yaml'
            if 'mongodb' == kw['keyword']:
                return 'https://github.com/kubernetes/charts/blob/master/stable/mongodb/Chart.yaml'
            if 'mysql' == kw['keyword']:
                return 'https://github.com/kubernetes/charts/tree/master/stable/mysql/Chart.yaml'



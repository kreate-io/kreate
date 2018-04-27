import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import jellyfish
import re
from kreate import chart_model
import os
from kreate import model_scorer

class Dependencies:
    __chart_model__ = chart_model.ChartModel()
    __SCORE_THRESHOLD = 0.6
    __JARO_WINKLER_THRESHOLD = 0.7
    __TOP_CHART_MATCHES = 3

    def match_charts(self, charts, src_paths):
        dep_lines = self.__extract_dependency_lines__(src_paths)

        dependencies = []
        for dep_line in dep_lines:
            dep_keywords = self.__dependency_to_keywords__(dep_line)
            
            dependencies.append({
                'line': dep_line,
                'keywords': dep_keywords
            })
        
        matched_charts = []
        for dep in dependencies:
            matches = self.__match_charts__(self.__TOP_CHART_MATCHES, charts, dep['keywords'])
            matched_charts.append(matches)

        return matched_charts

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

    def __match_charts__(self, top_count, charts, features):
        matches = []

        for chart in charts:
            closest_distance = 0

            keywords = []
            keywords.append(chart['name'])

            if 'keywords' in chart:
                keywords = keywords + chart['keywords']

            for feature in features:
                for keyword in keywords:
                    distance = jellyfish.jaro_winkler(feature, keyword)

                    if distance > self.__JARO_WINKLER_THRESHOLD and distance > closest_distance:
                        closest_distance = distance

            if closest_distance > 0:
                matches.append({
                    'name': chart['name'],
                    'score': closest_distance
                })
        
        if matches:
            matches.sort(key=lambda x: x['score'], reverse=True)

        return matches

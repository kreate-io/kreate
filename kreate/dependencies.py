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
            matches = self.__match_charts__(
                self.__TOP_CHART_MATCHES, charts, dep['keywords'])
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
                    dep_lines = dep_lines + \
                        scorer.predict_dependencies(src_lines)

        return dep_lines

    def __dependency_to_keywords__(self, dep_line):
        dep_line = dep_line.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(dep_line)

        keywords = []
        for token in tokens:
            # remove stop words
            if(not token in nltk.corpus.stopwords.words('english') and not token in keywords):
                keywords.append(token)

        return keywords

    def __match_charts__(self, top_count, charts, features):
        # TODO: implement top_count
        matches = []

        for chart in charts:
            keywords = []
            keywords.append(chart['name'])

            if 'keywords' in chart:
                keywords = keywords + chart['keywords']

            total_score = 0
            jaro_count = 0

            for feature in features:
                for keyword in keywords:
                    distance = jellyfish.jaro_winkler(feature, keyword)

                    if distance > self.__JARO_WINKLER_THRESHOLD:
                        total_score = total_score + distance
                        jaro_count = jaro_count + 1

            score = 0

            if jaro_count > 0:
                score = total_score / jaro_count

            matches.append({
                'name': chart['name'],
                'fullname': chart['fullname'],
                'score': score
            })

        if matches:
            matches.sort(key=lambda x: x['score'], reverse=True)

        return matches

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import jellyfish
import re
from kreate import chart_model
import os
from kreate import model_scorer
from kreate import dependency_stopwords


class Dependencies:
    __chart_model__ = chart_model.ChartModel()
    __JARO_WINKLER_THRESHOLD = 0.8
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
            extended_stopwords = stopwords.words('english')
            extended_stopwords = extended_stopwords + dependency_stopwords.get()

            if(not token in extended_stopwords): #and not token in keywords):
                keywords.append(token)

        return keywords

    def __match_charts__(self, top_count, charts, features):
        # TODO: implement top_count
        matches = []
        known_terms = self.__get_known_terms()

        for chart in charts:
            keywords = []
            keywords.append(chart['name'])

            if 'keywords' in chart:
                keywords = keywords + chart['keywords']

            keywords = self.__f7(keywords)
            total_score = 0
            jaro_count = 0

            for feature in features:
                if feature in known_terms.keys():
                    feature = known_terms[feature]

                for idx, keyword in enumerate(keywords):
                    distance = jellyfish.jaro_winkler(feature, keyword)

                    if distance > self.__JARO_WINKLER_THRESHOLD:
                        if idx == 0:
                            distance = distance * 2
                        
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
        
        filtered = [x for x in matches if x['score'] >= self.__calculate_final_threshold(x['score'])]

        if filtered:
            filtered.sort(key=lambda x: x['score'], reverse=True)

        return filtered[0:top_count]

    def __calculate_final_threshold(self,score):
        if score <= 1.0:
            return self.__JARO_WINKLER_THRESHOLD
        else:
            return 1


    
    def __f7(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def __get_known_terms(self):
        # TODO: externalize
        return {'pg': 'postgres'}

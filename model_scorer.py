from sklearn.externals import joblib
import jellyfish
import numpy as np

class Scorer():
    DEPENDENCY_MODEL_PATH = './models/dependency_model.pkl'
    JARO_WINKLER_THRESHOLD = 0.7
    STOP_THRESHOLD = 0.9

    def __init__(self):
        self.__load_dependency_model()

    def __load_dependency_model(self):
        self.dependency_model= joblib.load(self.DEPENDENCY_MODEL_PATH)

    def predict_charts(self, charts, features):
        chart_scores = dict()

        for chart in charts:
            closest_distance = 0

            keywords = []
            keywords.append(chart['name'])

            if 'keywords' in chart:
                keywords = keywords + chart['keywords']

            for feature in features:
                for keyword in keywords:
                    distance = jellyfish.jaro_winkler(feature, keyword)

                    if distance > self.JARO_WINKLER_THRESHOLD and distance > closest_distance:
                        closest_distance = distance

            if closest_distance > 0:
                chart_scores[chart['name']] = closest_distance

            if closest_distance >= self.STOP_THRESHOLD:
                break 
        
        return chart_scores


    def predict_dependencies(self, code_lines):
        preds = self.dependency_model.predict(code_lines)

        filtered_deps = []

        for idx, pred in enumerate(preds):
            if pred == 1:
                filtered_deps.append(code_lines[idx])

        return filtered_deps
        
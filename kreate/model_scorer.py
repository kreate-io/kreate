def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
    
from sklearn.externals import joblib
import os
import tempfile
import numpy as np

class Scorer():
    DEPENDENCY_MODEL_PATH = os.path.join(tempfile.gettempdir(), 'dependency_model.pkl')

    def __init__(self):
        self.__load_dependency_model()


    def __load_dependency_model(self):
        self.dependency_model= joblib.load(self.DEPENDENCY_MODEL_PATH)


    def remove_high_frequency_terms(self, line):
        pass


    def predict_dependencies(self, code_lines):
        preds = self.dependency_model.predict(code_lines)

        filtered_deps = []

        for idx, pred in enumerate(preds):
            if pred == 1:
                filtered_deps.append(code_lines[idx])

        return filtered_deps
        
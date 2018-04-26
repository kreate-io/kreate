import pandas as pd
import numpy as np
import os
import git
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

training_repos = ['https://github.com/pytorch/pytorch.git', 'https://github.com/kelproject/pykube.git', 
                 'https://github.com/mongo-express/mongo-express.git']

def load_training_data(dir_path, extension, identifier):
    files = []

    X = []
    y = []

    for root, directories, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(root,filename))

            for file in files:
                with open(file, 'rU') as f:
                    for line in f:
                        X.append(line)

                        if identifier in line:
                            y.append(1)
                        else:
                            y.append(0)
                        
    return [X, y]

def unite_training_data(training_sets):
    X_final = []
    y_final = []
    
    for training_set in training_sets:
        X_final = X_final + training_set[0]
        y_final = y_final + training_set[1]
        
    return [X_final, y_final]

def download_training_data(target_path, git_repo_url):
    if not os.path.isdir(target_path):
        os.makedirs(target_path)

    try:
        git.Git(target_path).clone(git_repo_url)
    except git.GitCommandError:
        return



for repo in training_repos:
    download_training_data('./data', repo)

javascript_data = load_training_data('./data/mongo-express', '.js', 'require(')
python_data = load_training_data('./data/pykube', '.py', 'import')
python_data2 = load_training_data('./data/pytorch', '.py', 'import')

test_set = unite_training_data([javascript_data, python_data, python_data2])

pipeline = Pipeline([
    ('vect', TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, sublinear_tf=True)),
    ('tfidf', TfidfTransformer(use_idf=True)),
    ('clf', SGDClassifier()),
])

X_train, X_test, y_train, y_test = train_test_split(test_set[0], test_set[1], test_size=0.3)

grid_search = GridSearchCV(pipeline, {}, n_jobs=-1)
grid_search.fit(X_train, y_train)

print("Best score: %0.3f" % grid_search.best_score_)

pred = grid_search.best_estimator_.predict(X_test)
print("Test accuracy: {0}".format(accuracy_score(y_test, pred)))
print("Validation set predicted dependency:", np.where(pred == 1)[0].size)

best_estimator = grid_search.best_estimator_
joblib.dump(best_estimator, 'dependency_model.pkl')

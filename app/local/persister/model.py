class Model:
    def __init__(self, clf, feature_names, outcome_names):
        self.clf = clf
        self.feature_names = feature_names
        self.outcome_names = outcome_names

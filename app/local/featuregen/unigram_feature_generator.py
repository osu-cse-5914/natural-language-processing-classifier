from app.local.featuregen.language_classifier_feature_generator import LanguageClassifierFeatureGenerator


class UnigramFeatureGenerator(LanguageClassifierFeatureGenerator):
    def __init__(self):
        pass

    def generate_features(self, passage: str):
        result = {}
        for unigram in passage.split():
            result[unigram] = result.get(unigram, 0.0) + 1.0
        return result

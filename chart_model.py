class ChartModel:

    def score_keywords(self, dep_keywords):
        
        #mock (@todo: update after integrating training a model)
        keyword_scores = []
        for kw in dep_keywords:
            keyword_scores.append({
                'keyword': kw,
                'score': 0.7
            })
        
        return keyword_scores
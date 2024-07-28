class F1ScoringMap():
    # Class for quick look up of points awarded in the top 10 of race.
    # Values with a half shift are used for tiebreakers of various predictions.
    
    #Omg a singleton
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(F1ScoringMap, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    def __init__(self) -> None:
        
        self.pos_to_score = {
            1: 25,
            2: 18,
            3: 15,
            4: 12,
            5: 10,
            6: 8, 
            7: 6,
            8: 4,
            9: 2,
            10: 1
        }

        for pos in range(11, 25):
            self.pos_to_score[pos] = 0

        for pos in range(1, 21):
            self.pos_to_score[pos - 0.5] = self.pos_to_score[pos]

        del self.pos_to_score[0.5]

    def map(self, pos):
        return self.pos_to_score[pos]
    
if __name__ == "__main__":

    scoring_map = F1ScoringMap()

    print(scoring_map.pos_to_score)

    print(scoring_map.map(10))
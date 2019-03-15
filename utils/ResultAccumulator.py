class ResultAccumulator:
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.counter = {key: 0 for key in thresholds}

    def add(self, label):
        self.counter[label] += 1
        return self.counter[label] >= self.thresholds[label]

    def clear_all(self):
        self.counter = {key: 0 for key in self.thresholds}

class Variables():
    def __init__(self):
        self.question = ""
        self.option_a = ""
        self.option_b = ""
        self.option_c = ""
        self.option_d = ""
        self.option_e = ""

    def setQuestion(self, questionArray):
        self.question = questionArray[0]
        self.option_a = questionArray[1]
        self.option_b = questionArray[2]
        self.option_c = questionArray[3]
        self.option_d = questionArray[4]
        self.option_e = questionArray[5]

    def getQuestion(self):
        return self.question, self.option_a, self.option_b, self.option_c, self.option_d, self.option_e

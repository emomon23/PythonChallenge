class LPLogger:
    def __init__(self, count = 0):
        self.newLines(count)

    def log(self, msg, newLineCount = 0):
        newLineMsg = '';

        # I'm sure there's a more clever way to do this, will refactor if...I get to it??
        if newLineCount > 0:
            r = range(newLineCount)
            for l in r:
               newLineMsg += "\n"

        print("{nlm}** LeadPages Log: {msg}".format(msg=msg, nlm=newLineMsg))
        return self

    def logError(self, err):
        if err == None:
            print("**** LeadPages ERROR: Logger.LogError - err = None");

        print(f"**** LeadPages ERROR: Unexpected {err=}, {type(err)=}")
        return self

    def newLines(self, count):
        if isinstance(count, int) & count > 0:
            x = range(count)
            for n in x:
                print(' ')

        return self

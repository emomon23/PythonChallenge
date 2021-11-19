class Logger:
    def Log(msg):
        print(msg);

    def LogError(err):
        if err == None:
            print("Logger.LogError - err = None");

        print(f"Unexpected {err=}, {type(err)=}")
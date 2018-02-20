from server import handler,run

@handler("index")
def printL(req):
    return 200,{},"hello world"

run()
from server import handler,run

@handler("index")
def printL(req):
    with open('WebPage1.html', 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return 200,{"Content-type":"text/html"},data #return_code,headers,code of the page(here it is html)

@handler("index","POST")
def answerpost(req,):
    with open('WebPage1.html', 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return 200,{"Content-type":"text/html"},data #return_code,headers,code of the page(here it is html)

run()
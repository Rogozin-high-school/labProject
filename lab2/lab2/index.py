from server import handler,run

@handler("index")
def printL(req):
    with open('index.html', 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return 200,{"Content-type":"text/html"},data #return_code,headers,code of the page(here it is html)

run()
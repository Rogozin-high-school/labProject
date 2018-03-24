from server import handler,run,post
from server import RequestHandler
import Math_module as mm
@handler("index")
def printL(req):
    mm.main()
    data=""
    if "?" in req.path:
        getdict=req.parse_get()
        if getdict["answer"] == "fail":
            data = "<script>alert('This is not the correct password')</script>"
        else:
            data = "<script>alert('changing the parameters of the get request wont do something')</script>"
    with open('index.html', 'r') as myfile:
        data+=myfile.read().replace('\n', '')
    return 200,{"Content-type": "text/html"},data

@handler("control","POST")
def answerpost(req):
    data=str(post(req),"utf-8")
    password = data.split("&")[0].split("=")[1]
    if(password== "Skyro"):
        with open('control_panel.html', 'r') as myfile:
            data=myfile.read().replace('\n', '')
            data=str(data)
            data=data[9:]
        print(data[0])
        return 200,{"Content-type": "text/html"},data
    else:
        return 302,{"Location": "/index?answer=fail"},data 

run()
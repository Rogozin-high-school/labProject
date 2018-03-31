from module.server.httpserver import handler, run

@handler("helloworld", "GET")
def a(req):
    return 200, {}, "Hello, World!"

t, h = run(('', 8080))
input()
h.shutdown()

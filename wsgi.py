import server
from paste.request import parse_formvars


def application(environ, start_response):
    path = environ["PATH_INFO"][1:] or "index"
    fields = parse_formvars(environ)
    if hasattr(server, path):
        try:
            body, ct = getattr(server, path)(**fields)
            code = "200 Success"
        except Exception as e:
            body, ct = "Error 500: " + type(e).__name__ + ": " + str(e), "text/plain"
            code = "500 Internal Server Error"
    else:
        body, ct = "Error 404: Page not found", "text/plain"
        code = "404 Page Not Found"

    response_headers = [("Content-type", ct), ("Content-length", str(len(body)))]
    start_response(code, response_headers)
    return [unicode(body).encode("utf8")]

if __name__ == "__main__":
    from paste import httpserver
    httpserver.serve(application, host="18.248.3.226", port="8080")

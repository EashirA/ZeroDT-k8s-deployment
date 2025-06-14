from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8080

class Handler(SimpleHTTPRequestHandler):
    pass

if __name__ == '__main__':
    print("Starting server at port", PORT)
    HTTPServer(("", PORT), Handler).serve_forever()
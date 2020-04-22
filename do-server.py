import http.server
import socketserver
import sys

PORT = sys.argv[1]

class SimpleHandler(http.server.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		print(self.wfile)
		self.wfile.write("<html><head><title>Title goes here.</title></head>".encode("utf-8"))
		self.wfile.write("<body><p>This is a test.</p>".encode("utf-8"))
		# If someone went to "http://something.somewhere.net/foo/bar/",
		# then s.path equals "/foo/bar/".
		self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path))
		self.wfile.write("</body></html>".encode("utf-8"))
		self.wfile.close()

try:
	server = http.server.HTTPServer(('localhost',PORT),SimpleHandler)
	print('Started http server')
	server.serve_forever()
except KeyboardInterrupt:
	print('^C received, shutting down server')
	server.socket.close()

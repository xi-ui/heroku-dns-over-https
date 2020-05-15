import http.server
import socketserver
import sys
PORT = int(sys.argv[1])

def handleDns(path):
	path = path.split("?",2)
	path[0] = ".".join(path[0].split("/")[::-1])
	path[1] = path[1].split("&",2)
	path[1][0] = path[1][0].split("=",2)
	path[1][1] = path[1][1].split("=",2)
	path[1][0][1] = path[1][0][1].upper()
	path[1][1][1] = path[1][1][1].upper()
	path[1][0][0] = path[1][0][0].lower()
	path[1][1][0] = path[1][1][0].lower()
	dnsq,dnsclass="SOA","IN"
	if path[1][0][0] == "c":
		dnsclass=path[1][0][1]
		if path[1][1][0] == "q":
			dnsq=path[1][1][1]
	elif path[1][1][0] == "c":
		dnsclass=path[1][1][1]
		if path[1][0][0] == "q":
			dnsq=path[1][0][1]
	return path[0]+"\t"+dnsclass+"\t"+dnsq

class SimpleHandler(http.server.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write(handleDns(self.path).encode("utf-8"))
		self.wfile.close()
	def do_POST(self):
		self.send_response(400)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write("400 Bad Request".encode("utf-8"))
		self.wfile.close()
try:
	server = http.server.HTTPServer(('0.0.0.0',PORT),SimpleHandler)
	print('Started http server')
	server.serve_forever()
except KeyboardInterrupt:
	print('^C received, shutting down server')
	server.socket.close()

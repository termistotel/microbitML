import socket
from ast import literal_eval


TCP_IP = '192.168.2.20'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print "Starting... "+TCP_IP+" "+str(TCP_PORT)

conn, addr = s.accept()
print 'Connection address:', addr

while True:
	try:
		data = literal_eval(conn.recv(BUFFER_SIZE))
		print "received data:", data
	except ValueError:
		print "krivo"
	conn.send("etoga")

conn.close()
s.close()

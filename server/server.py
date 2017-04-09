import socket

print "Starting..."

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


conn, addr = s.accept()
print 'Connection address:', addr

while True:
	data = conn.recv(BUFFER_SIZE)
	print "received data:", data
	conn.send("etoga")

conn.close()
s.close()

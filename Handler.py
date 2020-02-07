import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):

        self.recv_data = ""

        while True:
            try:
                self.recv_data = self.request.recv(1024).strip()
                print(self.recv_data)

            except NameError as e:
                pass

import sys
import socket
import shlex
import cmd
import multiprocessing
from time import sleep

class Application(cmd.Cmd):
    com = False
    prev_msg = ''

    def do_EOF(self, args):
        self.reader.terminate()
        self.socket.close()
        return True

    def responder(self, sockfd, pause):
        while True:
            while True:
                try:
                    data = sockfd.recv(1024, socket.MSG_DONTWAIT)
                    if data:
                        break
                except socket.error:
                    pass
            msg = data.strip().decode()
            if msg != self.previous_message or self.com:
                print(msg)
                self.prev_msg = msg
                com = False
                   
    def preloop(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
        self.port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
        self.socket.connect((self.host, self.port))
        self.pause = multiprocessing.Queue()
        self.reader = multiprocessing.Process(target=self.responder, args=[self.socket, self.pause])
        self.reader.start()
    
    def postcmd(self, stop, line):
        com = True

    def do_who(self, args):
        """usage: who\n\nLogged users list"""
        
        tokens = shlex.split(args)
        if not tokens:
            self.socket.sendall('who\n'.encode())
    
    def do_cows(self, args):
        """usage: cows\n\nAll cow-names available for registration"""
        
        tokens = shlex.split(args)
        if not tokens:
            self.socket.sendall('cows\n'.encode())
    
    def do_login(self, args):
        self.socket.sendall(f'login {args}'.encode())

    def do_say(self, args):
        self.socket.sendall(f'say {args}'.encode())

    def do_yield(self, args):
        self.socket.sendall(f'yield {args}'.encode())

if __name__ == '__main__':
    tmp = Appliaction()
    tmp.cmdloop()


exit()
host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
    sockfd.connect((host, port))
    while msg := sys.stdin.buffer.readline():
        sockfd.sendall(msg)
        print(sockfd.recv(1024).rstrip().decode())
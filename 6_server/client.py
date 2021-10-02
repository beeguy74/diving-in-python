import socket
import time

class ClientError(Exception):
    def __init__(self):
        self.message = "ClientError"

class Client:
    def __init__(self, ip: str, port: int, timeout: float = None) -> None:
        self._ip = ip
        self._port = port
        self._timeout = timeout
        self._connect()

    
    def _connect(self):
        try:
            self._sock = socket.create_connection((self._ip, self._port), timeout=self._timeout)
        except:
            raise ClientError


    def __del__(self):
        self._sock.close


    def get(self, message: str):
        response = dict()
        try:
            self._sock.sendall(str.encode('get ' + message + '\n'))
            data = self._sock.recv(1024)
            data = str.split(data.decode(), '\n')
        except:
            raise ClientError
        if data.pop(0) != "ok":
            raise ClientError
        try:
            for line in data:
                if line == '':
                    continue
                lst = str.split(line)
                response.setdefault(lst[0], []).append((int(lst[2]), float(lst[1])))
                response.get(lst[0]).sort(key= lambda x: x[0])
        except:
            raise ClientError
        return response


    def put(self, name: str, metric: float, timestamp: int = None):
        if timestamp is None:
            timestamp = int(time.time())
        try:
            message = 'put ' + name + ' ' + str(metric) + ' ' + str(timestamp) + '\n'
            self._sock.sendall(str.encode(message))
            data = self._sock.recv(1024)
            data = str.split(data.decode(), '\n')
        except:
            raise ClientError
        if data.pop(0) != "ok":
            raise ClientError
        if len(data) != 2:
            raise ClientError
        
cli = Client('127.0.0.1', 8888)
# for i in range(5):
#     cli.put("vasya", i + 0.1, 161 + i * 10)
# time.sleep(3.)
print("petya:")
print(cli.get("petya"))
time.sleep(1.)
print("vasya:")
print(cli.get("vasya"))
time.sleep(1.)
print("utsya:")
print(cli.get("utsya"))
cli = 0
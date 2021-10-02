import asyncio

class ClientServerProtocol(asyncio.Protocol):
    _stor = {}

    def _responseFromTuple(self, data: tuple):
        retStr = ''
        for item in data[1].items():
            retStr += data[0] + ' ' + item[1] + ' ' + item[0] + '\n'
        return retStr

    def _get(self, data):
        response = 'ok\n'
        if len(data) != 2:
            response = 'error\nwrong command\n'
        elif data[1] == '*':
            for item in self._stor.items():
                response += self._responseFromTuple(item)
        elif data[1] in self._stor.keys():
            response += self._responseFromTuple((data[1], self._stor.get(data[1])))
        response += '\n'
        return response

    def _put(self, data):
        if len(data) != 4 :
            response = 'error\nwrong command\n\n'
        elif not isinstance(data[1], str):
            response = 'error_str\nwrong command\n\n'
        elif not isinstance(float(data[2]), float):
            response = 'error_float\nwrong command\n\n'
        elif not isinstance(int(data[3]), int):
            response = 'error_int\nwrong command\n\n'
        else:
            self._stor.setdefault(data[1], {}).update({data[3]: data[2]})
            response = 'ok\n\n'
            print(self._stor)
        return response

    def _validation(self, data):
        if data == '\n' or len(str.split(data, '\n')) != 2:
            return None
        data = str.split(data)
        if data[0] != 'put' and data[0] != 'get':
            return None
        return data

    def connection_made(self, transport):
        print('Соединение установлено:', type(transport.get_extra_info('socket')))
        self.transport = transport

    def _process_data(self, decoded_data):
        print(f'Получен запрос: {ascii(decoded_data)}')
        data = self._validation(decoded_data) 
        if data is None:
            response = 'error\nwrong command\n\n'
        elif data[0] == 'put':
            response = self._put(data)
        else:
            response = self._get(data)
        print(f'Отправлен ответ {ascii(response)}')
        return response

    def data_received(self, data):
        resp = self._process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host: str, port: int):
    loop = asyncio.get_event_loop()
    print("loop")
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    print("coroutine")

    server = loop.run_until_complete(coro)
    print("run")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    print("close")
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
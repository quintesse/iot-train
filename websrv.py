# Sets up a webserver

from ws_connection import ClientClosedError
from ws_server import WebSocketClient
from ws_multiserver import WebSocketMultiServer
import motor

_server = None
_motor = None

    
class WSTrainClient(WebSocketClient):
    def __init__(self, conn):
        super().__init__(conn)
        print('Connection accepted.')

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            print("Incoming speed msg : " + msg)
            speed = int(msg)
            _motor.speedTo(speed)
        except ClientClosedError:
            self.connection.close()


class WSTrainServer(WebSocketMultiServer):
    def __init__(self):
        super().__init__("www/index.html", 2)

    def _make_client(self, conn):
        return WSTrainClient(conn)
    
def start(imotor):
    assert isinstance(imotor, motor.IMotor), "argument should be of type motor.IMotor"
    global _server, _motor
    _motor = imotor
    _server = WSTrainServer()
    _server.start()
    try:
        while True:
            _server.process_all()
    except KeyboardInterrupt:
        pass
    _server.stop()

    
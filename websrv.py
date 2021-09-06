# Sets up a webserver

from MicroWebSrv2 import *
import motor

_wsMod = None
_mws2 = None
_motor = None

@WebRoute(GET, '/speed/<speed>')
def SetSpeed(microWebSrv2, request, args):
    speed = args["speed"]
    if isinstance(speed, int) and speed >= -100 and speed <= 100:
        _motor.speedTo(speed)
        request.Response.ReturnOk("OK")
    else:
        request.Response.ReturnBadRequest()
    
@WebRoute(POST, '/speed')
def SetSpeed(microWebSrv2, request):
    data = request.GetPostedURLEncodedForm()
    try:
        speed = int(data["speed"])
        if speed >= -100 and speed <= 100:
            _motor.speedTo(speed)
            request.Response.ReturnOk("OK")
        else:
            request.Response.ReturnBadRequest()
    except:
        request.Response.ReturnBadRequest()
    
def _onWSSetSpeed(webSocket, msg):
    print("Incoming speed msg : " + msg)
    speed = int(msg)
    _motor.speedTo(speed)

def _onWSAccepted(microWebSrv2, webSocket):
    print("Incoming WebSocket connection:")
    print('   - User   : %s:%s' % webSocket.Request.UserAddress)
    print('   - Path   : %s'    % webSocket.Request.Path)
    print('   - Origin : %s'    % webSocket.Request.Origin)
    if webSocket.Request.Path.lower() == '/wsspeed' :
        print('Connection accepted.')
        webSocket.OnTextMessage = _onWSSetSpeed
    else :
        print('Connection rejected.')
        webSocket.Close()
        
def start(imotor):
    assert isinstance(imotor, motor.IMotor), "argument should be of type motor.IMotor"
    global _wsMod, _mws2, _motor
    _motor = imotor
    _wsMod = MicroWebSrv2.LoadModule('WebSockets')
    _wsMod.OnWebSocketAccepted = _onWSAccepted
    _mws2 = MicroWebSrv2()
    _mws2.SetEmbeddedConfig()
    _mws2.NotFoundURL = '/'
    _mws2.StartManaged()
    
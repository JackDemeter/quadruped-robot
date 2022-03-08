import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def create_socket_connection(start_port=5000):

    host=get_ip() # this computer's IP
    port = start_port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while port < min(start_port+1000,9999):
        try:
            s.bind((host,port))
            break
        except OSError as e:
            port+=1
    print(f"Connection Info - ip: {host}, port: {port}")
    return s
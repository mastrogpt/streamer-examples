import socket
import time
import json

def stream(args):
    inp = args.get("input")
    stream_host = args.get("STREAM_HOST",None)
    stream_port = args.get("STREAM_PORT", None)
    print(f"Receving stream action for host:port {stream_host}:{stream_port}")
    if stream_host and stream_port:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"Connecting to {stream_host}:{stream_port}")
                s.connect((stream_host, int(stream_port)))
                print(f"Streaming to {stream_host}:{stream_port}")
                for c in inp:
                    print("Sending char %c ASCII %d\n" % (c, ord(c)))
                    msg = {"output": "Char '%c' ASCII %d\n" %(c, ord(c))} 
                    s.sendall(json.dumps(msg).encode('utf-8'))
                    time.sleep(2)
                s.sendall(b"{}")
        except :
            pass
                
    return {"output": "Returning ASCII char for the input.", "streaming": True}

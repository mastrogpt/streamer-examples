#--kind python:default
#--web true
#--timeout 300000
import stream
import threading


def main(args):

    t = threading.Thread(target=stream.stream, args=(args,))
    t.start()

    return {"statusCode": 200, "body": "Accepted"}

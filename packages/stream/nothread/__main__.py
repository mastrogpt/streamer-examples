#--kind python:default
#--web true
#--timeout 300000
import stream

def main(args):
  return { "body": stream.stream(args) }  

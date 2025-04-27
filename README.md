# Apache OpenServerless Streamer Examples

## What is this
Sample repository on how to use Apache OpenServerless Streamer.
The purpose is to show how stream from an OpenServerless action, avoiding the
timeouts.

## Small introduction
[Apache OpenServerless Streamer](https://github.com/openserverless-streamer) 
is a unique solution: it can invoke an OpenServerless action or web action,
returning a stream to the client.

## How to use examples
Make a login on your OpenServerless account:

```bash
ops ide login <username> <host>
```

Then deploy as usual:

```bash
ops ide deploy
```

Three action are deployed:

| Action             | Web   | Details                       |
|--------------------|-------|-------------------------------|
| `hello/call`         | True  | This action will return 202 and call the hello/stream behind the scenes     |
| `hello/stream`       | False | Called by the `hello/call` action     |
| `hello/thread`       | True  | This action will start the stream in a separate thread   |

## Examples

### Action hello/call
This web action will call the `hello/stream`. We need to authenticate sending
our wsk authorization token: this because hello/call needs to invoke a protected
resource.

To test this action and see the streamed response, you can use this cURL:

```bash
curl -N -X POST "<streamer_url>/web/<user_namespace>/stream/call" \
  -H "Authorization: <auth_token>" \
  -H "Content-Type: application/json" \
  -d '{"input":"0123456789A0123456789B0123456789C0123456789D"}'
```

**Note**: you can retrieve auth_token from your `~/.wskprops` file

Behind the scenes, the web action `hello/call` is called by the streamer, 
passing to it informations about the stream socket. The `hello/call` will then call the action `hello/stream` in non-blocking mode and returning http status 
202 to the streamer.

### Action hello/thread
This webaction is instead using a different technique. When called by the 
streamer, this action will create a thread to handle the socket and continue
the stream. After creating the thread, the action is returning immediately
sending a 202 http status.

To test this action and see the streamed response, you can use this cURL:

```bash
curl -N -X POST "<streamer_url>/web/<user_namespace>/stream/thread" \
  -H "Content-Type: application/json" \
  -d '{"input":"0123456789A0123456789B0123456789C0123456789D"}'
```

## Final notes
Both action stream/thread and stream/stream actions need an higher timeout.
OpenWhisk actions will last, by default, 60 seconds.
To increase this timeout, we used this annotation: `#--timeout 300000`

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from webexteamssdk import WebexTeamsAPI
import sys
import os


# https://stackoverflow.com/questions/18444395/basehttprequesthandler-with-custom-instance
class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    api = None

    def __init__(self, api, *args):
        self.api = api
        BaseHTTPRequestHandler.__init__(self, *args)

    # Remember, bots can only see messages in which they're specifically mentioned.
    # See Differences Between Bots & People in the Bots guide for more details.
    # source: https://developer.webex.com/docs/api/guides/webhooks
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        # receives a webhook message:
        # See more at:
        # https://webexteamssdk.readthedocs.io/en/latest/user/api.html#webexteamssdk.Webhook
        receivedMessage = json.loads(body.decode("utf-8"))

        # retrieves the message sent to the room
        realMessage = self.api.messages.get(
            messageId=receivedMessage["data"]["id"])
        roomId = realMessage.roomId

        # sends a new message to the room
        self.api.messages.create(roomId=roomId, text="hello there")
        return


class http_server:
    def __init__(self, api):
        def handler(*args):
            HTTPServer_RequestHandler(api, *args)
        print("Running server")
        server = HTTPServer(('0.0.0.0', 9999), handler)
        server.serve_forever()


class main:
    def __init__(self):
        access_token = os.environ.get("ACCESS_TOKEN")
        if not access_token:
            print("Please provide your Access Token to be able to execute this code.")
            sys.exit(2)
        self.api = WebexTeamsAPI(access_token=access_token)

        self.server = http_server(self.api)


if __name__ == "__main__":
    m = main()

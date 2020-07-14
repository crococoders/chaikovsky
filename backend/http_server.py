import json
import jsonpickle
from http.server import BaseHTTPRequestHandler, HTTPServer

from yandex_music.client import Client
import logging
logging.basicConfig(level=logging.CRITICAL)


class S(BaseHTTPRequestHandler):
    token = ""

    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        # token = "AgAAAAAcPiuVAAG8XhlKrZWp1E1SrUv2dHA-q5Y"
        client = Client.from_token(token)
        if self.path == '/liked_tracks/':
            print("token", token)
            liked_tracks = client.users_likes_tracks().tracks
            print("signed up as ", client.me['account']['full_name'])
            response = {'result': []}
            for track in liked_tracks:
                response['result'].append(track)
            json_dump = jsonpickle.encode(response)
            self._set_response(200)
            self.wfile.write(json_dump.encode("utf-8"))
        elif self.path == '/play/':
            title = client.users_likes_tracks().tracks[0].track.title
            print(client.users_likes_tracks().tracks[0].track.file_size)
            client.users_likes_tracks().tracks[0].track.download(title)
            self._set_response(200)
            # print(track)
        else:
            self._set_response(404)
            self.wfile.write("Not found".encode('utf-8'))

    def do_POST(self):
        if self.path == '/auth/':
            global token
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")  # <--- Reads data from body
            data = json.loads(post_data)  # <--- Converts string to json
            print("data", data)
            client1 = Client()
            try:
                token = client1.generate_token_by_username_and_password(username=data['login'], password=data['password'])
                self._set_response(200)
                self.wfile.write("OK".encode('utf-8'))
            except:
                self._set_response(403)
                self.wfile.write("invalid password or login".encode("utf-8"))
        else:
            self._set_response(404)
            self.wfile.write("Error".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting server at 8080")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

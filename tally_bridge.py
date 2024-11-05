#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests
import logging
import argparse


logging.basicConfig(level=logging.INFO)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/cgi-bin/aw_ptz':
            query = urllib.parse.parse_qs(parsed_path.query)
            cmd = query.get('cmd', [''])[0]
            res = query.get('res', [''])[0]
            logging.info(f"Richiesta ricevuta: cmd={cmd}, res={res}")
            if cmd == '#DA1' and res == '1':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'dA1')
                try:
                    response = requests.get(f'http://{self.server.target_ip}/-wvhttp-01-/control.cgi?f.tally:=on&f.tally.mode:=program')
                    response.raise_for_status()
                    logging.info("Tally on")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Errore nella richiesta tally on: {e}")
            elif cmd == '#DA0' and res == '1':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'dA0')
                try:
                    response = requests.get(f'http://{self.server.target_ip}/-wvhttp-01-/control.cgi?f.tally:=off')
                    response.raise_for_status()
                    logging.info("Tally off")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Errore nella richiesta tally off: {e}")
            else:
                self.send_error(400, 'richiesta invalida')
        else:
            self.send_error(404, 'indirizzo non trovato')

def run():
    parser = argparse.ArgumentParser(description='HTTP Server per Tally-Bridge')
    parser.add_argument('--port', type=int, default=8080, help='Porta del canale del tricaster (Standard: 8080)')
    parser.add_argument('--target-ip', required=True, help='Indirizzo IP della camera')
    args = parser.parse_args()

    server_address = ('', args.port)
    handler_class = MyHandler
    httpd = HTTPServer(server_address, handler_class)
    httpd.target_ip = args.target_ip 
    logging.info(f'Server sulla porta {args.port} ed invia la richiesta alla camera {args.target_ip}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
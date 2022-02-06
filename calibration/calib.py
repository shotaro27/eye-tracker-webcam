# -*- coding: utf-8 -*-
"""
@author: shotaro27
"""

from http.server import CGIHTTPRequestHandler, HTTPServer

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/calib_result"]

# ポート番号
PORT = 8080

# IPアドレス
HOST = "127.0.0.1"

# URLを表示
print("http://127.0.0.1:8080/")

# サーバの起動
with HTTPServer((HOST, PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

print("http://127.0.0.1:8080/")
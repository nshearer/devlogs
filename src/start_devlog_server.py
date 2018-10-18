import os

from devhttp import DevelopmentHttpServer


def test_index(request, server, assets):
    return "<html><body><h1>Success!</h1></body></html>"


if __name__ == '__main__':

    server = DevelopmentHttpServer()

    project = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assets = os.path.join(project, 'assets')

    server.add_static('md5.js', os.path.join(assets, 'md5.js'))
    server.add_dynamic('index.html', test_index, '.html')

    server.serve_forever('127.0.0.1', 8080)
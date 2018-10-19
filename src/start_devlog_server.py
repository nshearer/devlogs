import os

from devhttp import DevelopmentHttpServer


def test_index(request, server, assets):
    return "<html><body><h1>Success!</h1></body></html>"


if __name__ == '__main__':

    server = DevelopmentHttpServer()

    project = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assets = os.path.join(project, 'assets')

    server.add_multiple_static(
        '/',
        os.path.join(project, 'lib', 'startbootstrap-sb-admin'),
        lambda p: os.path.basename(p) not in ('LICENSE', 'gulpfile.js'))

    server.serve_forever('127.0.0.1', 8080)
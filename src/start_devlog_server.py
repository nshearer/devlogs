import os

from devhttp import DevelopmentHttpServer
from devhttp import render_jinja


def index_view(request, server, assets):
    return render_jinja(assets, 'index.j2.html')


if __name__ == '__main__':

    server = DevelopmentHttpServer()

    project = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assets = os.path.join(project, 'assets')

    for bootstrap_dir in ('css', 'js', 'vendor'):
        server.add_multiple_static(
            bootstrap_dir,
            os.path.join(project, 'lib', 'startbootstrap-sb-admin', bootstrap_dir))

    server.add_static('favicon.ico', os.path.join(assets, 'favicon.ico'))

    server.add_asset('base.j2.html', os.path.join(assets, 'base.j2.html'))
    server.add_asset('index.j2.html', os.path.join(assets, 'index.j2.html'))
    server.add_dynamic('index.html', index_view)

    server.redirect('', 'index.html')

    print("Serving http://127.0.0.1:8080")
    server.serve_forever('127.0.0.1', 8080)
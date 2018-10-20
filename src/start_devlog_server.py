import os

from devlogs import DevLogHttpServer



if __name__ == '__main__':

    server = DevLogHttpServer(project_folder=os.path.join(os.path.dirname(__file__), '..'))
    print("Serving http://127.0.0.1:8080")
    server.serve_forever('127.0.0.1', 8080)
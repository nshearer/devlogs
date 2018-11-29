import os
import sys

from devlogs import DevlogHttpServer, NullDevlogConfig

if __name__ == '__main__':

    # Paths
    module_path = 'devlogs\DevlogHttpAssets.py'
    project_path = os.path.abspath(os.path.dirname(__file__))
    module_path = os.path.join(project_path, module_path)

    print("PROJECT: " + project_path)

    # Create server
    server = DevlogHttpServer(config=NullDevlogConfig(), project_folder=project_path)

    # Save assets
    print("")
    print("Writing " + module_path)
    server.save_assets_module(module_path)


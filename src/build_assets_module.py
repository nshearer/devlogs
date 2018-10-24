import os
import sys

from libdevlog import DevlogHttpServer, NullDevlogConfig

if __name__ == '__main__':

    # Parse args
    try:
        module_path,  = sys.argv[1:]
    except ValueError:
        print("USAGE: %s module_path" % (os.path.basename(sys.argv[0])))
        sys.exit(1)

    # Paths
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    module_path = os.path.join(project_path, module_path)

    print("PROJECT: " + project_path)

    # Create server
    server = DevlogHttpServer(config=NullDevlogConfig(), project_folder=project_path)

    # Save assets
    print("")
    print("Writing " + module_path)
    server.save_assets_module(module_path)


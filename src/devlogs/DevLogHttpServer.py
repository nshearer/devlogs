import os

from devhttp import DevelopmentHttpServer

from . import views

class DevLogHttpServer(DevelopmentHttpServer):
    '''
    Web app server for showing monitored log content
    '''

    def __init__(self, project_folder=None):
        '''

        :param project_folder:
            Path to project folder for locating assets

            If project_folder is specified, then find and load assets from project
            folder files.
            If not speicified, then will load assets saved to module devlogs.assets
        '''

        super().__init__()

        # Load assets (statics and templates)
        if project_folder is None:
            from . import assets
            self.load_assets_module(assets.DEV_HTTP_ASSETS)
        else:
            self._add_file_assets(project_folder)

        self._configure()


    def _configure(self):

        # Dynamic views
        self.add_dynamic('index.html', views.index_view)

        # Redirects
        self.redirect('', 'index.html')


    def _add_file_assets(self, project_folder):
        '''
        Add all of the assets this server needs from disk

        :param project_folder:
            Path to the project folder for locating assets
        '''
        assets = os.path.join(project_folder, 'assets')
    
        for bootstrap_dir in ('css', 'js', 'vendor'):
            self.add_multiple_static(
                bootstrap_dir,
                os.path.join(project_folder, 'lib', 'startbootstrap-sb-admin', bootstrap_dir))
    
        self.add_static('favicon.ico', os.path.join(assets, 'favicon.ico'))
    
        self.add_asset('base.j2.html', os.path.join(assets, 'base.j2.html'))
        self.add_asset('index.j2.html', os.path.join(assets, 'index.j2.html'))

    def _register_dynamics(self):
        '''Register all the dynamic endpoints'''




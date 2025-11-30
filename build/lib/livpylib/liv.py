import subprocess
import sys
from importlib import import_module
import inspect

# __all__ = []

def get_options():
    print(
        """
        Options for library imports:
        - plot
        - stats
        - images
        - formatting
        - geo
        - all
        - default
        """
    )

class package():
    def __init__(self, name, func=None, alias=None, install_name=None):
        self.name = name
        self.func = func
        self.alias = alias

        if install_name:
            self.install_name = install_name
        else:
            self.install_name = self.name

    def i_s(self):
        if self.func and self.alias:
            return f'from {self.name} import {self.func} as {self.alias}'
        elif self.func and not self.alias:
            return f'from {self.name} import {self.func}'
        elif self.alias and not self.func:
            return f'import {self.name} as {self.alias}'
        else:
            return f'import {self.name}'

class lib_list():
    def __init__(self, types=None):
        self.global_enviro = inspect.currentframe().f_back.f_back.f_globals
        self.libs = [
            package('pandas',alias='pd'),
            package('math'),
            package('numpy', alias='np'),
            package('time'),
            package('datetime'),
            package('glob', 'glob', 'glob'),
            package('os'),
            package('sys')
        ]

        if types:
            if isinstance(types, str):
                self.handle(types)
            if isinstance(types, list):
                for each in types:
                    self.handle(each)
        
        for p in self.libs:
            self._install_lib(p)

    def handle(self, types):
        match types:
            case 'plot':
                self._add_plot_libs()
            case 'stats':
                self._add_stats_libs()
            case 'images':
                self._add_images_libs()
            case 'formatting':
                self._add_formatting_libs()
            case 'geo':
                self._add_geo_libs()
            case 'all':
                self._add_all_libs()
            case 'default':
                pass
            case _:
                print(f'Could not find a type or none given.\n Loading default libs. Looking for more options?\n\n')
                get_options()
                return

    # These just need to add to the self.libs list
    def _add_plot_libs(self):
        self.libs.append(package('matplotlib.pyplot',alias='plt', install_name='matplotlib'))
        self.libs.append(package('seaborn',alias='sns'))
        self.libs.append(package('matplotlib.patches',alias='patches', install_name='matplotlib'))
        self.libs.append(package('matplotlib.colors',alias='mcolors', install_name='matplotlib'))
        self.libs.append(package('matplotlib.ticker',alias='mtick', install_name='matplotlib'))
    def _add_stats_libs(self):
        self.libs.append(package('scipy',func='stats'))
        self.libs.append(package('statsmodels.api',alias='sm', install_name='statsmodels'))
        self.libs.append(package('statsmodels'))
        self.libs.append(package('statsmodels.formula.api',alias='smf', install_name='statsmodels'))
        self.libs.append(package('scipy.optimize',func='curve_fit', install_name='scipy'))
        self.libs.append(package('scipy.stats',func='shapiro', install_name='scipy'))
    def _add_images_libs(self):
        self.libs.append(package('PIL', install_name='Pillow'))
        self.libs.append(package('cv2', install_name='opencv-python'))
    def _add_formatting_libs(self):
        self.libs.append(package('textwrap'))
    def _add_geo_libs(self):
        self.libs.append(package('geopandas',alias='gpd'))
        self.libs.append(package('geodatasets'))
    def _add_all_libs(self):
        self._add_plot_libs()
        self._add_stats_libs()
        self._add_images_libs()
        self._add_formatting_libs()
        self._add_geo_libs()

    def _install_lib(self, p:package):
        try:
            exec(p.i_s(),self.global_enviro,self.global_enviro)
        except ModuleNotFoundError:
            try:
                subprocess.check_call([sys.executable,'-m','pip','install',p.install_name])
                try:
                    exec(p.i_s(),self.global_enviro,self.global_enviro)
                except ModuleNotFoundError:
                    print(f'Error with {p.name}: wont import')
            except subprocess.CalledProcessError as e:
                print(f'Error installing {p.name}: {e}')
                print(f'Try installing {p.name} manually and try again!')
        

def lib(types=None):
    l = lib_list(types)


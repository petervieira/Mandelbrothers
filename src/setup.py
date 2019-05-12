import cx_Freeze

executables = [cx_Freeze.Executable('mandelbrothers.py')]
options = {'build_exe': {'packages': ['pygame'],
                         'include_files': ['images', 'maps', 'music', 'sounds', 'mapp.py', 'minimap.py', 'settings.py', 'sprites.py', 'text.py'],
                         'build_exe': '../build'}}

cx_Freeze.setup(name = 'Mandelbrothers', options = options, executables = executables)

import sys
import cx_Freeze

base_ = None
if (sys.platform == "win32"):
    base_ = "Win32GUI"

executables = [cx_Freeze.Executable("SERVER.py", base=base_)]

buildOptions = dict(include_files = []) #folder,relative path. Use tuple like in the single file to set a absolute path.
buildOptions.update({"packages": ["psutil", "json"], "include_msvcr": True})

cx_Freeze.setup(
         name = "CellAs",
         version = "1.0",
         description = "description",
         author = "Leandro Peres",
         options = dict(build_exe = buildOptions),
         executables = executables)

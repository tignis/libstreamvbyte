import os
import pathlib
from typing import Dict, Any
import sys
from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext
import re
import subprocess
import setuptools

PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}


class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = ""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext: CMakeExtension):
        cwd = pathlib.Path().absolute()

        debug = int(os.environ.get("DEBUG", 0)
                    ) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={cwd}{os.sep}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
        ]
        build_args = []

        # if self.compiler.compiler_type == "msvc":
        #     cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name],
        #                    f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={cwd}{os.sep}", ]
        #     build_args += ["--config", cfg]
        print("compiler:", self.compiler)
        print("shlib_compiler:", self.shlib_compiler)

        if sys.platform.startswith("darwin"):
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmake_args += [
                    "-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            ["cmake", ext.sourcedir] + cmake_args,
            cwd=build_temp,
            check=True,
        )
        subprocess.run(
            ["cmake", "--build", "."] + build_args,
            cwd=build_temp,
            check=True,
        )


def build(setup_kwargs: Dict[str, Any]):
    setup_kwargs.update(
        name="libstreamvbyte",
        version="0.1.0",
        author="HSING-HAN WU (Xyphuz)",
        author_email="xyphuzwu@gmail.com",
        description="A C++ implementation with Python binding for StreamVByte",
        long_description="",
        ext_modules=[CMakeExtension("libstreamvbyte")],
        cmdclass=dict(build_ext=CMakeBuild),
    )

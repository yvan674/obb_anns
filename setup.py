from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
import subprocess


description = 'A toolkit to work with the Oriented Bounding Boxes annotation ' \
              'schema for datasets.'


def build_with_swig(command_subclass):
    """A decorator that builds the extension using SWIG first.

    Modifies run by first calling the checks for swig and its build command.
    Also takes care of the install.run(self) call.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        print("Installing polyiou extension using SWIG...")
        try:
            r = subprocess.call("swig", stdout=subprocess.DEVNULL)
            if r != 1:
                raise EnvironmentError("Make sure that SWIG is properly "
                                       "installed and is in PATH")
        except FileNotFoundError:
            raise FileNotFoundError("SWIG does not seem to be installed or "
                                    "could not be found in PATH")
        subprocess.call(
            "swig -c++ -python polyiou/polyiou.i",
            stdout=subprocess.DEVNULL
        )
        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


@build_with_swig
class InstallPolyIOU(install):
    """Installs the PolyIOU extension."""
    def run(self):
        install.run(self)
        subprocess.call(
            "python3 polyiou/setup.py build_ext",
            stdout=subprocess.DEVNULL
        )
        print("polyiou extension installed!")


class DevelopPolyIOU(develop):
    """Installs the PolyIOU extension in place"""
    def run(self):
        develop.run(self)
        subprocess.call(
            "python3 polyiou/setup.py build_ext --inplace",
            stdout=subprocess.DEVNULL
        )
        print("polyiou extension installed in place!")


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='obb_anns',
      version='0.1a1',
      description=description,
      long_description=readme(),
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          # 'Programming Language :: Python :: 3 :: Only',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',

      ],
      keywords='AI machine learning neural network deep learning object '
               'detection oriented bounding box annotations segmentation',
      author='Yvan Satyawan',
      license='BSD 3-Clause License',
      packages=['obb_anns'],
      install_requires=[
          'numpy',
          'pillow',
          'colorcet',
          'pandas',
      ],
      python_requires='>=3',
      cmdclass={'install': InstallPolyIOU,
                'develop': DevelopPolyIOU},
      include_package_data=True,
      zip_safe=False)

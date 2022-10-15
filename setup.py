from importlib.metadata import entry_points
from setuptools import setup
import os

def get_readme():
    """returns the contents of the README file"""
    return open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
   name="space-game",
   version="1.0.0",
   description="a simple space-traveling adventure game",   
   long_description=get_readme(),
   author="Kristian Rother",
   author_email="kristian.rother@posteo.de",
   packages=["space_game"],
   url="https://github.com/krother/space",
   license="MIT",
   classifiers=[
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10"
   ],
   entry_points={
        "console_scripts":["space=space_game.space:main"]
   }
)
    

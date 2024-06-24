from pathlib import Path
import argparse
import click
import subprocess
from ploomber_test.runner import CodeRunner
#This is the file that we will run to run all commands contained in a .md file in a specific format
#docker container with the python version that is specified by the user

#When invoking this file the user will pass in two arguments: the file path to the .md file
#and the python version that the user wants to use

#Entry point for the file
@click.group()
def cli():
    print("Hello from the CLI! You have specified for the code in the .md file you passed to be executed in a docker container....")
    start_up_container()
    
#Adding a command which will spin up the docker container with the requested version in the background
@cli.command()
@click.argument("python version")
def start_up_container(python_version):
    #This function will start up a docker container with the specified python version
    subprocess.run(["docker", "run", "-d", f"python:{python_version}"])


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
def run(file_path):
    CodeRunner(Path(file_path).read_text()).run()
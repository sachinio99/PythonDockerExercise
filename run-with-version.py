from pathlib import Path
import argparse
import subprocess
import docker
from ploomber_test.runner import CodeRunner
import click 
import uuid

#This is the file that we will run to run all commands contained in a .md file in a specific format
#docker container with the python version that is specified by the user

#When invoking this file the user will pass in two arguments: the file path to the .md file
#and the python version that the user wants to use


def main():
    print("Hello from the CLI! You have specified for the code in the .md file you passed to be executed in a docker container....")
    parser = argparse.ArgumentParser(description="Run code in a docker container with specified version")
    parser.add_argument("--version", type=str, help="The python version you want to use")
    parser.add_argument('filepath', type=str, help='Path to the Markdown file.')
    args = parser.parse_args()
    removeAllExistingContainers()
    verify_path(args)
    verify_version(args)
    #Once we have verified the input we can start the docker container
    container_name = f"container_{uuid.uuid4()}"
    container = startDockerContainerInBackground(args.version, container_name)
    run(args.filepath,container)
    stopDockerContainer(container_name)



#
def verify_path(args):
    if not args.filepath:
        raise ValueError("File path is required")
    if not Path(args.filepath).exists():
        raise ValueError("File path does not exist")
    
def verify_version(args):
    if not args.version:
        raise ValueError("Python version is required")
    try:
        float(args.version)
    except ValueError:
        raise ValueError("Python version must be a number")
    
def startDockerContainerInBackground(version, container_name):
   client = docker.from_env()
   container = client.containers.run(f"python:{version}", name = container_name, detach=True)
   print(f"Started container with ID: {container.id}")
   return container
    

def stopDockerContainer(container_id):
    subprocess.run(["docker", "stop", container_id])

def run(file_path,container):
    CodeRunner(Path(file_path).read_text()).run(container)

def removeAllExistingContainers():
    client = docker.from_env()
    for container in client.containers.list():
        container.stop()
        container.remove()

if __name__ == '__main__':
    main()
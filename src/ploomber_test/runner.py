import duckdb
from IPython import InteractiveShell
import subprocess

from ploomber_test.parse import iterate_code_chunks
import docker
import uuid


class CodeRunner:
    def __init__(self, text, conn=None):
        self.text = text
        self.shell = InteractiveShell()

        if conn:
            self.conn = conn
        else:
            self.conn = duckdb.connect()

    def run(self,version):
        
        for code in iterate_code_chunks(self.text):
            language = code["language"]
            print(f"Running: {code}")

            if language == "python":
                execution = self.shell.run_cell(code["code"])
                #init docker client
                client = docker.from_env()
                #Create a unique container name for each run so there are no conflicts
                container_name = f"container_{uuid.uuid4()}"
                #Run the container with the specified python version, in the background so we have access to the object
                container = client.containers.run(f"python:{version}", name = container_name, detach = True)
                #client.containers.run(f"python:{version}",code["code"])
                #Now we want to execute the code on the already runnning container
                container.start()
                exec_log = container.exec_run(['python -c "{code["code"]}"'])
                #Print the output of the execution
                print(exec_log)
                #Stop the container and remove after execution
                container.stop()
                container.remove()

                execution.raise_error()

                result = execution.result

                print(f"Output: {result}")
            elif language == "sql":
                result = self.conn.execute(code["code"]).fetchall()
                print(f"Output: {result}")


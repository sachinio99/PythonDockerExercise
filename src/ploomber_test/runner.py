import duckdb
from IPython import InteractiveShell
import subprocess

from ploomber_test.parse import iterate_code_chunks
import docker


class CodeRunner:
    def __init__(self, text, conn=None):
        self.text = text
        self.shell = InteractiveShell()

        if conn:
            self.conn = conn
        else:
            self.conn = duckdb.connect()

    def run(self,container):
        
        for code in iterate_code_chunks(self.text):
            language = code["language"]
            print(f"Running: {code}")

            if language == "python":
                execution = self.shell.run_cell(code["code"])
                #docker_execution = subprocess.run(["docker", "exec", container_id, code["code"]])
                container.exec_run(code["code"])
                #docker_execution.raise_error()

                result = execution.result

                print(f"Output: {result}")
            elif language == "sql":
                result = self.conn.execute(code["code"]).fetchall()
                print(f"Output: {result}")

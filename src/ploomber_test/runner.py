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
        client = docker.from_env()
        container = client.containers.run(f"python:{version}", stdout=True,tty=True,stderr =True, detach =True)
        container.start()
        print(f"The name of the running container is: {container.name}")

        for code in iterate_code_chunks(self.text):
            language = code["language"]
            #print(f"Running: {code}")

            if language == "python":
                #result = execution.result
                try: 
                    container.exec_run(cmd=code['code'],stream=True,stdout = True)
                    print(f"Just ran the following code on the container: {code['code']}")
                except Exception as e:
                    print(f"Error running python: {e}")
                    continue

                #print(f"Output: {result}")
            elif language == "sql":
                #result = self.conn.execute(code["code"]).fetchall()
                try: 
                    container.exec_run(cmd="self.conn.execute(code['code']).fetchall()",stream=True,stdout = True)
                    print(f"Just ran the following code on the container: {code['code']}")
                except Exception as e:
                    print(f"Error running sql: {e}")
                    continue
                print(f"Container status after running sql: {container.status}")
                #print(f"Output: {result}")
        container.stop()
        container.remove()

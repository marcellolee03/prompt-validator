import socket
from core import exec_tempscript
from os import getenv
from dotenv import load_dotenv


load_dotenv(override=True)

LOCALHOST_PASSWORD = getenv("LOCALHOST_PASSWORD")
OPENVAS_USER = getenv("OPENVAS_USER")
OPENVAS_PASSWORD = getenv("OPENVAS_PASSWORD")

filepath = 'core/scan_info'

def start_scan(taskname):
        
    with open(f"{filepath}/startscan.csv", "w") as file:
        file.write(taskname)
    
    script = f'''
    #!/bin/bash

    docker cp {filepath}/startscan.csv greenbone-community-edition-gvmd-1:/auto_vas/startscan.csv

    docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
        source /path/to/venv/bin/activate &&
        cd auto_vas &&
        gvm-script --gmp-username {OPENVAS_USER} --gmp-password {OPENVAS_PASSWORD} socket start-scans-from-csv.py startscan.csv"

    '''
    
    exec_tempscript.exec_tempscript(script, LOCALHOST_PASSWORD)


def create_task(task_name):

    with open(f"{filepath}/ip.txt", "r") as file:
            localhost = file.read()

    csv_content = f'"{task_name}","Target for {localhost}","OpenVAS Default","Full and fast",,,,,,,'

    with open(f"{filepath}/task.csv", "w") as file:
        file.write(csv_content)


    script = f'''
    #!/bin/bash

    docker cp {filepath}/task.csv greenbone-community-edition-gvmd-1:/auto_vas/task.csv

    docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
        source /path/to/venv/bin/activate &&
        cd auto_vas &&
        gvm-script --gmp-username {OPENVAS_USER} --gmp-password {OPENVAS_PASSWORD} socket create-tasks-from-csv.gmp.py task.csv"
    '''

    exec_tempscript.exec_tempscript(script, LOCALHOST_PASSWORD)


def create_target():

    # storing localhost ip
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    with open(f"{filepath}/ip.txt", "w") as file:
        file.write(ip_address)
    
    # creating target for localhost
    script = f'''
        #!/bin/bash

        docker cp {filepath}/ip.txt greenbone-community-edition-gvmd-1:/auto_vas/ip.txt

        docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "
            source /path/to/venv/bin/activate &&
            cd auto_vas &&
            gvm-script --gmp-username {OPENVAS_USER} --gmp-password {OPENVAS_PASSWORD} socket create-targets-from-host-list.gmp.py teste ip.txt"
        '''
    
    exec_tempscript.exec_tempscript(script, LOCALHOST_PASSWORD)
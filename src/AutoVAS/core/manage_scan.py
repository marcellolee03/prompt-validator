from AutoVAS.core import exec_tempscript
from os import getenv, mkdir
from dotenv import load_dotenv


load_dotenv(override=True)

LOCALHOST_PASSWORD = getenv("LOCALHOST_PASSWORD")
OPENVAS_USER = getenv("OPENVAS_USER")
OPENVAS_PASSWORD = getenv("OPENVAS_PASSWORD")


def check_progress(task_name):
    report = get_report(task_name)

    status = report['status']
    progress = report['progress']

    if progress == '100%':
        print('Scan complete!')
        return True
    else:
        print(f'Status: {status} - Progress: {progress}')
        return False


def get_report(task_name):
    reports = list_reports()

    for report in reports:
        if report['task_name'] == task_name:
            return report
    return


def list_reports():

    script = f'''
    docker exec -i --user auto_vas greenbone-community-edition-gvmd-1 bash -c "source /path/to/venv/bin/activate &&\
        cd auto_vas &&\
        gvm-script --gmp-username {OPENVAS_USER} --gmp-password {OPENVAS_PASSWORD} socket list-reports.gmp.py"
    '''

    output = exec_tempscript.return_output_tempscript(script, LOCALHOST_PASSWORD).stdout

    # Parse da saída
    lines = output.strip().splitlines()

    reports = []
    for line in lines:
        # Ignora cabeçalhos e linhas separadoras
        if line.strip().startswith("#") or line.strip().startswith("-") or line.strip() == "":
            continue

        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 7:
            continue  # Linha incompleta, pula

        relatorio = {
            "id": parts[1],
            "creation_time": parts[2],
            "modification_time": parts[3],
            "task_name": parts[4],
            "status": parts[5],
            "progress": parts[6]
        }
        reports.append(relatorio)

    return reports


def save_report(report_id, filename):
    base_path = "scan_reports"
    try:
        mkdir(base_path)
    except FileExistsError:
        pass

    filepath = f"{base_path}/{filename}.csv"

    script = f'''
    #!/bin/bash

    docker exec greenbone-community-edition-gvmd-1 bash -c "chmod 777 /auto_vas"
    
    docker exec --user auto_vas greenbone-community-edition-gvmd-1 bash -c "source /path/to/venv/bin/activate && cd auto_vas && gvm-script --gmp-username {OPENVAS_USER} --gmp-password {OPENVAS_PASSWORD} socket export-csv-report.gmp.py {report_id} pretty_relatorio"
    docker cp greenbone-community-edition-gvmd-1:/auto_vas/pretty_relatorio.csv "{filepath}"
    '''

    exec_tempscript.exec_tempscript(script, LOCALHOST_PASSWORD)

    print('Report saved!')
    print(f'File location: {filepath}')

    return filepath
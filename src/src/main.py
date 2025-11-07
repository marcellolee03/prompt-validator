import time
from getpass import getpass
from datetime import datetime
from core import init_scan, manage_scan


# Creating and starting scan
taskname = datetime.now().strftime("self_scan_%d-%m-%y_%H-%M")

print('Creating target...')
init_scan.create_target()

print('Creating task...')
init_scan.create_task(taskname)

print('Starting scan...')
init_scan.start_scan(taskname)


# Waiting for scan to finish
while not manage_scan.check_progress(taskname):
    time.sleep(5)


# Saving report as csv
report_id = manage_scan.get_report(taskname)['id']
manage_scan.save_report(report_id, taskname)

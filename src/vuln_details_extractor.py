import pandas as pd

def extract_vulnerability_details(scan_report_filepath: str, line: int):
    headers = ['CVEs','NVT Name','Port','Port Protocol','Summary', 'Specific Result', 'Vulnerability Detection Method','Affected Software/OS','Solution']
    vulnerability_details = '-VULNERABILITY DETAILS:\n'

    scan_report = pd.read_csv(scan_report_filepath)

    for header in headers:
        content = scan_report.loc[line, header]
        vulnerability_details += f'**{header}**: ({content})\n'
    
    return vulnerability_details
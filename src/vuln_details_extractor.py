import pandas as pd

def extract_vulnerability_details(scan_report_filepath: str, line: int):
    headers = ['CVEs','NVT Name','Port','Port Protocol','Summary', 'Specific Result', 'Vulnerability Detection Method','Affected Software/OS','Solution']

    scan_report = pd.read_csv(scan_report_filepath)

    vuln_details = {}
    for header in headers:
        content = scan_report.loc[line, header]
        vuln_details[header] = content
    
    return vuln_details
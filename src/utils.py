import argparse

MODELS = ['gemini-2.5-pro', 'deepseek-V3.1']

def parse_arguments():
    parser = argparse.ArgumentParser(description = 'Patch correction generation comparison between different prompt engineering techniques.')

    parser.add_argument('model', choices=MODELS, help='LLM model responsible for patch generation.')
    parser.add_argument('scan_report_filepath', help='Scan report filepath.')
    parser.add_argument('vulnerability_loc', help='Line in scan report containing vulnerability to be mitigated')

    return parser.parse_args()
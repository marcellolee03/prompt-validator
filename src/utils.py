import argparse
from os import makedirs

MODELS = ['gemini-2.5-pro', 'deepseek-V3.1']

def parse_arguments():
    parser = argparse.ArgumentParser(description = 'Patch correction generation comparison between different prompt engineering techniques.')

    parser.add_argument('scan_report_filepath', help='Scan report filepath.')
    parser.add_argument('vulnerability_loc', help='Line in scan report containing vulnerability to be mitigated')

    return parser.parse_args()

def save_results(CVEs: str, LLM_model: str, generated_patch: str, elapsed_time: float):

    base_path = f'patches/{CVEs}'

    try:
        makedirs(base_path)
    except FileExistsError:
        pass


    patch_file = base_path + f'/{LLM_model}_patch.sh'
    details_file = base_path + f'/{LLM_model}_details.txt'

    print(f'Saving correction patch in: {patch_file}')
    with open(patch_file, 'w') as f:
        f.write(generated_patch)
    
    print(f'Saving patch generation details in: {details_file}')
    with open(details_file, 'w') as f:
        f.write('=== PATCH GENERATION DETAILS ===\n')
        f.write(f'Model: {LLM_model}\n')
        f.write(f'Vulnerability: {CVEs}\n')
        f.write(f'Time elapsed: {elapsed_time:.4f} seconds\n')
        f.write('=====================\n')
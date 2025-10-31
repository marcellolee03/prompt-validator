from patch_generator import generate_prompt, ask_LLM
from utils import parse_arguments
from env_scanner import extract_environment_info
from vuln_details_extractor import extract_vulnerability_details
import concurrent.futures

args = parse_arguments()

scan_report_filepath = args.scan_report_filepath
vulnerability_loc = int(args.vulnerability_loc)

print('Extracting vulnerability details...')
vuln_details = extract_vulnerability_details(scan_report_filepath, vulnerability_loc)

print('Extracting environment information...')
env_info = extract_environment_info()

print('Generating prompt...')
prompt = generate_prompt(vuln_details, env_info)

print('Awaiting LLM api response...')
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_gemini = executor.submit(ask_LLM, 'gemini-2.5-pro', prompt)
    future_deepseek = executor.submit(ask_LLM, 'deepseek-R1', prompt)

    gemini_response = future_gemini.result()
    deepseek_response = future_deepseek.result()
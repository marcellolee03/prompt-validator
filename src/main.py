from LLM_patch_generation.patch_generator import generate_prompt, ask_LLM, save_results
from LLM_patch_generation.args_parser import parse_arguments
from LLM_patch_generation.extract_info.env_scanner import extract_environment_info
from LLM_patch_generation.extract_info.vuln_details_extractor import extract_vulnerability_details
from AutoVAS.fully_initiate_scan import fully_initiate_scan
import time


def main():
    scan_report = fully_initiate_scan()

    args = parse_arguments()

    LLM_model = args.LLM_model
    scan_report_filepath = scan_report
    vulnerability_loc = int(args.vulnerability_loc)

    print('Extracting vulnerability details...')
    vuln_details = extract_vulnerability_details(scan_report_filepath, vulnerability_loc)

    print('Extracting environment information...')
    env_info = extract_environment_info()

    print('Generating prompt...')
    prompt = generate_prompt(vuln_details, env_info)
'''
    # Patch generation and elapsed time calculation
    print(f'Awaiting {LLM_model} api response...')

    timer_start = time.perf_counter()

    LLM_response = ask_LLM(LLM_model, prompt["prompt"])

    timer_end = time.perf_counter()
    elapsed_time = (timer_end - timer_start)

    if LLM_response.status == "ERR":
        print(f"ERROR while fetching {LLM_model} response. Shutting down script.")
        print(f"ERROR details: {LLM_response.content}")
        return
    
    # Saving results
    print("Saving results...")
    save_results(prompt["CVEs"], LLM_model, LLM_response.content, elapsed_time)
'''

if __name__ == "__main__":
    main()
from patch_generator import generate_prompt, ask_LLM
from utils import parse_arguments, save_results
from env_scanner import extract_environment_info
from vuln_details_extractor import extract_vulnerability_details
import time


def main():
    args = parse_arguments()

    LLM_model = args.LLM_model
    scan_report_filepath = args.scan_report_filepath
    vulnerability_loc = int(args.vulnerability_loc)

    print('Extracting vulnerability details...')
    vuln_details = extract_vulnerability_details(scan_report_filepath, vulnerability_loc)

    print('Extracting environment information...')
    env_info = extract_environment_info()

    print('Generating prompt...')
    prompt = generate_prompt(vuln_details, env_info)

    # LLM patch generation and elapsed time calculation
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
    save_results(prompt["CVEs"], {LLM_model}, LLM_response.content, elapsed_time)
    

if __name__ == "__main__":
    main()
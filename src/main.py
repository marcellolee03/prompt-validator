from patch_generator import generate_prompt, ask_LLM
from utils import parse_arguments, save_results
from env_scanner import extract_environment_info
from vuln_details_extractor import extract_vulnerability_details
import time


def main():
    args = parse_arguments()

    scan_report_filepath = args.scan_report_filepath
    vulnerability_loc = int(args.vulnerability_loc)

    print('Extracting vulnerability details...')
    vuln_details = extract_vulnerability_details(scan_report_filepath, vulnerability_loc)

    print('Extracting environment information...')
    env_info = extract_environment_info()

    print('Generating prompt...')
    prompt = generate_prompt(vuln_details, env_info)

    # GEMINI patch generation and elapsed time calculation
    print('Awaiting GEMINI api response...')

    gemini_timer_start = time.perf_counter()

    gemini_response = ask_LLM('gemini-2.5-pro', prompt["prompt"])

    gemini_timer_end = time.perf_counter()
    gemini_elapsed_time = (gemini_timer_end - gemini_timer_start)

    if gemini_response.status == "ERR":
        print("ERROR while fetching GEMINI response. Shutting down script.")
        print(f"ERROR details: {gemini_response.content}")
        return
    
    # Saving GEMINI results
    print("Saving GEMINI results...")
    save_results(prompt["CVEs"], "gemini-2.5-pro", gemini_response.content, gemini_elapsed_time)

    # DEEPSEEK patch generation and elapsed time calculation
    print('Awaiting DEEPSEEK api response...')
    deepseek_timer_start = time.perf_counter()

    deepseek_response = ask_LLM('deepseek-R1', prompt["prompt"])

    deepseek_timer_end = time.perf_counter()
    deepseek_elapsed_time = (deepseek_timer_end - deepseek_timer_start)

    if deepseek_response.status == "ERR":
        print("ERROR while fetching DEEPSEEK response. Shutting down script.")
        print(f"ERROR details: {deepseek_response.content}")
        return
    
    # Saving DEEPSEEK results
    print("Saving DEEPSEEK results...")
    save_results(prompt["CVEs"], "deepseek-R1", deepseek_response.content, deepseek_elapsed_time)
    

if __name__ == "__main__":
    main()
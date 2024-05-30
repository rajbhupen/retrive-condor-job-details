import re
from prettytable import PrettyTable



def extract_job_details(log_file_path, job_submitted):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        
    job_submit = False
    transfer_start_time = None
    transfer_end_time = None
    job_end_time = None
    slot_found = False
    # Iterating through each line to find relevant information
    for line in lines:
        if job_submitted in line:
            job_submit = True
            
        if job_submit:
            if "Started transferring input files" in line:
                start_transfer_match = re.search(r"(\d+-\d+-\d+ \d+:\d+:\d+) Started transferring input files", line)
                if start_transfer_match:
                    transfer_start_time = start_transfer_match.group(1)

            if "Finished transferring input files" in line:
                end_transfer_match = re.search(r"(\d+-\d+-\d+ \d+:\d+:\d+) Finished transferring input files", line)
                if end_transfer_match:
                    transfer_end_time = end_transfer_match.group(1)
            if "SlotName" in line:
                slot_name_line = line.strip()
                slot_found = True
            if "Job terminated" in line:
                end_match = re.search(r"(\d+-\d+-\d+ \d+:\d+:\d+) Job terminated", line)
                if end_match:
                    job_end_time = end_match.group(1)
                    break  # Assuming the first termination after start is what we need

                
    return {
        "log_file": log_file_path,
        "slot_name": slot_name_line,
        "transfer_start_time": transfer_start_time or "N/A",
        "transfer_end_time": transfer_end_time or "N/A",
        "job_end_time": job_end_time or "N/A"
    }

    # Printing the extracted information
#    if slot_found:
#        print(f"Job running on slot: {slot_name_line}")
#    else:
#        print("SlotName not found")
#    if transfer_start_time:
#        print(f"Transfer input files started at: {transfer_start_time}")
#    else:
#        print("Started transferring input files time not found.")
#    if transfer_end_time:
#        print(f"Transfer input files finished at: {transfer_end_time}")
#    else:
#        print("Finished transferring input files time not found.")
#
#        
#    if job_end_time:
#        print(f"Job ended at: {job_end_time}")
#    else:
#        print("Job end time not found.")




def process_multiple_logs(log_list_file, job_submitted):
    with open(log_list_file, 'r') as file:
        log_files = file.readlines()

    table = PrettyTable()
    table.field_names = ["Log File", "Slot Name", "Transfer Start Time", "Transfer End Time", "Job End Time"]

    for log_file in log_files:
        log_file_path = log_file.strip()
        job_details = extract_job_details(log_file_path, job_submitted)
        table.add_row([
            job_details["log_file"],
            job_details["slot_name"],
            job_details["transfer_start_time"],
            job_details["transfer_end_time"],
            job_details["job_end_time"]
        ])
        
    print(table)

# Replace 'log_file_list.txt' with the path to your text file containing the list of log file paths
log_list_file = 'log_file_list.txt'
job_submitted = 'Job submitted from host'
process_multiple_logs(log_list_file, job_submitted)





#    for log_file in log_files:
#        log_file_path = log_file.strip()
#        print(f"Processing log file: {log_file_path}")
#        extract_job_details(log_file_path, job_submitted)
#        print("\n" + "-"*50 + "\n")  # Separate outputs for readability

# Replace 'log_file_list.txt' with the path to your text file containing the list of log file paths
#log_list_file = 'log_file_list.txt'
#job_submitted = 'Job submitted from host'
#process_multiple_logs(log_list_file, job_submitted)




        
# Replace 'log_file_path' with the path to your log file and 'slot19_1@simclu-wn01.ino.tifr.res.in' with the desired slot name
#log_file_path = 'condorOutput/jobraj_990.3.log'
#job_submitted = 'Job submitted from host'
#extract_job_details(log_file_path, job_submitted)

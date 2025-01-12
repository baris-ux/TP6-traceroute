import argparse
import subprocess
import re

def run_traceroute(target, progressive, output_file): # prend en argument target, l'adresse cible 
    """
    Execute a tracert command (Windows equivalent of traceroute) and handle its output.
    
    Parameters:
        target (str): The target URL or IP address.
        progressive (bool): If True, display IPs progressively.
        output_file (str): Path to the file where results will be saved.
    """
    try:
        # Open the output file for writing, if specified
        output = open(output_file, 'w') if output_file else None 

        # Start the tracert process (Windows equivalent of traceroute)
        process = subprocess.Popen(
            ["tracert", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if progressive:
            # Progressive mode: Display IPs as they are discovered
            print("Traceroute in progress...")
            for line in iter(process.stdout.readline, ''):
                ip = extract_ip(line)
                if ip:
                    print(ip)  # Print each IP found
                    if output:
                        output.write(ip + '\n')  # Save to file if specified
            process.wait()
        else:
            # Default mode: Wait for tracert to finish and process output
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                ips = [extract_ip(line) for line in stdout.splitlines() if extract_ip(line)]
                for ip in ips:
                    print(ip)  # Print all IPs at once
                    if output:
                        output.write(ip + '\n')
            else:
                print("Error executing tracert:", stderr.strip())

    except FileNotFoundError:
        print("Error: 'tracert' command not found. Please ensure it is installed.")
    finally:
        # Close the output file if it was opened
        if output:
            output.close()

def extract_ip(line):
    """
    Extract an IP address from a tracert line.
    
    Parameters:
        line (str): A single line of tracert output.
    
    Returns:
        str: The extracted IP address, or None if no IP is found.
    """
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'  # Regex for IPv4
    match = re.search(ip_pattern, line)
    return match.group(0) if match else None

if __name__ == "__main__":
    # Argument parser for command-line interface
    parser = argparse.ArgumentParser(description="Traceroute script with options for progressive display and output file.")
    parser.add_argument(
        "target",
        help="The target URL or IP address for the traceroute."
    )
    parser.add_argument(
        "-p", "--progressive",
        action="store_true",
        help="Display IPs progressively as they are discovered."
    )
    parser.add_argument(
        "-o", "--output-file",
        help="Specify a file to save the list of IPs."
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Run the traceroute function with parsed arguments
    run_traceroute(args.target, args.progressive, args.output_file)

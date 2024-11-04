import subprocess
import sys

# Define a mapping of domains to software versions
software_versions = {
    'finance': 'finance_software_v1.3',
    'HR': 'hr_software_v2.1',
    'logistics': 'logistics_software_v3.0'
}

def deploy_software(domain):
    # Check if the domain is supported
    if domain not in software_versions:
        print(f"Error: Domain '{domain}' is not supported.")
        sys.exit(1)
    
    # Get the software version for the domain
    software_version = software_versions[domain]
    
    # Command to deploy the software (this is a placeholder command)
    deploy_command = f"sudo apt-get install {software_version}"
    
    # Execute the deployment command
    try:
        subprocess.run(deploy_command.split(), check=True)
        print(f"Successfully deployed {software_version} in the {domain} domain.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while deploying software: {e}")

if __name__ == "__main__":
    # Example usage: python deploy.py finance
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <domain>")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    print("Before method call")
    deploy_software(target_domain)
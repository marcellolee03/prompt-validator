import subprocess

def run_command(cmd) -> str:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f'Error: {str(e)}'


def list_containers() -> list:
    raw_output = run_command('docker ps --format "{{.Names}}"')
    
    if not raw_output:
        return []
    
    return raw_output.splitlines()


def extract_container_info(container_name: str) -> str:
    full_command = f"""docker exec {container_name} sh -c 'echo "**OS INFO**"; cat /etc/os-release 2>/dev/null || cat /etc/issue; echo -e "\\n**USER INFO**"; id; echo -e "\\n**PACKAGE MANAGER**"; which apk apt-get yum dnf 2>/dev/null; echo -e "\\n**TOOLS**"; which curl wget sed awk python3 2>/dev/null'"""
    
    return run_command(full_command)
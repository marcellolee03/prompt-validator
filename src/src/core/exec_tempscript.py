import tempfile
import subprocess
import os

def exec_tempscript(script, senha):
    with tempfile.NamedTemporaryFile(mode="w", delete = False, suffix=".sh") as tempscript:
        tempscript.write(script)
        tempscript_path = tempscript.name
    
    try:
        comando = ["sudo", "-S", "bash", tempscript_path]
        subprocess.run(
            comando,
            input = senha.encode(),
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )
    
    finally:
        if os.path.exists(tempscript_path):
            os.remove(tempscript_path)


def return_output_tempscript(script, password):
    with tempfile.NamedTemporaryFile(mode="w", delete = False, suffix=".sh") as tempscript:
        tempscript.write(script)
        tempscript_path = tempscript.name
    
    try:
        comando = ["sudo", "-S", "bash", tempscript_path]
        output = subprocess.run(
            comando,
            input = password,
            capture_output= True,
            text=True
        )
    
    finally:
        if os.path.exists(tempscript_path):
            os.remove(tempscript_path)
    
    return output
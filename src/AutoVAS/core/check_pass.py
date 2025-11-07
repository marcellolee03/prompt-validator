import subprocess

def check_sudo_pass(senha: str):
    try:
        comando = ['sudo', '-S', 'true']

        processo = subprocess.Popen(
            comando,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines = True
        )

        saida, erro = processo.communicate(input = senha + '\n')

        return processo.returncode == 0
    
    except Exception as e:
        print(f"Erro durante a verificação: {str(e)}")
        return False

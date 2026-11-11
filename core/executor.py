import subprocess

def run_command(args, timeout=120):
    if not isinstance(args, (list, tuple)) or not args:
        return -1, "Invalid command arguments."
    if not all(isinstance(arg, str) for arg in args):
        return -1, "All command arguments must be strings."
    if any("\0" in arg for arg in args):
        return -1, "Invalid null byte in arguments."
    
    try:
        result = subprocess.run(
            list(args),
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        output = (result.stdout or "") + (result.stderr or "")
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return -1, "Command timed out."
    except FileNotFoundError:
        return -1, f"Command not found: {args[0]}"
    except OSError as e:
        return -1, str(e)

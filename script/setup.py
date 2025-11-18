import subprocess
import platform

def run(cmd):
    print(f"\n> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    venv_dir = "venv"
    is_windows = platform.system() == "Windows"

    print("📦 Creating virtual environment...")
    if is_windows:
        run(f"py -m venv {venv_dir}")
    else:
        run(f"python3 -m venv {venv_dir}")

    print("\n🚀 Installing dependencies...")
    pip_cmd = (
        f"{venv_dir}\\Scripts\\pip" 
        if is_windows 
        else f"{venv_dir}/bin/pip"
    )

    run(f"{pip_cmd} install --upgrade pip")
    run(f"{pip_cmd} install -r requirements.txt")

    activate = (
        f"{venv_dir}\\Scripts\\activate"
        if is_windows
        else f"source {venv_dir}/bin/activate"
    )

    if is_windows:
        print(f"\n💡 Before activate your environment, run:\n   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass")

    print(f"\n💡 To activate your environment, run:\n   {activate}")


if __name__ == "__main__":
    main()

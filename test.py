import subprocess

program_path = "C:\\Program Files (x86)\\HEIDENHAIN\\TNCremo\\TNCcmdPlus.exe"

for i in range(1, 26):
    subprocess.Popen(["",program_path, f"./Data/tnccmd/HP-{i:02d}.tnccmd"], creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)

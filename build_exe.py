import os
import subprocess
import shutil

def build():
    print("Building BizProcess Optimizer Pro EXE...")
    
    # Paths
    project_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(project_dir, "main.py")
    dist_dir = os.path.join(project_dir, "dist")
    desktop_dir = "D:/Backup/Desktop"
    
    # PyInstaller command
    cmd = [
        "python", "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "BizProcessOptimizerPro",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "pyqtgraph",
        "--hidden-import", "requests",
        "--hidden-import", "bcrypt",
        "--add-data", f"{os.path.join(project_dir, 'ui')};ui",
        "--add-data", f"{os.path.join(project_dir, 'pages')};pages",
        "--add-data", f"{os.path.join(project_dir, 'components')};components",
        "--add-data", f"{os.path.join(project_dir, 'database')};database",
        "--add-data", f"{os.path.join(project_dir, 'translations')};translations",
        "--add-data", f"{os.path.join(project_dir, 'services')};services",
        "--add-data", f"{os.path.join(project_dir, 'assets')};assets",
        main_file
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    # Copy to Desktop
    exe_path = os.path.join(dist_dir, "BizProcessOptimizerPro.exe")
    if os.path.exists(exe_path):
        print(f"Copying EXE to Desktop...")
        shutil.copy(exe_path, os.path.join(desktop_dir, "BizProcessOptimizerPro.exe"))
        print("Success! EXE is now on your Desktop.")
    else:
        print("Build failed: EXE not found.")

if __name__ == "__main__":
    build()

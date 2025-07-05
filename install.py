#!/usr/bin/env python3
"""
Smart installation script for Smiley Splash game
This script will create a virtual environment and install dependencies safely
"""

import subprocess
import sys
import os
import venv

def run_command(command, description, cwd=None):
    """Run a command and print the result"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            print(f"✅ Success!")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment already exists at {venv_path}")
        return venv_path
    
    print(f"\n🏗️  Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print(f"✅ Virtual environment created at {venv_path}")
        return venv_path
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return None

def get_venv_python_path():
    """Get the path to the Python executable in the virtual environment"""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

def get_venv_pip_path():
    """Get the path to the pip executable in the virtual environment"""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "pip.exe")
    else:
        return os.path.join("venv", "bin", "pip")

def main():
    print("🎮 Welcome to Smiley Splash Installation!")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or newer is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version OK: {sys.version.split()[0]}")
    
    # Create virtual environment
    venv_path = create_virtual_environment()
    if not venv_path:
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Get paths to virtual environment executables
    venv_python = get_venv_python_path()
    venv_pip = get_venv_pip_path()
    
    # Install dependencies in virtual environment
    print(f"\n📦 Installing dependencies in virtual environment...")
    success = run_command(f"{venv_pip} install -r requirements.txt", 
                         "Installing pygame and numpy in virtual environment")
    
    if not success:
        print("\n⚠️  Installation failed. Trying alternative method...")
        success = run_command(f"{venv_python} -m pip install pygame numpy", 
                             "Installing with python -m pip")
    
    if not success:
        print("\n❌ Could not install dependencies automatically.")
        print("Please try running manually:")
        print(f"   {venv_pip} install pygame numpy")
        sys.exit(1)
    
    # Test the installation
    print(f"\n🎯 Testing pygame installation...")
    test_success = run_command(f"{venv_python} -c \"import pygame; print('Pygame version:', pygame.version.ver)\"", 
                              "Testing pygame import")
    
    if not test_success:
        print("❌ Pygame test failed!")
        sys.exit(1)
    
    # Test the game
    print(f"\n🎯 Checking game files...")
    if os.path.exists("main.py"):
        print("✅ Game file found!")
        
        # Create a run script
        create_run_script(venv_python)
        
        print("\n🎉 Installation complete!")
        print("\n🚀 To start the game, run:")
        if sys.platform == "win32":
            print("   run_game.bat")
        else:
            print("   ./run_game.sh")
        print("\n   Or manually:")
        print(f"   {venv_python} main.py")
        print("\nHave fun clicking those smileys! 😄")
    else:
        print("❌ main.py not found!")
        sys.exit(1)

def create_run_script(venv_python):
    """Create a convenient run script"""
    if sys.platform == "win32":
        # Windows batch file
        with open("run_game.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"echo Starting Smiley Splash...\n")
            f.write(f"{venv_python} main.py\n")
            f.write(f"pause\n")
        print("✅ Created run_game.bat")
    else:
        # Unix shell script
        with open("run_game.sh", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"echo \"Starting Smiley Splash...\"\n")
            f.write(f"{venv_python} main.py\n")
        # Make executable
        os.chmod("run_game.sh", 0o755)
        print("✅ Created run_game.sh")

if __name__ == "__main__":
    main() 
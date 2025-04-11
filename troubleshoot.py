#!/usr/bin/env python3
"""
Troubleshooting script for Agent Village
This script helps diagnose and fix common issues with the Agent Village system.
"""

import os
import sys
import subprocess
import pkg_resources
import platform
from pathlib import Path

def check_python_version():
    """Check Python version and provide recommendations."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 10):
        print("❌ Python 3.10 or higher is required.")
        print("  Please upgrade your Python installation.")
        return False
    else:
        print("✓ Python version is compatible.")
        return True

def check_dependencies():
    """Check installed dependencies and their versions."""
    required = {
        "flask": "2.3.3",
        "pyautogen": "0.8.5",
        "openai": "1.72.0",
        "python-dotenv": "1.1.0"
    }
    
    issues = []
    
    for package, min_version in required.items():
        try:
            installed = pkg_resources.get_distribution(package)
            print(f"{package}: {installed.version}")
            
            if pkg_resources.parse_version(installed.version) < pkg_resources.parse_version(min_version):
                issues.append(f"{package} version {installed.version} is older than required {min_version}")
        except pkg_resources.DistributionNotFound:
            issues.append(f"{package} is not installed")
    
    if issues:
        print("\n❌ Dependency issues found:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nTo fix, run: pip install -r requirements.txt")
        return False
    else:
        print("✓ All dependencies are installed with compatible versions.")
        return True

def check_env_file():
    """Check .env file configuration."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found.")
        print("  Please run setup.py or create a .env file manually.")
        return False
    
    with open(env_file, "r") as f:
        content = f.read()
        
        if "OPENAI_API_KEY" not in content:
            print("❌ OPENAI_API_KEY not found in .env file.")
            return False
        
        if "your_openai_api_key_here" in content:
            print("❌ OpenAI API key not set in .env file.")
            print("  Please edit .env to add your actual OpenAI API key.")
            return False
    
    print("✓ .env file is properly configured.")
    return True

def check_file_permissions():
    """Check file permissions for log files."""
    files_to_check = ["agent_logs.txt", "current_strategy.txt"]
    issues = []
    
    for file in files_to_check:
        path = Path(file)
        if path.exists():
            if not os.access(path, os.W_OK):
                issues.append(f"{file} is not writable")
        else:
            # Try to create the file to test permissions
            try:
                with open(path, "w") as f:
                    f.write("")
                os.remove(path)
            except (IOError, PermissionError):
                issues.append(f"Directory is not writable for creating {file}")
    
    if issues:
        print("\n❌ Permission issues found:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nPlease check file and directory permissions.")
        return False
    else:
        print("✓ File permissions are correct.")
        return True

def check_openai_api():
    """Test OpenAI API connection."""
    try:
        from dotenv import load_dotenv
        import openai
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("❌ OpenAI API key not found in environment.")
            return False
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print("✓ OpenAI API connection successful.")
        return True
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False

def main():
    """Main troubleshooting function."""
    print("Agent Village Troubleshooting\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Configuration", check_env_file),
        ("File Permissions", check_file_permissions),
        ("OpenAI API Connection", check_openai_api)
    ]
    
    all_passed = True
    
    for name, check in checks:
        print(f"\nChecking {name}...")
        if not check():
            all_passed = False
    
    if all_passed:
        print("\n✓ All checks passed! Your system is ready to run Agent Village.")
    else:
        print("\n❌ Some issues were found. Please fix them before running Agent Village.")
        print("  Run 'python run.py' after fixing the issues.")

if __name__ == "__main__":
    main() 
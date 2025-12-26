"""
Test Installation Script for StoryWriterAgent
Verifies all components are properly installed and configured.
"""
import sys
import os

def print_status(name, success, message=""):
    status = "✓" if success else "✗"
    color = "\033[92m" if success else "\033[91m"
    reset = "\033[0m"
    print(f"  {color}{status}{reset} {name}" + (f" - {message}" if message else ""))

def test_python_version():
    version = sys.version_info
    success = version.major >= 3 and version.minor >= 8
    print_status(
        "Python Version",
        success,
        f"{version.major}.{version.minor}.{version.micro}" + (" (OK)" if success else " (Need 3.8+)")
    )
    return success

def test_dependencies():
    dependencies = [
        ("openai", "OpenAI SDK"),
        ("fastapi", "FastAPI Framework"),
        ("uvicorn", "Uvicorn Server"),
        ("dotenv", "Python Dotenv"),
        ("jinja2", "Jinja2 Templates"),
        ("colorama", "Colorama"),
        ("pydantic", "Pydantic")
    ]

    all_success = True
    for module, name in dependencies:
        try:
            __import__(module)
            print_status(name, True)
        except ImportError:
            print_status(name, False, "Not installed")
            all_success = False

    return all_success

def test_env_file():
    env_exists = os.path.exists(".env")
    print_status(".env File", env_exists, "Found" if env_exists else "Not found")

    if env_exists:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        has_key = bool(api_key and len(api_key) > 10)
        print_status("OpenAI API Key", has_key, "Configured" if has_key else "Missing or invalid")
        return has_key

    return False

def test_config():
    try:
        from config import Config
        Config.validate()
        print_status("Configuration", True, "Valid")
        return True
    except Exception as e:
        print_status("Configuration", False, str(e))
        return False

def test_story_agent():
    try:
        from story_agent import StoryAgent
        # Just test import, don't initialize (requires valid API key)
        print_status("Story Agent Module", True, "Loaded")
        return True
    except Exception as e:
        print_status("Story Agent Module", False, str(e))
        return False

def test_web_app():
    try:
        from web_app import app
        print_status("Web Application", True, "Ready")
        return True
    except Exception as e:
        print_status("Web Application", False, str(e))
        return False

def test_directories():
    dirs = ["static", "templates", "stories"]
    all_exist = True
    for d in dirs:
        exists = os.path.isdir(d)
        print_status(f"Directory: {d}", exists)
        if not exists:
            all_exist = False
    return all_exist

def test_files():
    files = [
        "main.py",
        "config.py",
        "story_agent.py",
        "web_app.py",
        "templates/index.html",
        "static/style.css",
        "static/script.js"
    ]
    all_exist = True
    for f in files:
        exists = os.path.isfile(f)
        if not exists:
            print_status(f"File: {f}", False, "Missing")
            all_exist = False
    if all_exist:
        print_status("All required files", True, f"{len(files)} files found")
    return all_exist

def main():
    print("\n" + "=" * 50)
    print("  StoryWriterAgent - Installation Test")
    print("=" * 50 + "\n")

    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Environment", test_env_file),
        ("Directories", test_directories),
        ("Files", test_files),
        ("Configuration", test_config),
        ("Story Agent", test_story_agent),
        ("Web Application", test_web_app),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n[{name}]")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_status(name, False, f"Error: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 50)
    passed = sum(1 for _, r in results if r)
    total = len(results)

    if passed == total:
        print(f"\033[92m  All tests passed! ({passed}/{total})\033[0m")
        print("\n  You can now run the application:")
        print("    python main.py --web      # Web interface")
        print("    python main.py --terminal # Terminal interface")
    else:
        print(f"\033[93m  {passed}/{total} tests passed\033[0m")
        print("\n  Please fix the issues above before running.")

    print("=" * 50 + "\n")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

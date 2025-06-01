#!/usr/bin/env python3
"""
Daily Routine Manager - Application Runner
This script provides an easy way to start the application with proper setup.
"""

import sys
import subprocess
import os
import argparse
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        print("Please upgrade Python and try again.")
        return False
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'plotly',
        'pandas',
        'numpy'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 To install missing packages, run:")
        print("   pip install -r requirements.txt")
        return False

    return True


def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = Path("routine_data")
    if not data_dir.exists():
        try:
            data_dir.mkdir(exist_ok=True)
            (data_dir / "backups").mkdir(exist_ok=True)
            print("✅ Created data directories")
        except Exception as e:
            print(f"❌ Error creating data directory: {e}")
            return False
    return True


def setup_sample_data():
    """Set up sample data for first-time users"""
    try:
        from routine_storage import RoutineStorage, create_sample_data

        storage = RoutineStorage()

        # Check if any data already exists
        routines = storage.load_routines()
        workout_plans = storage.load_workout_plans()
        meal_plans = storage.load_meal_plans()

        if not routines and not workout_plans and not meal_plans:
            print("🎯 Setting up sample data for first-time use...")
            create_sample_data(storage)
            print("✅ Sample data created!")

        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not set up sample data: {e}")
        return True  # Non-critical error


def check_streamlit():
    """Check if Streamlit is available and working"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "streamlit", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True
        else:
            print("❌ Streamlit not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Streamlit not found or not responding")
        return False


def start_application(port=8501, debug=False):
    """Start the Streamlit application"""
    print("🚀 Starting Daily Routine Manager...")
    print("📊 Loading application components...")

    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", "daily_routine_app.py",
            "--server.port", str(port),
            "--browser.gatherUsageStats", "false"
        ]

        if not debug:
            cmd.extend([
                "--server.headless", "false",
                "--logger.level", "error"
            ])
        else:
            cmd.extend([
                "--logger.level", "debug"
            ])

        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False

    return True


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Daily Routine Manager")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the app on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--setup", action="store_true", help="Run setup only")
    parser.add_argument("--sample-data", action="store_true", help="Create sample data")

    args = parser.parse_args()

    print("📅 Daily Routine Manager")
    print("=" * 50)

    # Install dependencies if requested
    if args.install:
        if not install_dependencies():
            return 1
        print("🎉 Dependencies installed! Now run without --install flag.")
        return 0

    # Setup mode
    if args.setup:
        print("🔧 Running setup...")

        checks = [
            ("Python Version", check_python_version),
            ("Dependencies", check_dependencies),
            ("Data Directory", create_data_directory),
            ("Streamlit", check_streamlit)
        ]

        for check_name, check_function in checks:
            print(f"   Checking {check_name}...", end=" ")
            if check_function():
                print("✅")
            else:
                print("❌")
                print(f"\n💥 Setup failed at: {check_name}")
                return 1

        print("\n🎉 Setup completed successfully!")
        return 0

    # Sample data creation
    if args.sample_data:
        print("🎯 Creating sample data...")
        if setup_sample_data():
            print("✅ Sample data created!")
            return 0
        else:
            print("❌ Failed to create sample data")
            return 1

    # Full startup checks
    print("🔧 Performing startup checks...")

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Data Directory", create_data_directory),
        ("Streamlit", check_streamlit),
        ("Sample Data", setup_sample_data)
    ]

    for check_name, check_function in checks:
        print(f"   Checking {check_name}...", end=" ")
        if check_function():
            print("✅")
        else:
            print("❌")
            if check_name != "Sample Data":  # Sample data is non-critical
                print(f"\n💥 Startup failed at: {check_name}")
                print("🔧 Try running with --install to install dependencies")
                print("🔧 Or run with --setup to diagnose issues")
                return 1

    print("\n🎉 All checks passed!")
    print("🌐 Starting web application...")
    print(f"🔗 The application will be available at: http://localhost:{args.port}")
    print("\n💡 To stop the application, press Ctrl+C in this terminal")
    print("-" * 50)

    # Start the application
    if start_application(port=args.port, debug=args.debug):
        print("\n✅ Application started successfully!")
        return 0
    else:
        print("\n❌ Failed to start application")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
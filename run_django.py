import os
import sys
import django

if __name__ == "__main__":
    # Set DJANGO_SETTINGS_MODULE to the correct settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_project.settings')
    
    # Ensure the settings are loaded before any access
    try:
        django.setup()
    except ImportError as e:
        print(f"Error importing Django settings: {e}")
        sys.exit(1)
    
    # Call the manage.py script to run the server
    from django.core.management import execute_from_command_line
    sys.argv = [sys.argv[0], 'runserver', '0.0.0.0:8000']  # Specify IP and port
    execute_from_command_line(sys.argv)

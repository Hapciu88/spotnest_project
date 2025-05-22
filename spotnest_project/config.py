import os
from pathlib import Path


# Get the current directory of this script
current_directory = Path(__file__).resolve().parent.parent

# Search for the 'spotnest_project_content' directory in the current directory
project_root = None
for root, dirs, files in os.walk(current_directory):
    if 'spotnest_project_content' in dirs:
        project_root = Path(root) / 'spotnest_project_content'
        break

# If 'spotnest_project_content' is not found, raise an error
if project_root is None:
    raise FileNotFoundError("Could not find 'spotnest_project_content' directory")

# Setting up configuration variables for the project
config = {
    'templatesLocation': os.path.join(project_root, 'templates'),  # Path for template files
    'staticRootLocation': os.path.join(project_root, 'static_root'),  # Path for collected static files
    'staticLocation': os.path.join(project_root, 'static'),  # Path for app-level static files
    'mediaLocation': os.path.join(project_root, 'media')  # Path for app-level static files
}

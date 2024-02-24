#%%

import os, fnmatch
from pathlib import Path
from typing import Union
import shutil
import re

import argparse

def findReplace(
        directory : Union[os.PathLike, str], 
        find : Union[str, re.Pattern], 
        replace : str,
        filePattern : str
        ) -> None:
    """Recursively find and replace text in files in a directory.
    
    Parameters
    ----------
    directory : Union[os.PathLike, str]
        The directory to search in.
    find : str, re.Pattern
        The text to find.
        Either a string or a regular expression.
    replace : str
        The text to replace with.
    filePattern : str
        The file pattern to search for.
    
    Returns
    -------
    None
    """

    if isinstance(find, str):
        replace_func = lambda s: s.replace(find, replace)
    elif isinstance(find, re.Pattern):
        replace_func = lambda s: find.sub(replace, s)
    else:
        raise TypeError("find must be a string or a regular expression.")
    
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = replace_func(s)
            with open(filepath, "w") as f:
                f.write(s)



# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Update Joplin export')

# Add arguments
parser.add_argument('--origin', type=str, help='Origin directory', default=r"C:\Users\Niebaum\Desktop\joplin_export")
parser.add_argument('--destination', type=str, help='Destination directory', default=r"C:\Users\Niebaum\Documents\Repositories\sdm-eurec4a-notes")

# Parse the arguments
args = parser.parse_args()

# Define the directories
origin_dir = Path(args.origin)
destination_dir = Path(args.destination)
# #%%

if input(f"\n- Origin: {origin_dir}"
      f"\n- Destination: {destination_dir}"
      "\nAre these correct directories? [yes/no]\n"
      ) in ["yes", "Yes", "YES", "y", "Y"]:
    pass
else:
    raise KeyboardInterrupt("User cancelled the operation.")


print(f"\nCopying the files from origin_dir to destination_dir...")
html_dir = origin_dir / "Master-Thesis"
new_html_dir = destination_dir / "_includes" / "Master-Thesis"
new_html_dir.mkdir(exist_ok=True, parents=False)

# Copy the original directory to a new directory
shutil.copytree(html_dir, new_html_dir, dirs_exist_ok=True)


# copy all files from the _resources folder to the assets folder    
resource_dir = origin_dir / Path("_resources")
new_resource_dir = destination_dir / "assets" / "images"

print(f"\nCopying the files from resource_dir to new_resource_dir...")
shutil.copytree(resource_dir, new_resource_dir, dirs_exist_ok=True)

# copy all files from the pluginAssets folder to the assets folder

print(f"\nCopying the files from pluginAssets to new_plugin_assets_dir...")
new_plugin_assets_dir = destination_dir / "assets" / "pluginAssets"

for path, dirs, files in os.walk(new_html_dir):
    for dir in dirs :
        if dir == "pluginAssets":
            shutil.copytree(os.path.join(path, dir), new_plugin_assets_dir, dirs_exist_ok=True)

print(f"\nRemoving the pluginAssets folders from the old destinations ...")
# remove all subfolders with the name pluginAssets
for path, dirs, files in os.walk(new_html_dir):
    for dir in dirs:
        if dir == "pluginAssets":
            shutil.rmtree(os.path.join(path, dir))



# Modify the copied directory
# Modify the links to the pluginAssets
print(f"\nModifying the links to the pluginAssets ...")
findReplace(
    directory=new_html_dir,
    find="pluginAssets/",
    replace="/assets/pluginAssets/",
    filePattern="*.html"
)

# Modify the links to the _resources
print(f"\nModifying the links to the _resources ...")
pattern = r"(\.\./)*_resources/"
regex = re.compile(pattern, re.IGNORECASE)
findReplace(
    directory=new_html_dir,
    find=regex,
    replace="https://nilsnevertree.github.io/sdm-eurec4a-notes/assets/images/",
    filePattern="*.html"
)

# Remove the header string from the html files
print(f"\nRemoving the header string from the html files ...")
header_str = "<!DOCTYPE html>"
findReplace(
    directory=new_html_dir,
    find=header_str,
    replace="",
    filePattern="*.html"
)

# %%

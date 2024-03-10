#%%

import os, fnmatch
from pathlib import Path
from typing import Union
import shutil
import re
from bs4 import BeautifulSoup as bs
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

def findReplaceRelativePathImages(
        directory : Union[os.PathLike, str], 
        filePattern : str
        ) -> None:
    """Recursively find and replace text in files in a directory.
    
    Parameters
    ----------
    directory : Union[os.PathLike, str]
        The directory to search in.
    filePattern : str
        The file pattern to search for.
    
    Returns
    -------
    None
    """

    # Regex for the full substring
    pattern_full = r"(\.\./)*_resources/([a-zA-Z0-9])+\.(png|jpg|gif|yaml)"
    regex_full = re.compile(pattern_full)
    # regex for the _resources pattern
    pattern_resource = r"(\.\./)*_resources"
    regex_resource = re.compile(pattern_resource, re.IGNORECASE)

    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            # print(filepath)
            with open(filepath) as f:
                s = f.read()
            # Extract the full substring from the original string
            lines = []
            for line in s.split("\n"):
                match = regex_full.search(line)
                if match is not None:
                    name = match.group(0)
                    # Replace the _resources with the new path
                    name = regex_resource.sub('{{"assets/images', name)
                    # Add the end of the string
                    name += '" | relative_url }}'
                    # Replace the full substring with the new path
                    line = regex_full.sub(name, line)
                else:
                    pass
                lines.append(line)
            res = "\n".join(lines)
            with open(filepath, "w") as f:
                f.write(res)


# Create an ArgumentParser object
# parser = argparse.ArgumentParser(description='Update Joplin export')

# # # Add arguments
# parser.add_argument('--origin', type=str, help='Origin directory', default=r"C:\Users\Niebaum\Desktop\joplin_export")
# parser.add_argument('--destination', type=str, help='Destination directory', default=r"C:\Users\Niebaum\Documents\Repositories\sdm-eurec4a-notes")

# # Parse the arguments
# args = parser.parse_args()

# # Define the directories
# origin_dir = Path(args.origin)
# destination_dir = Path(args.destination)

origin_dir = Path(r"C:\Users\Niebaum\Documents\Uni\Master\MasterThesis\joplin_notes")
destination_dir = Path(r"C:\Users\Niebaum\Documents\Repositories\sdm-eurec4a-notes")

# if input(f"\n- Origin: {origin_dir}"
#       f"\n- Destination: {destination_dir}"
#       "\nAre these correct directories? [yes/no]\n"
#       ) in ["yes", "Yes", "YES", "y", "Y"]:
#     pass
# else:
#     raise KeyboardInterrupt("User cancelled the operation.")


print(f"\nCopying the files from origin_dir to destination_dir...")
html_dir = origin_dir / "Master-Thesis"
new_html_dir = destination_dir / "_includes" / "Master-Thesis"
new_html_dir.mkdir(exist_ok=True, parents=False)

# Copy the original directory to a new directory
shutil.copytree(html_dir, new_html_dir, dirs_exist_ok=True)

print(f"\nRefactor html files ...")
# And some other stuff
for path, dirs, files in os.walk(os.path.abspath(new_html_dir)):
    for filename in fnmatch.filter(files, '*.html'):
        filepath = os.path.join(path, filename)
        with open(filepath, "r") as f:
            s = f.read()

        # get a soup object
        soup = bs(s, features="html.parser")                #make BeautifulSoup

        # remove the katex-html span
        for div in soup.find_all("span", {'class':'katex-html'}): 
            div.decompose()

        # remove the style tag to have the random style still active
        for style in soup.find_all("style"):
            style.decompose()

        # remove all the joplin-source tags for spand and pre
        for jpsrc in soup.find_all("span", {'class': 'joplin-source'}) :
            jpsrc.decompose()
        for jpsrc in soup.find_all("pre", {'class': 'joplin-source'}) :
            jpsrc.decompose()

        for cl in soup.find_all("joplin-source"):
            cl.decompose()
        # remove the head 
        # for head in soup.find_all("head"):

        prettyHTML = soup.prettify(formatter="html")   #prettify the html
        # remove the DOCTYPE HEADER
        # prettyHTML.replace("<!DOCTYPE html>", "")
        s = prettyHTML

        # remove the meta tag and the DOCType
        s = s.replace("<!DOCTYPE html>", "")
        s = s.replace("</meta>", "")
        with open(filepath, "w") as f:
            f.write(s)


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
    find="pluginAssets/katex/katex.css",
    replace=r"{{/assets/pluginAssets/katex/katex.css | prepend: baseurl}}",
    filePattern="*.html"
)
findReplace(
    directory=new_html_dir,
    find="pluginAssets/highlight.js/atom-one-light.css",
    replace=r"{{/assets/pluginAssets/highlight.js/atom-one-light.css | prepend: baseurl}}",
    filePattern="*.html"
)
findReplace(
    directory=new_html_dir,
    find="pluginAssets/mermaid/mermaid.min.js",
    replace=r"{{/assets/pluginAssets/mermaid/mermaid.min.js | prepend: baseurl}}",
    filePattern="*.html"
)
findReplace(
    directory=new_html_dir,
    find="pluginAssets/mermaid/mermaid_render.js",
    replace=r"{{/assets/pluginAssets/mermaid/mermaid_render.js | prepend: baseurl}}",
    filePattern="*.html"
)


# Modify the links to the _resources
print(f"\nModifying the links to the _resources ...")

findReplaceRelativePathImages(
    directory=new_html_dir,
    filePattern="*.html"
)
# %%

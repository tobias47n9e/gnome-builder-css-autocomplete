# gnome-builder-css-autocomplete

Basic CSS autocompletion plugin for Gnome Builder.

This is still work in progress and has bugs!

# Installation

Place the files in `src` in `.local/share/gnome-builder/plugins/`.
Then restart Builder.

# Completion data

The completion data is base on this file:
https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/css/generated/properties-db.js

# Rebuild the completion data

Copy the contents of this file into a file `mozilla.json` and
place it into the project directory. Remove all the text around the
first JSON object. Then run:

    python3 convert_mozilla_to_python.py

Make sure the new `__init__.py` file contains no mistakes. Then
replace the file in `src/suggestions/__init__.py` with the new file.


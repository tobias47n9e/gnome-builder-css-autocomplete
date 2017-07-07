import json
import os
import textwrap

path = os.path.dirname(os.path.realpath(__file__))

with open(path + "/mozilla.json", "r") as import_file:
    import_data = import_file.read()
    import_json = json.loads(import_data)
    export_dict = {}

    for key in import_json:
        if key.startswith('-'):
            continue

        values = []

        for value in import_json[key]['values']:
            if value.startswith('-'):
                continue

            values.append(value)

        export_dict[key] = values

    print(export_dict)

    with open(path + "/__init__.py", "w") as export_file:
        wrapped_text = textwrap.fill(str(export_dict), 80,
                                     break_long_words=False,
                                     break_on_hyphens=False)
        export_file.write("SUGGESTIONS = {}".format(wrapped_text))


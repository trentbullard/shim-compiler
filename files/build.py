import json
import re


def build_page(content):
    file_string = ""
    if content.items():
        for key, value in content.items():
            if key != 'locals':
                try:
                    file_string += open(f'files/shims/{key}.htm').read()
                except:
                    print(f'failed to open shim file {key}')
                    return file_string
                if re.findall('<!-- <\( replace \)> -->', file_string):
                    file_string = file_string.replace(
                        '<!-- <( replace )> -->', build_page(value))
            else:
                for local_key, local_value in value.items():
                    if re.findall(f'<!-- <\( {local_key} \)> -->', file_string):
                        file_string = file_string.replace(
                            f'<!-- <( {local_key} )> -->', local_value)
    return file_string


layout = json.load(open('files/layout.json', 'r'))

pages = layout['pages']
file_names = list(pages.keys())

for file_name, page_content in pages.items():
    with open(f'{file_name}.htm', 'w') as file:
        file.write(build_page(page_content))

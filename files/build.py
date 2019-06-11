import json
import re


def build_page(content):
    file_string = ""
    if isinstance(content, list):
        for child in content:
            file_string += build_page(child)
    else:
        for key, value in content.items():
            if key == 'locals':
                continue
            try:
                file_string += open(f'files/shims/{key}.htm').read()
            except:
                print(f'failed to open shim file {key}')
                continue
            if re.findall('~~ replace ~~', file_string):
                file_string = file_string.replace(
                    '~~ replace ~~', build_page(value))
            if 'locals' in value:
                for local_key, local_value in value['locals'].items():
                    special = f'~~ {local_key} ~~'
                    if re.findall(special, file_string):
                        file_string = file_string.replace(
                            f'~~ {local_key} ~~', local_value)
    return file_string


layout = json.load(open('files/layout.json', 'r'))
pages = layout['pages']

for file_name, page_content in pages.items():
    with open(f'{file_name}.htm', 'w') as file:
        file.write(build_page(page_content))

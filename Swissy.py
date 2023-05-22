def beautify_leef(input_text: str) -> str:
    # Split the input text into parts using "|" as a delimiter.
    parts = input_text.split("|", maxsplit=5)
    header = "\n".join(parts[:5])
    fields = parts[5]

    # Split the fields into key-value pairs using " " as a delimiter.
    key_value_pairs = fields.split(" ")

    beautified_text = header + "\n"
    # Replace "=" with ": " in each key-value pair and join them with newline.
    for pair in key_value_pairs:
        if "=" in pair:
            beautified_text += "\n" + pair.replace("=", ": ")
        else:
            beautified_text += " " + pair

    return beautified_text

def parse_and_format_xml(xml, indent=''):
    formatted_xml = ''

    lines = xml.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("<") and not line.startswith("</"):
            key = line.split('<')[1].split('>')[0].split()[0]
            if "/" not in key:
                try:
                    value = line.split('>')[1].split('<')[0]
                except IndexError:
                    value = ""

                # Check if there's a Data Name attribute and use it as the key
                if key == "Data" and 'Name' in line:
                    key = line.split('Name="')[1].split('"')[0]

                if line.endswith("/>"):
                    formatted_line = ""  # Skip self-closing tags from the formatted output
                else:
                    formatted_line = f"{indent}{key}: "
                    indent += '  '
                    formatted_value = parse_and_format_xml(value, indent)

                    # Only add closing tags and newlines to nested elements, ignore for others
                    if formatted_value and not formatted_value.startswith('</'):
                        formatted_line += f"{formatted_value}\n"
                    else:
                        formatted_line += f"{formatted_value}"

                    indent = indent[:-2]
        elif line.startswith("</"):
            formatted_line = ""
        else:
            formatted_line = f"{indent}{line}\n"

        formatted_xml += formatted_line

    return formatted_xml.strip()

import sublime
import sublime_plugin
import json
import re
import base64
from datetime import datetime
import string


## The Author of this is Moises Santiago SOC Analyst.
## 

class MagicDecoderCommand(sublime_plugin.TextCommand):

    def lain_unravel(self, navis: str) -> str:
        protocol_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        pad_character = '='
        cyberia_mind = []
        data_stream = 0
        bit_accumulation = 0

        for char in navis:
            if char == pad_character:
                break

            data_stream = (data_stream << 6) | protocol_alphabet.index(char)
            bit_accumulation += 6
            if bit_accumulation >= 8:
                bit_accumulation -= 8
                transformed_char = chr((data_stream >> bit_accumulation) & 0xFF)
                cyberia_mind.append(transformed_char)

        return ''.join(cyberia_mind)

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                # Get the selected text
                s = self.view.substr(region)
                # Transform the input string
                try:
                    transformed = self.lain_unravel(s)
                    # Replace the selected region with the transformed string
                    self.view.replace(edit, region, transformed)
                except Exception as e:
                    print("Error: ", str(e))
                    
class ConvertToHumanReadableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")

        for region in regions:
            timestamp = self.view.substr(region)
            cur_format = "%Y-%m-%d %H:%M:%S"
            target_format = "On %B %d, %Y at %I:%M:%S %p"

            try:
                datetime_object = datetime.strptime(timestamp, cur_format)
                human_readable = datetime_object.strftime(target_format)
                self.view.replace(edit, region, human_readable)
            except Exception as e:
                sublime.message_dialog("Error: " + str(e))

class BeautifyLogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            view = self.view

            # If there's no current selection, select the whole view.
            if view.sel()[0].size() == 0:
                region = sublime.Region(0, view.size())
            else:
                region = view.sel()[0]

            content = view.substr(region)

            # Check if the content contains "LEEF" and beautify.
            if 'LEEF' in content:
                content = beautify_leef(content)
            # Check if the content contains XML and beautify.
            elif 'xmlns' in content:
                content = parse_and_format_xml(content)
            else:
                # Define a helper function to check if a string is valid JSON.
                def is_valid_json(s):
                    try:
                        json.loads(s)
                        return True
                    except:
                        return False

                # Define a helper function to find JSON objects in the content.
                def find_json(content):
                    brackets = {'{': '}', '[': ']'}
                    stack = []
                    start = -1
                    for i, c in enumerate(content):
                        if c in brackets:
                            if not stack:
                                start = i
                            stack.append(brackets[c])
                        elif stack and c == stack[-1]:
                            stack.pop()
                            if not stack:
                                if is_valid_json(content[start:i+1]):
                                    yield start, i+1
                                start = -1

                # Beautify the JSON objects found in the content.
                for start, end in reversed(list(find_json(content))):
                    j = json.loads(content[start:end])
                    content = content[:start] + json.dumps(j, indent=4) + content[end:]

            # Replace the content in the view with the beautified content.
            view.replace(edit, region, content)
            # Display a status message indicating success.
            sublime.status_message('Content Beautified')
        except Exception as e:
            # Display an error message in case of an exception.
            sublime.status_message('Error: ' + str(e))
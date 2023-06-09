# Swissy: The Swiss Army Knife for Cybersecurity in Sublime Text

Swissy is a Sublime Text plugin that provides several handy commands and tools for cybersecurity professionals within the Sublime Text editor. It's designed to make your life easier by offering various features such as decoding base64 strings, making timestamps more human-readable, and beautifying log files.

## Features

- Decode highlighted text (base64)
- Convert timestamps to a human-readable format
- Beautify log files (LEEF format and XML)
- Reformat JSON data

## Commands

### Decode highlighted text

- Command: `magic_decoder`
- Caption: "Decode highlighted text"

This command decodes the base64 encoded text you have highlighted in the editor.

### Convert timestamps to a human-readable format

- Command: `convert_to_human_readable`
- Caption: "Convert time to human readable"

This command finds all timestamps in the current file and converts them to a more human-readable format.

### Beautify log files

- Command: `beautify_log`
- Caption: "Beauitfy Logs"

This command beautifies log file content according to LEEF logs, XML, or JSON data.

## Usage

To use Swissy in Sublime Text, you can add the following commands to your command palette or context menu:

```json
[
  {
    "caption": "Beauitfy Logs",
    "command": "beautify_log"
  },
  {
    "caption": "Decode highlighted text",
    "command": "magic_decoder"
  },
  {
    "caption": "Convert time to human readable",
    "command": "convert_to_human_readable"
  }
]
```

## Limitations

Swissy may not be able to handle some corner cases, e.g., malformed base64 or JSON data. Moreover, it currently supports LEEF log and XML beautification, but other log formats might not be supported. Future development may provide support for additional formats and improved error handling.

## Disclaimer

We are not responsible for any issues that may arise from the use of Swissy. The plugin is provided "as is" without any guarantees or warranties. By using Swissy, you acknowledge that we have no control over, and assume no responsibility for, any damage or loss resulting from the use of this plugin.

We do not, in any way, store, modify, or transmit your data for any purposes other than providing the intended functionality of the tool within Sublime Text. It is solely your responsibility to ensure that the data you work with is handled securely and in compliance with any applicable laws and regulations.

Please use Swissy responsibly and consider any security implications when working with sensitive data or log files.

## Feedback and Contributions

Feel free to provide feedback or suggest new features you'd like to see in Swissy to help make it even more helpful for cybersecurity professionals! We welcome contributions and improvements from the community.
# SMS Extractor

The `SMS Extractor` is a tool that extracts text messages from an XML file and summarizes them in Markdown format, for intended use in [Obidian.md](https://obsidian.md). The tool uses the `requests` library to send the extracted messages to the [Ollama](https://ollama.ai) API for summary generation, to keep everything **offline and secure**.

## Installation

To install the `SMS Extractor`, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/bscholer/SMS-Extractor.git
```
2. Navigate to the repository directory and run the tool:
```bash
python SMS_Extractor.py
```
## Features


* Extracts text messages from an XML file
* Summarizes the extracted messages using the Obsidian platform
* Generates a new file for each day of data in the XML file

## Usage

1. Open the script and specify the path to the XML file containing the text messages (`sms_extractor.py`)

1. Run the tool:
```bash
python sms_extractor.py
```
3. The tool will extract and summarize the text messages in the XML file for each day, generating a new file for each day.


# Data Masking Tool

A Python tool for masking sensitive data in various file formats using OpenAI's GPT models. The tool supports multiple input and output formats including PDF, EML (email), TXT, and MD (markdown) files. I don't suggest using chat gpt for real life data, use LLMs that work on your hardware.

## Features

- Support for multiple file formats:
  - PDF files
  - EML (email) files
  - Text files (.txt)
  - Markdown files (.md)
- Custom logging system
- Configurable OpenAI model selection
- Flexible input/output handling
- Easy-to-extend architecture for new file formats

## Prerequisites

```bash
pip install -r requirements.txt
```

Required packages:
- PyPDF2
- fpdf
- openai
- python-dotenv

## Configuration

1. Create a `.env` file in the project root directory
2. Add your OpenAI API key:
```
API_KEY=your_api_key_here
```
3. Create a `system_prompt.txt` file with your OpenAI system message

## Usage

### Basic Usage

```python
from data_masking import OpenaiDataMasking

# Initialize the masking tool
data_masking = OpenaiDataMasking(
    api_key="your_api_key",
    start_msg="your_system_prompt"
)

# Mask data from a file
data_masking.mask_data_from_file(
    file_path="path/to/input/file",
    output_path="path/to/output/file"
)
```

### Command Line Usage

```bash
python data_masking.py
```

### Custom Logging

The tool includes a custom logging system that can be configured:

```python
logger = CustomLogger(
    logger_log_level=logging.DEBUG,
    file_handler_log_level=logging.DEBUG
).create_logger()
```

## Project Structure

```
project/
├── data_masking.py    # Main script
├── .env              # Environment variables
├── system_prompt.txt # OpenAI system prompt
├── Data/            # Input data directory
├── Output/          # Output data directory
└── logs.log         # Log file
```

## Class Reference

### OpenaiDataMasking

Main class for handling data masking operations.

#### Parameters:
- `api_key` (str): OpenAI API key
- `start_msg` (str): System prompt for OpenAI
- `model` (str, optional): OpenAI model name (default: "gpt-4o-mini")

#### Methods:
- `mask_data(content: str) -> str`: Masks sensitive data in the provided content
- `mask_data_from_file(file_path: str, output_path: str) -> str`: Processes a file and saves masked output
- `load_data(file_path: str) -> str`: Loads content from a file
- `save_data(content: str, output_path: str) -> str`: Saves masked content to a file

### CustomLogger

Class for setting up logging configuration.

#### Parameters:
- `format` (str): Log message format
- `log_file_name` (str): Name of the log file
- `logger_name` (str): Name of the logger
- `logger_log_level` (int): Logging level for the logger
- `file_handler_log_level` (int): Logging level for the file handler

## Error Handling

The tool includes comprehensive logging for debugging and error tracking. Logs are saved to `logs.log` by default.

## Contributing

To add support for a new file format:
1. Add a new loader method in the `OpenaiDataMasking` class
2. Add a new saver method in the `OpenaiDataMasking` class
3. Update the `loaders` and `savers` dictionaries in `__post_init__`

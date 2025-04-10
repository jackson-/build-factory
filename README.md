# Construction PDF Data Extractor

A prototype tool for extracting structured data from construction PDFs, specifically focused on plumbing work packages.

## Features

- Extracts structured data from construction PDFs including:
  - Item/Fixture Types
  - Quantities
  - Page References
  - Associated Dimensions

Future data to be extracted:
  - Model Numbers / Spec References
  - Mounting Type

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit demo:
```bash
python3 src/pdf2json.py
```

2. Upload a PDF file through the web interface

## Technologies Used

- `pdfplumber` - PDF text and table extraction
- `anthropic` - LLM for abbreviation parsing

## Limitations

- Currently optimized for pipes and not other compenent types
- Unaware of mounting types, model numbers, and spec refs
- Regex could be a bit more general on parsing the initial abbreviations
- Error handling could be a bit more specific
- Lack of layout awareness
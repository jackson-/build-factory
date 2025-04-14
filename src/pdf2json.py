import json
import os
import re

import anthropic
from dotenv import load_dotenv
import pdfplumber

load_dotenv()
class PDFExtractor:
    def __init__(self):
        self.abbreviations = None
        self.components = []
        self.pipes_pattern = None
        self.component_quantities = {}
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def parse_pipes(self, text, page_num):
        """Parse the text for pipe dimensions and types."""
        abbrev_pattern = '|'.join(re.escape(k) for k in self.abbreviations.keys())
        self.pipes_pattern = re.compile(rf'''(?P<dimensions>\d+( |-)\d\/\d"ø) (?P<component_abbreviation>({abbrev_pattern}))( BE= (?P<elevation>\d+' -\d+))?''')
        for match in self.pipes_pattern.finditer(text):
            try:
                match_dict = match.groupdict()
                quantity_key = f"pipe: {match_dict['dimensions']} {self.abbreviations[match_dict['component_abbreviation']]}"
                if match_dict['elevation'] is not None:
                    quantity_key += f" {match_dict['elevation']}"
                if quantity_key not in self.component_quantities:
                    self.component_quantities[quantity_key] = 0
                self.component_quantities[quantity_key] += 1
                self.components.append({
                    "dimensions": match_dict["dimensions"],
                    "type": "pipe",
                    "component_abbreviation": match_dict["component_abbreviation"],
                    "elevation": match_dict["elevation"],
                    "page": page_num + 1
                    })
            except Exception as e:
                print("Error parsing pipes: ", e)
                continue
        

    def extract_abbreviations(self, text_lines):
        """Extract abbreviations and their meanings from the text."""
        system_prompt = """Look at the acronym and the phrase following it. 
        Return a number representing the confidence of the acronym being an abbreviation of the phrase.
        
        IMPORTANT: Respond ONLY with a number between 0 and 100. Nothing else.

        Example:
        Input:
        AS AIR SEPARATOR
        Output:
        100

        Input:
        OM EXIT PATH
        Output:
        0

        Input:
        DN DOWN
        Output:
        85
        """
        abbrev_dict = {}        
        for line in text_lines:
            # Match abbreviation patterns like "AS AIR SEPARATOR"
            match = re.match(r'^([A-Z]{1,5}) +(([A-Z]+ ?)+)$', line)
            if match:
                abbrev = match.group(1)
                full_name = match.group(2)
                response = self.claude.messages.create(
                    model="claude-3-7-sonnet-20250219",
                    temperature=0.0,
                    max_tokens=4000,
                    system=system_prompt,
                    messages=[{
                        "role": "user",
                        "content": [{"type": "text", "text": f"{abbrev} {full_name}"}]
                    }]
                )
                try:
                    confidence = int(response.content[0].text)
                    if confidence >= 75:
                        abbrev_dict[abbrev] = full_name
                except Exception as e:
                    print("Error getting response from Claude: ", e)
                    continue
        return abbrev_dict

    def parse_pdf(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                print("PAGE: ", page_num)
                text = page.extract_text()
                if text.strip() == "":
                    continue
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                # Extract abbreviations from page
                if self.abbreviations is None:
                    self.abbreviations = self.extract_abbreviations(lines)
                self.parse_pipes(text, page_num)

    def export_json(self, pipes_path, component_quantities_path):
        with open(pipes_path, "w", encoding='utf-8') as f:
            json.dump(self.components, f, indent=4, ensure_ascii=False)
        with open(component_quantities_path, "w", encoding='utf-8') as f:
            json.dump(self.component_quantities, f, indent=4, ensure_ascii=False)

    
                

if __name__ == "__main__":
    pdf_path = "M&P mark-up against shop systems piping.pdf"
    extractor = PDFExtractor()
    data = extractor.parse_pdf(pdf_path)
    extractor.export_json("pipes.json", "component_quantities.json")
    exit()
import pdfplumber
from PyPDF2 import PdfReader
import re

pdf_file_path = 'standard.pdf'

tocpdfprompt="Validate response based on theory of change rules; suggest clarification/question. in 30 words "
ntocpdfprompt="Summarize if content follows rules of with 'theory of change' concept else deny"

# Function to extract sections from the PDF based on numeric headings and uppercase words
def extract_sections_from_pdf(file_path):
    sections = []
    rquestions=[]
    current_section = ""

    # Regex patterns
    heading_pattern = r'\d{1,2}\.'
    uppercase_pattern = r'\b[A-Z]+\b'

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.splitlines()

                for line in lines:
                    # Detect and combine consecutive uppercase words
                    uppercase_matches = re.findall(uppercase_pattern, line)
                    if uppercase_matches:
                        combined_uppercase = " ".join(uppercase_matches)
                        # Remove uppercase words from the line
                        line = re.sub(uppercase_pattern, '', line).strip()
                        # Append the combined uppercase words to the sections
                        sections.append(combined_uppercase.strip())

                    # Check if the line matches the numeric heading pattern (1. or 10. or 11.)
                    if re.match(heading_pattern, line):
                        # If there's already content in current_section, save it to sections
                        if current_section:
                            rques=current_section
                            rquestions.append(rques.strip())
                        # Start a new section with the current line
                        current_section = line
                    else:
                        # If the line does not match, append it to the current section
                        current_section += ' ' + line

                # After the loop, add the last section if it exists
                if current_section:
                    rquestions.append(current_section.strip())

    return rquestions


def extract_sections_from_and_text(text):
    sections = []
    rquestions=[]
    current_section = ""

    # Regex patterns
    heading_pattern = r'\d{1,2}\.'
    uppercase_pattern = r'\b[A-Z]+\b'

    if text:
        # Split the text into lines
        lines = text.splitlines()

        for line in lines:
            # Detect uppercase words and combine them
            uppercase_matches = re.findall(uppercase_pattern, line)
            if uppercase_matches:
                combined_uppercase = " ".join(uppercase_matches)
                # Append the combined uppercase words to sections
                sections.append(combined_uppercase.strip())
                # Remove uppercase words from the line
                line = re.sub(uppercase_pattern, '', line).strip()

            # Check if the line matches the heading pattern
            if re.match(heading_pattern, line):
                # Save the current section if it's not empty
                if current_section:
                    rquestions.append(current_section.strip())
                # Start a new section with the current line
                current_section = line
            else:
                # If the line does not match a heading, append it to the current section
                current_section += ' ' + line

        # After processing all lines, save the last section if it exists
        if current_section:
            rquestions.append(current_section.strip())


    return rquestions


def extract_answer_from_pdf(text):
    
    ranswers = list(dict.fromkeys(extract_sections_from_and_text(text)[1:]))
    ranswers = [s for s in ranswers if re.search(r'[a]+\.\ ', s)]
    # ranswers = [s[match.start():] for s in ranswers if (match := re.search(r'[a]+\. ', s))]

    return ranswers

rquestions = extract_sections_from_pdf(pdf_file_path)[1:]

def check_type_of_pdf(raw_text):
    text=raw_text
    query=[]
    if rquestions[0] in text:
        ranswers = extract_answer_from_pdf(text)
        # print(ranswers)
        # if len(rquestions) != len(ranswers):
        #     rpt="Error in pdf upload or few questions are unanswered"
        #     query.append(rpt)
        # else:
        for question,ranswer in zip(rquestions,ranswers):
            rpt=tocpdfprompt+question+"answer:"+ranswer
            query.append(rpt)
    else:
        rpt=ntocpdfprompt+text
        query.append(rpt)
    return query

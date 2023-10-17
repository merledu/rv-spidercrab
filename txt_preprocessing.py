import os
import fitz
import re
import pandas as pd
import datetime
import json  
import nltk
from nltk.corpus import stopwords

def extract_and_split_content(pdf_path):
    chapter_pattern =r'^Chapter \d+|^Appendix [A-Z]'  
    section_pattern = r'^\d+\.\d+|^[A-Z]\.\d+|\d+\.\d+\.\d+'

    pdf_document = fitz.open(pdf_path)
    section_data = []
    current_chapter = ""
    current_section = ""
    current_content = ""

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4]

            # Check if the text matches a chapter heading pattern
            if re.match(chapter_pattern, text):
                # If it's a chapter heading, treat it as a section
                if current_section and current_content:
                    section_data.append((current_section, current_content))
                current_section = text
                current_content = ""
            # Check if the text matches a section pattern
            elif re.match(section_pattern, text):
                if current_section and current_content:
                    section_data.append((current_section, current_content))
                current_section = text
                current_content = ""
            else:
                # Append the text to the current content
                current_content += text + " "

    # Add the last section and its content to the section_data list
    if current_section and current_content:
        section_data.append((current_section, current_content))

    pdf_document.close()
    return section_data

pdf_path = 'book-riscv-rev1.pdf'
section_data = extract_and_split_content(pdf_path)

section_list = [{"section": row[0], "content": row[1]} for row in section_data]

for entry in section_list:
    entry['section'] = entry['section'].replace('\n', ' ')
    content = entry['content']
    content = content.lower()
    words = nltk.word_tokenize(content)
    filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
    clean_text = ' '.join(filtered_words)
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', clean_text)
    entry['content'] = clean_text
    entry['content'] = entry['content'].replace('\n', ' ')
    entry['content'] = entry['content'].strip()
    entry['url'] = "RV32ISPEC.pdf#segment" + str(section_list.index(entry))
    entry['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry['segment'] = 'segment' + str(section_list.index(entry))
    entry['image_urls'] = []
    entry['Book'] = os.path.splitext(os.path.basename(pdf_path))[0]

with open('Final_Output.json', 'w') as json_file:
    json.dump(section_list, json_file, indent=4) 

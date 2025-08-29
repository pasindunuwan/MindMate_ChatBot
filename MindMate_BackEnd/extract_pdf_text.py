import pdfplumber
import os
import nltk
nltk.download('punkt')  # For sentence splitting

def extract_text_from_pdfs(pdf_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    documents = []
    doc_metadata = []
    for root, _, files in os.walk(pdf_folder):
        for pdf_file in files:
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(root, pdf_file)
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    # Clean text
                    text = text.strip().replace('\n\n', '\n').replace('  ', ' ')
                    if text:
                        # Split into paragraphs
                        paragraphs = text.split('\n')
                        current_chunk = ""
                        current_words = 0
                        chunk_id = 0
                        for para in paragraphs:
                            para_words = len(para.split())
                            if current_words + para_words <= 500:
                                current_chunk += para + "\n"
                                current_words += para_words
                            else:
                                if current_chunk:
                                    output_path = os.path.join(output_folder, f"{pdf_file}_chunk_{chunk_id}.txt")
                                    with open(output_path, 'w', encoding='utf-8') as f:
                                        f.write(f"Source: {pdf_file}\nScale: Unknown\nLevel: Unknown\nTechnique: Unknown\nRemote Adaptation: Unknown\nContent: {current_chunk}")
                                    documents.append(current_chunk)
                                    doc_metadata.append({'file': pdf_file, 'chunk': chunk_id})
                                    chunk_id += 1
                                current_chunk = para + "\n"
                                current_words = para_words
                        # Save final chunk
                        if current_chunk:
                            output_path = os.path.join(output_folder, f"{pdf_file}_chunk_{chunk_id}.txt")
                            with open(output_path, 'w', encoding='utf-8') as f:
                                f.write(f"Source: {pdf_file}\nScale: Unknown\nLevel: Unknown\nTechnique: Unknown\nRemote Adaptation: Unknown\nContent: {current_chunk}")
                            documents.append(current_chunk)
                            doc_metadata.append({'file': pdf_file, 'chunk': chunk_id})
    return documents, doc_metadata

# Run extraction
pdf_folder = './pdf_knowledge_base/'
output_folder = './text_knowledge_base/'
documents, doc_metadata = extract_text_from_pdfs(pdf_folder, output_folder)

# Save metadata
with open('pdf_metadata.txt', 'w') as f:
    for meta in doc_metadata:
        f.write(f"{meta['file']} | Chunk {meta['chunk']}\n")
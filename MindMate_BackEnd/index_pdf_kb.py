from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

text_folder = './text_knowledge_base/'
documents = []
doc_paths = []
for file in os.listdir(text_folder):
    if file.endswith('.txt'):
        with open(os.path.join(text_folder, file), 'r', encoding='utf-8') as f:
            documents.append(f.read())
            doc_paths.append(file)

# Use CPU-only model to avoid TensorFlow
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
embeddings = model.encode(documents, show_progress_bar=True)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))
faiss.write_index(index, 'pdf_knowledge_base_index.faiss')

with open('text_metadata.txt', 'w') as f:
    for path in doc_paths:
        f.write(f"{path}\n")
# test_paths.py
try:
    with open(r"C:\Users\User\Desktop\test_rasa3\text_metadata.txt", 'r') as f:
        print("Metadata file accessible:", f.read()[:100])
    import faiss
    index = faiss.read_index(r"C:\Users\User\Desktop\test_rasa3\pdf_knowledge_base_index.faiss")
    print("FAISS index accessible")
except Exception as e:
    print(f"Error: {e}")
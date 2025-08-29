import os

def tag_chunks(text_folder):
    for file in os.listdir(text_folder):
        if file.endswith('.txt'):
            path = os.path.join(text_folder, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            source = lines[0].split(': ')[1]
            content = ''.join(lines[5:])  # Skip metadata
            scale = "Unknown"
            level = "Unknown"
            technique = "Unknown"
            adaptation = "Unknown"
            if "depression" in content.lower():
                scale = "Depression"
                if "moderate" in content.lower() or "score 14-20" in content.lower():
                    level = "Moderate"
                elif "severe" in content.lower() or "score 21-27" in content.lower():
                    level = "Severe"
            elif "anxiety" in content.lower():
                scale = "Anxiety"
                if "moderate" in content.lower() or "score 10-14" in content.lower():
                    level = "Moderate"
            elif "stress" in content.lower():
                scale = "Stress"
                if "moderate" in content.lower() or "score 19-25" in content.lower():
                    level = "Moderate"
            if "remote" in content.lower() or "work from home" in content.lower():
                adaptation = "Practice during work breaks or virtual meetings."
            if "mindfulness" in content.lower():
                technique = "Mindfulness Meditation"
            elif "pmr" in content.lower() or "progressive muscle" in content.lower():
                technique = "Progressive Muscle Relaxation"
            elif "breathing" in content.lower():
                technique = "Deep Breathing"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"Source: {source}Scale: {scale}\nLevel: {level}\nTechnique: {technique}\nRemote Adaptation: {adaptation}\nContent: {content}")
tag_chunks('./text_knowledge_base/')
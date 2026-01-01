from sentence_transformers import SentenceTransformer, util
import cv2
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def text_similarity(new_text, existing_texts):
    if not existing_texts:
        return []

    embeddings = model.encode([new_text] + existing_texts)
    scores = util.cos_sim(embeddings[0], embeddings[1:])[0]

    return list(scores)

def image_similarity(img1, img2):
    try:
        i1 = cv2.imread(img1)
        i2 = cv2.imread(img2)
        if i1 is None or i2 is None:
            return 0

        i1 = cv2.resize(i1, (200, 200))
        i2 = cv2.resize(i2, (200, 200))

        diff = cv2.absdiff(i1, i2)
        score = 1 - (diff.mean() / 255)

        return float(score)
    except:
        return 0


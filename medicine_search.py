import os

import numpy as np
from gensim.models import KeyedVectors

from database import DatabaseConnection
from preprocessing import PreprocessingText


class MedicineSearch:
    def __init__(self, database_name='medicine'):
        self.db = DatabaseConnection(user='root', password='', database=database_name)
        self.preprocessing = PreprocessingText()
        self.model = self._load_model()

    def _load_model(self):
        model_path = "GoogleNews-vectors-negative300-SLIM.bin.gz"
        if os.path.exists(model_path):
            print("Loading Word2Vec model...")
            model = KeyedVectors.load_word2vec_format(model_path, binary=True)
            print("Model loaded successfully")
            return model

        from gensim.downloader import load

        print("Model not found locally. Downloading 'word2vec-google-news-300' ...")
        return load("word2vec-google-news-300")

    def run(self):
        query = "SELECT Medicine_Name, Uses, Composition, Side_Effects FROM medicine"
        data = self.db.select(query)

        if not data:
            print("No Database connection")
            return

        processed_data = [self.preprocessing.preprocess(' '.join(row[:2])) for row in data]
        document_vectors = []
        for doc in processed_data:
            vectors = [self.model[word] for word in doc if word in self.model]
            if vectors:
                document_vectors.append(np.mean(vectors, axis=0))
            else:
                document_vectors.append(np.zeros(self.model.vector_size))

        while True:
            user_query = input("\nEnter your search query (or 'exit' to quit): ")
            if user_query.lower() == 'exit':
                print("Goodbye!")
                break

            query_tokens = self.preprocessing.preprocess(user_query)
            expanded_query_tokens = self.preprocessing.expand_query(query_tokens)
            vectors = [self.model[word] for word in expanded_query_tokens if word in self.model]
            if vectors:
                query_vector = np.mean(vectors, axis=0)
            else:
                print("No valid tokens found in query.")
                continue

            similarities = []
            for doc_vec in document_vectors:
                if np.linalg.norm(doc_vec) == 0:
                    similarities.append(0)
                else:
                    sim = np.dot(doc_vec, query_vector) / (np.linalg.norm(doc_vec) * np.linalg.norm(query_vector))
                    similarities.append(sim)

            top_indices = np.argsort(similarities)[::-1][:5]
            print("\nTop matching results:")
            for i in top_indices:
                uses_items = [item.strip() for item in data[i][1].split("Treatment of") if item.strip()]
                uses_display = "\n  - ".join(uses_items)
                print(f"Medicine Name: {data[i][0]}")
                print(f"Uses:\n  - {uses_display}" if len(uses_items) > 1 else f"Uses: {uses_items[0] if uses_items else ''}")
                print(f"Composition: {data[i][2]}")
                print(f"Side Effects: {data[i][3]}")
                print(f"Similarity Score: {similarities[i]:.4f}")
                print("-" * 50)

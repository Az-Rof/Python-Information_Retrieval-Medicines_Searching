# Medicine Search Engine

A command-line based Information Retrieval system for searching medicines based on their uses, composition, and side effects. This project uses Natural Language Processing (NLP) techniques and Word Embeddings (Word2Vec) to understand user queries and find the most relevant medicines from a MySQL database using Cosine Similarity.

## Features

- **Text Preprocessing**: Utilizes NLTK for tokenization, stop-word removal, and lemmatization.
- **Query Expansion**: Expands user queries with synonyms using WordNet to improve search results.
- **Word Embeddings**: Uses Gensim with a pre-trained Word2Vec model (`GoogleNews-vectors-negative300`) to create document and query embeddings.
- **Cosine Similarity**: Calculates the semantic similarity between the user query and medicine descriptions.
- **Database Integration**: Fetches medicine records (Name, Uses, Composition, Side Effects) from a MySQL database using `mysql-connector-python`.

## Project Structure

- `main.py`: The entry point of the application.
- `medicine_search.py`: Contains the core logic for loading the model, vectorizing documents, computing similarities, and handling the search loop.
- `preprocessing.py`: Handles text cleaning, normalization, and query expansion using NLTK.
- `database.py`: Manages the MySQL database connection and executes queries.
- `medicine.sql`: The database dump file containing the dataset.
- `GoogleNews-vectors-negative300-SLIM.bin.gz`: The pre-trained slim Word2Vec model used for generating embeddings.
- `requirements.txt`: Lists all Python dependencies required to run the project.

## Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.x
- MySQL Server (e.g., XAMPP, WAMP, or standalone MySQL)

## Installation & Setup

1. **Clone or Extract the Project**
   Ensure all files are in your project directory.

2. **Set up the Database**
   - Start your MySQL server.
   - Create a new database named `medicine`.
   - Import the `medicine.sql` file into the `medicine` database.
   - *Note: Default database credentials in `database.py` are `user='root'`, `password=''`, `host='localhost'`. Modify them if your setup is different.*

3. **Set up a Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv .venv
   ```
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

4. **Install Dependencies**
   Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Word2Vec Model**
   The project expects `GoogleNews-vectors-negative300-SLIM.bin.gz` in the root directory. If the file is not present, the script will attempt to download the full `word2vec-google-news-300` model via Gensim's downloader automatically (which may take some time depending on your internet connection).

## Usage

Run the main script to start the search engine CLI:

```bash
python main.py
```

Once the application starts and the model is loaded, you will see a prompt to enter your search query:

```text
Database connected successfully
Loading Word2Vec model...
Model loaded successfully

Enter your search query (or 'exit' to quit): painkiller for headache
```

The system will display the top 5 matching medicines based on semantic similarity.

## Technologies Used
- **Python 3**
- **Gensim** (Word2Vec)
- **NLTK** (Natural Language Toolkit)
- **NumPy**
- **MySQL / MySQL Connector**

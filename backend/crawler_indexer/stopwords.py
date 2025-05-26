import os

def load_stopwords(filename: str = 'vietnamese-stopwords-dash.txt') -> set[str]:
    dir_path = os.path.dirname(os.path.realpath(__file__))  # thư mục của stopwords.py
    path = os.path.join(dir_path, filename)
    with open(path, encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

STOPWORDS_SET = load_stopwords()

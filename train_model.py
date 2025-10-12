# train_model.py

import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

print("--- Starting Model Training ---")

# --- Text Preprocessing Functions ---
# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 1]
    return " ".join(tokens)

# 1. Load the dataset
print("Step 1: Loading dataset 'mbti_1.csv'...")
df = pd.read_csv('mbti_1.csv')

# 2. Preprocess the text data
print("Step 2: Cleaning and preprocessing text data... (This might take a minute)")
df['clean_posts'] = df['posts'].apply(clean_text)

# 3. Define features (X) and labels (y)
X = df['clean_posts']
y = df['type']

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 5. Vectorize the text data
print("Step 3: Vectorizing text data with TF-IDF...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 6. Train the machine learning model
print("Step 4: Training the Multinomial Naive Bayes model...")
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# 7. Save the trained model and vectorizer
print("Step 5: Saving the model and vectorizer to .pkl files...")
joblib.dump(model, 'mbti_model.pkl')
joblib.dump(vectorizer, 'mbti_vectorizer.pkl')

print("--- Training complete! 'mbti_model.pkl' and 'mbti_vectorizer.pkl' have been created. ---")
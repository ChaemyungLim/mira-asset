import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Any, Dict, Optional, List

class StockTickerFinder:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.company_df = None

    def load_company_data(self, file_path):
        self.company_df = pd.read_excel(file_path)
        
    def find_most_similar_company(self, query):
        if self.company_df is None:
            raise ValueError("Company data has not been loaded.")
        
        combined_texts = [query] + self.company_df['Name'].tolist()
        
        tfidf_matrix = self.vectorizer.fit_transform(combined_texts)
        
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        most_similar_idx = cosine_similarities.argmax()
        
        most_similar_company = self.company_df.iloc[most_similar_idx]['Name']
        most_similar_ticker = self.company_df.iloc[most_similar_idx]['Ticker']
        return most_similar_company, most_similar_ticker

class ConversationManager:
    def __init__(self):
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_payload(self) -> Dict[str, Any]:
        return {
            'messages': self.history,
            'topP': 0.8,
            'topK': 0,
            # 'maxTokens': 256,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

# # Example usage
# if __name__ == "__main__":
#     file_path = "company_data.xlsx"  # Replace with your actual xlsx file path
#     finder = StockTickerFinder()
#     finder.load_company_data(file_path)
#     query = "애플에 투자할까?"
#     company_name, ticker = finder.find_most_similar_company(query)
#     print(f"The most similar company is: {company_name} with ticker: {ticker}")


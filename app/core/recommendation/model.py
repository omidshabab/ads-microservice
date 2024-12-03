import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Tuple
import json

class RecommenderModel(nn.Module):
    def __init__(self, n_users: int, n_items: int, embedding_dim: int):
        super().__init__()
        self.user_embeddings = nn.Embedding(n_users, embedding_dim)
        self.item_embeddings = nn.Embedding(n_items, embedding_dim)
        self.user_bias = nn.Embedding(n_users, 1)
        self.item_bias = nn.Embedding(n_items, 1)
        
    def forward(self, user_ids: torch.Tensor, item_ids: torch.Tensor) -> torch.Tensor:
        user_embeds = self.user_embeddings(user_ids)
        item_embeds = self.item_embeddings(item_ids)
        user_bias = self.user_bias(user_ids).squeeze()
        item_bias = self.item_bias(item_ids).squeeze()
        
        dot_product = torch.sum(user_embeds * item_embeds, dim=1)
        return dot_product + user_bias + item_bias

class AdsRecommender:
    def __init__(self, embedding_size: int = 64):
        self.embedding_size = embedding_size
        self.model = None
        self.user_map = {}
        self.item_map = {}
        
    def _prepare_data(self, interactions: List[Tuple[int, int, float]]) -> torch.Tensor:
        users, items, ratings = zip(*interactions)
        return (
            torch.LongTensor(users),
            torch.LongTensor(items),
            torch.FloatTensor(ratings)
        )
    
    def train(self, interactions: List[Tuple[int, int, float]], epochs: int = 10):
        # Map users and items to consecutive indices
        unique_users = sorted(set(user for user, _, _ in interactions))
        unique_items = sorted(set(item for _, item, _ in interactions))
        
        self.user_map = {user: idx for idx, user in enumerate(unique_users)}
        self.item_map = {item: idx for idx, item in enumerate(unique_items)}
        
        # Initialize model
        self.model = RecommenderModel(
            n_users=len(self.user_map),
            n_items=len(self.item_map),
            embedding_dim=self.embedding_size
        )
        
        # Prepare data
        mapped_interactions = [
            (self.user_map[user], self.item_map[item], rating)
            for user, item, rating in interactions
        ]
        users, items, ratings = self._prepare_data(mapped_interactions)
        
        # Training loop
        optimizer = optim.Adam(self.model.parameters())
        criterion = nn.MSELoss()
        
        for epoch in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            
            predictions = self.model(users, items)
            loss = criterion(predictions, ratings)
            
            loss.backward()
            optimizer.step()
    
    def get_user_embedding(self, user_id: int) -> np.ndarray:
        if user_id not in self.user_map:
            return np.zeros(self.embedding_size)
        
        with torch.no_grad():
            user_idx = torch.LongTensor([self.user_map[user_id]])
            embedding = self.model.user_embeddings(user_idx)
            return embedding.numpy().squeeze()
    
    def get_item_embedding(self, item_id: int) -> np.ndarray:
        if item_id not in self.item_map:
            return np.zeros(self.embedding_size)
        
        with torch.no_grad():
            item_idx = torch.LongTensor([self.item_map[item_id]])
            embedding = self.model.item_embeddings(item_idx)
            return embedding.numpy().squeeze()
    
    def recommend(self, user_id: int, item_ids: List[int], top_k: int = 10) -> List[Tuple[int, float]]:
        user_embedding = self.get_user_embedding(user_id)
        item_embeddings = np.vstack([self.get_item_embedding(item_id) for item_id in item_ids])
        
        # Calculate similarities
        similarities = cosine_similarity([user_embedding], item_embeddings)[0]
        
        # Get top-k recommendations
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        recommendations = [(item_ids[idx], similarities[idx]) for idx in top_indices]
        
        return recommendations

    def save_embeddings(self, user_id: int) -> str:
        embedding = self.get_user_embedding(user_id)
        return json.dumps(embedding.tolist())
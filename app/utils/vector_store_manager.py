from typing import List, Dict, Any
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PDFLoader,
    CSVLoader,
    JSONLoader
)
import os
from pathlib import Path
import json
import pickle
import streamlit as st

class VectorStoreManager:
    """Gestionnaire de base de données vectorielle pour le RAG"""
    
    def __init__(self, embedding_model="text-embedding-ada-002"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store_path = Path("data/vector_store")
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
    
    def load_documents(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Charge et prétraite les documents"""
        documents = []
        
        for file_path in file_paths:
            file_extension = Path(file_path).suffix.lower()
            
            try:
                if file_extension == '.txt':
                    loader = TextLoader(file_path)
                elif file_extension == '.pdf':
                    loader = PDFLoader(file_path)
                elif file_extension == '.csv':
                    loader = CSVLoader(file_path)
                elif file_extension == '.json':
                    loader = JSONLoader(
                        file_path,
                        jq_schema='.[]',
                        text_content=False
                    )
                else:
                    continue
                
                doc = loader.load()
                documents.extend(doc)
                
            except Exception as e:
                print(f"Erreur lors du chargement de {file_path}: {str(e)}")
        
        return self.text_splitter.split_documents(documents)
    
    def create_vector_store(self, documents: List[Dict[str, Any]], store_name: str):
        """Crée une nouvelle base de données vectorielle"""
        try:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            self.save_vector_store(store_name)
            return True
        except Exception as e:
            print(f"Erreur lors de la création du vector store: {str(e)}")
            return False
    
    def save_vector_store(self, store_name: str):
        """Sauvegarde la base de données vectorielle"""
        if self.vector_store:
            store_path = self.vector_store_path / f"{store_name}.pkl"
            with open(store_path, "wb") as f:
                pickle.dump(self.vector_store, f)
    
    def load_vector_store(self, store_name: str) -> bool:
        """Charge une base de données vectorielle existante"""
        store_path = self.vector_store_path / f"{store_name}.pkl"
        if store_path.exists():
            try:
                with open(store_path, "rb") as f:
                    self.vector_store = pickle.load(f)
                return True
            except Exception as e:
                print(f"Erreur lors du chargement du vector store: {str(e)}")
        return False
    
    def similarity_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Effectue une recherche par similarité"""
        if not self.vector_store:
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                }
                for doc, score in results
            ]
        except Exception as e:
            print(f"Erreur lors de la recherche: {str(e)}")
            return []
    
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """Ajoute de nouveaux textes à la base existante"""
        try:
            if not self.vector_store:
                documents = self.text_splitter.create_documents(texts, metadatas)
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                self.vector_store.add_texts(texts, metadatas)
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de textes: {str(e)}")
            return False
    
    def delete_vector_store(self, store_name: str) -> bool:
        """Supprime une base de données vectorielle"""
        store_path = self.vector_store_path / f"{store_name}.pkl"
        try:
            if store_path.exists():
                store_path.unlink()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du vector store: {str(e)}")
            return False
    
    def create_empty_vector_store(self, store_name: str):
        """
        Crée une base de connaissances vectorielle vide
        
        Args:
            store_name (str): Nom de la base de connaissances
        """
        try:
            # Créer un FAISS vide avec les embeddings
            empty_docs = []
            empty_vectors = self.embeddings.embed_documents(["Aucun document"])
            
            # Créer un nouveau store vide
            self.vector_store = FAISS.from_embeddings(
                text_embeddings=list(zip(["Aucun document"], empty_vectors)),
                embedding=self.embeddings
            )
            
            # Sauvegarder le store vide
            store_path = self.vector_store_path / f"{store_name}.index"
            self.vector_store.save_local(str(store_path))
            
            st.info(f"Base de connaissances vide '{store_name}' créée avec succès.")
        
        except Exception as e:
            st.error(f"Erreur lors de la création de la base de connaissances vide : {str(e)}")
            raise

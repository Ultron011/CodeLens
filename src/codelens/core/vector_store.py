import chromadb
from chromadb.utils import embedding_functions

class VectorMemory:
    def __init__(self, db_path="./.codelens_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        
        self.collection = self.client.get_or_create_collection(
            name="code_chunks",
            metadata={"hnsw:space": "cosine"}
        )
        
    def add_chunk(self, content: str, metadata: dict, chunk_id: str):
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[chunk_id]
        )

    def add_chunks(self, contents: list[str], metadatas: list[dict], ids: list[str]):
        """Batch add chunks to the collection"""
        self.collection.add(
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )

    def clear_all(self):
        """Deletes the collection and recreates it"""
        try:
            self.client.delete_collection("code_chunks")
            self.collection = self.client.get_or_create_collection(
                name="code_chunks",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            console.print(f"[bold red]Error clearing DB: {e}[/bold red]")       
             
    def search(self, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

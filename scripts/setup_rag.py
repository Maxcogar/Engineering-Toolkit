#!/usr/bin/env python3
"""
RAG System Setup for Gas Turbine Knowledge Base

Sets up vector database and indexing for all reference PDFs.
Enables semantic search across technical documentation.
"""

import os
import sys
from pathlib import Path

try:
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
    from llama_index.vector_stores.chroma import ChromaVectorStore
    from llama_index.core import Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    import chromadb
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install llama-index llama-index-vector-stores-chroma chromadb sentence-transformers")
    sys.exit(1)


def setup_knowledge_base(docs_path="docs/reference", db_path="./chroma_db"):
    """
    Initialize RAG system with reference PDFs

    Args:
        docs_path: Path to reference documentation
        db_path: Path to vector database storage

    Returns:
        VectorStoreIndex: The created index
    """

    print(f"Loading documents from {docs_path}...")

    # Check if docs directory exists
    if not os.path.exists(docs_path):
        print(f"ERROR: Documentation directory not found: {docs_path}")
        sys.exit(1)

    # Load documents (PDFs and markdown)
    try:
        documents = SimpleDirectoryReader(
            docs_path,
            recursive=True,
            required_exts=[".pdf", ".md"]
        ).load_data()

        print(f"Loaded {len(documents)} documents")

    except Exception as e:
        print(f"ERROR loading documents: {e}")
        sys.exit(1)

    # Set up embedding model
    print("Setting up embedding model...")
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create vector store
    print(f"Creating vector database at {db_path}...")
    chroma_client = chromadb.PersistentClient(path=db_path)

    # Delete existing collection if it exists (for fresh rebuild)
    try:
        chroma_client.delete_collection("gas_turbine_knowledge")
        print("Deleted existing collection")
    except:
        pass

    chroma_collection = chroma_client.create_collection("gas_turbine_knowledge")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create index
    print("Building vector index (this may take a few minutes)...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )

    print(f"\nKnowledge base created successfully!")
    print(f"Vector database: {db_path}")
    print(f"Documents indexed: {len(documents)}")

    return index


def query_knowledge_base(query, db_path="./chroma_db", top_k=5):
    """
    Query the knowledge base

    Args:
        query: Search query
        db_path: Path to vector database
        top_k: Number of results to return

    Returns:
        Query response with sources
    """
    from llama_index.core.llms import MockLLM

    # Load existing index
    chroma_client = chromadb.PersistentClient(path=db_path)
    chroma_collection = chroma_client.get_collection("gas_turbine_knowledge")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Set embedding model and LLM
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Use MockLLM to avoid needing OpenAI API key
    # This returns chunks without synthesis
    Settings.llm = MockLLM(max_tokens=256)

    index = VectorStoreIndex.from_vector_store(vector_store)

    # Use retriever instead of query engine for raw chunks
    retriever = index.as_retriever(similarity_top_k=top_k)

    nodes = retriever.retrieve(query)

    # Create a simple response object
    class SimpleResponse:
        def __init__(self, nodes):
            self.source_nodes = nodes
            # Create response text from nodes
            self.response = "\n\n".join([
                f"[From {node.metadata.get('file_name', 'Unknown')}]\n{node.text[:500]}..."
                for node in nodes[:3]
            ])

    return SimpleResponse(nodes)


def main():
    """Main entry point for RAG setup"""

    import argparse

    parser = argparse.ArgumentParser(description="Setup and query gas turbine knowledge base")
    parser.add_argument("--setup", action="store_true", help="Set up knowledge base from PDFs")
    parser.add_argument("--query", type=str, help="Query the knowledge base")
    parser.add_argument("--docs", default="docs/reference", help="Path to documentation")
    parser.add_argument("--db", default="./chroma_db", help="Path to vector database")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")

    args = parser.parse_args()

    if args.setup:
        # Set up knowledge base
        setup_knowledge_base(args.docs, args.db)

    elif args.query:
        # Query knowledge base
        print(f"Querying: {args.query}\n")

        response = query_knowledge_base(args.query, args.db, args.top_k)

        print("=" * 80)
        print("RESPONSE:")
        print("=" * 80)
        print(response.response)
        print("\n" + "=" * 80)
        print("SOURCES:")
        print("=" * 80)

        for i, node in enumerate(response.source_nodes, 1):
            metadata = node.metadata
            file_name = metadata.get('file_name', 'Unknown')
            page = metadata.get('page_label', metadata.get('page', 'N/A'))

            print(f"\n[{i}] {file_name} (page {page})")
            print(f"    Score: {node.score:.3f}")
            print(f"    Excerpt: {node.text[:200]}...")

    else:
        print("Please specify --setup or --query")
        parser.print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
RAG Query Tool for Gas Turbine Knowledge Base

Quick interface for querying reference documentation.
"""

import sys
from setup_rag import query_knowledge_base


def query_system(system_name, aspect="all information", top_k=10):
    """
    Query knowledge base for specific system and aspect

    Args:
        system_name: System to query (combustor, fuel-system, etc.)
        aspect: What to find (geometry, constraints, design, etc.)
        top_k: Number of results

    Returns:
        Formatted response with sources
    """

    # Construct query
    query = f"For the {system_name} system in a small gas turbine: {aspect}"

    print(f"Querying knowledge base...")
    print(f"System: {system_name}")
    print(f"Aspect: {aspect}\n")

    response = query_knowledge_base(query, top_k=top_k)

    return response


def main():
    if len(sys.argv) < 2:
        print("Usage: python rag_query.py <system> [aspect] [top_k]")
        print("\nExamples:")
        print("  python rag_query.py combustor")
        print("  python rag_query.py combustor 'geometry and air flow'")
        print("  python rag_query.py fuel-system 'atomization and spray characteristics' 15")
        sys.exit(1)

    system_name = sys.argv[1]
    aspect = sys.argv[2] if len(sys.argv) > 2 else "all information"
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    response = query_system(system_name, aspect, top_k)

    print("=" * 80)
    print("KNOWLEDGE BASE RESPONSE:")
    print("=" * 80)
    print(response.response)
    print("\n" + "=" * 80)
    print("SOURCES (read these for detailed information):")
    print("=" * 80)

    for i, node in enumerate(response.source_nodes, 1):
        metadata = node.metadata
        file_name = metadata.get('file_name', 'Unknown')
        page = metadata.get('page_label', metadata.get('page', 'N/A'))

        print(f"\n[{i}] {file_name}")
        if page != 'N/A':
            print(f"    Page: {page}")
        print(f"    Relevance: {node.score:.3f}")
        print(f"    Content preview:")
        print(f"    {node.text[:300]}...")
        print()

    print("=" * 80)
    print(f"\nNext step: Read the cited pages in the source PDFs for complete information.")


if __name__ == "__main__":
    main()

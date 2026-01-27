# Reference Materials

External documentation, PDFs, datasheets, and specifications.

## Adding References

1. Place PDF files directly in this folder
2. For RAG indexing, run: `python scripts/setup_rag.py --setup`

## Organization

- Datasheets: `component-name-datasheet.pdf`
- Specifications: `spec-name.pdf`
- Books/Guides: Descriptive filename

## RAG Integration

After adding PDFs, update the RAG index:
```bash
python scripts/setup_rag.py --setup
```

Query the knowledge base:
```bash
python scripts/rag_query.py "your question"
```

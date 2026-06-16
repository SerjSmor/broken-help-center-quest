from app.retrieval import LexicalRetriever


def test_lexical_retriever_returns_matching_document_first():
    retriever = LexicalRetriever(
        [
            {
                "id": "doc_domain",
                "title": "Connecting a domain",
                "url": "/help/connect-domain",
                "body": "Update DNS records at your provider to connect a domain.",
            },
            {
                "id": "doc_blog",
                "title": "Writing a blog post",
                "url": "/help/blog",
                "body": "Open the blog manager and publish a post.",
            },
        ]
    )

    results = retriever.search("How do I connect my domain DNS?", top_k=1)

    assert len(results) == 1
    assert results[0].id == "doc_domain"
    assert results[0].score > 0

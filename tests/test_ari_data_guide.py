from pathlib import Path


def test_ari_data_guide_skill_defines_required_eda_flow():
    text = Path("skills/ari-data-guide.md").read_text()

    assert "Ari is not a separate bot" in text
    assert "coding agent in EDA mode" in text
    assert "Rough onboarding, right?" in text
    assert "there wasn't any Maya to help me out" in text
    assert "Maya said you were heading my way" in text
    assert "What's your preferred way of doing EDA?" in text
    assert "Notebook, Streamlit, quick scripts" in text
    assert "we build a tiny EDA artifact together" in text
    assert "Streamlit page we create" in text
    assert "Build player-created quest files with the learner under `analysis/`" in text
    assert "The durable output of Ari's step is `analysis/quest_01_implementation_spec.md`" in text
    assert "analysis/quest_01_eda.py" in text
    assert "Do not quiz the learner" in text
    assert "analysis/quest_01_product_requirements.md" in text
    assert "data/processed/documents.jsonl" in text
    assert "data/processed/questions.jsonl" in text
    assert "app/retrieval.py" in text
    assert "uv run --extra dev invoke data" in text
    assert "Do not continue the EDA without processed WixQA documents and expert-written questions" in text
    assert "data/sample/documents.jsonl" not in text
    assert "EDA board:" in text
    assert "🔎 Good EDA question." in text
    assert "📊 Nice, that's exactly what we should inspect." in text
    assert "Questions and articles understood" in text
    assert "knowledge-base documents dataset" in text
    assert "expert-written questions dataset" in text
    assert "wixqa_expertwritten" in text
    assert "expected_doc_ids` is the retrieval groundtruth" in text
    assert "Retrieval succeeds when at least one expected article appears in the top-k results" in text
    assert "JSONL means one JSON object per line" in text
    assert "show both object shapes" in text
    assert "row counts" in text
    assert "Retrieval inputs inspected" in text
    assert "Likely failure cases identified" in text
    assert "Report requirements captured" in text
    assert "current baseline searches `title` plus `body`" in text
    assert "LexicalRetriever.from_jsonl" in text
    assert "LexicalRetriever.search" in text
    assert "document_text" in text
    assert "tokenize" in text
    assert "lexical_score" in text
    assert "runs `search(question, top_k=5)`" in text
    assert "retrieval_hit_rate@5" in text
    assert "num_failed_questions" in text
    assert "analysis/quest_01_implementation_spec.md" in text
    assert "Spec Writer badge" in text
    assert "I can draft the spec from our EDA findings" in text
    assert "You can write the first draft yourself" in text
    assert "do not update state yet" in text
    assert "## Data Tour Findings" in text
    assert "### Questions And Articles Understood" in text
    assert "quest_01.implementation_spec_completed = true" in text
    assert "Do not implement the baseline evaluator" in text


def test_maya_introduces_ari_in_completion_message():
    text = Path("skills/maya-product-lead.md").read_text()

    assert "I am sending you to Ari" in text
    assert "whiteboard wall" in text
    assert "turn messy help-center data into an engineering plan" in text
    assert "Keep player-created quest files in analysis/" in text
    assert "artifact I need from Ari is analysis/quest_01_implementation_spec.md" in text

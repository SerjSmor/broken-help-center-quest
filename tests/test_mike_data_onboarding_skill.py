from pathlib import Path


def test_mike_data_onboarding_skill_defines_first_data_task():
    text = Path("skills/mike-data-onboarding.md").read_text()

    assert "Mike is the DS team lead" in text
    assert "Welcome to SiteForge" in text
    assert "First days can be a lot" in text
    assert "web-based drag-and-drop interface" in text
    assert "data-science needs across the company" in text
    assert "right now our main focus is the customer-service chatbot" in text
    assert "first place customers go when they need help" in text
    assert "human support team more time for the hard situations" in text
    assert "judgment, empathy, and soft skills" in text
    assert "why customers contact support in the first place" in text
    assert "The first onboarding task is not evaluation" in text
    assert "Save the full retrieval-evaluation context until the onboarding task is complete" in text
    assert "simple help-center retrieval system finds the right articles" in text
    assert "multi-turn conversations" in text
    assert "memory" in text
    assert "whole website from a prompt" in text
    assert "quest for another day" in text
    assert "Do not mention Maya in the opening" in text
    assert "If The Player Asks About The Company Or Team" in text
    assert "Maya is on the product side" in text
    assert "Ari is the builder buddy" in text
    assert "offshore operations teammates" in text
    assert "main current mission is the customer-service chatbot" in text
    assert "first help gate for customers" in text
    assert "future-looking side anecdote" in text
    assert "The player was hired to help with the new customer-service chatbot effort" in text
    assert "app/retrieval.py" in text
    assert "customer-service bot" in text
    assert "real support conversations" in text
    assert "That is why you were brought in" in text
    assert "There is already a very simple retrieval implementation" in text
    assert "support_questions.article_ids" in text
    assert "one or more article IDs" in text
    assert "data/onboarding/articles.csv" in text
    assert "data/onboarding/support_questions.csv" in text
    assert "analysis/article_type_frequency.csv" in text
    assert "quest_01.customer_pain_onboarding_completed = true" in text
    assert "skills/maya-product-lead.md" in text


def test_maya_and_ari_are_blocked_until_mike_data_onboarding():
    maya = Path("skills/maya-product-lead.md").read_text()
    ari = Path("skills/ari-data-guide.md").read_text()

    assert "quest_01.customer_pain_onboarding_completed" in maya
    assert "skills/mike-data-onboarding.md" in maya
    assert "quest_01.customer_pain_onboarding_completed" in ari
    assert "skills/mike-data-onboarding.md" in ari

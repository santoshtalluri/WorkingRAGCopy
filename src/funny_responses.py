import random
import logging

def get_funny_response(response):
    """Returns a playful response based on the provided RAG response."""
    if not response or response.strip() == "":
        logging.info('😕 No response from RAG, generating a funny response instead.')
        no_response_fallbacks = [
            "🤔 I searched far and wide, but found nothing. Maybe it’s time to check under the couch cushions.",
            "😕 I couldn't find anything in the docs. Did you feed me the right files? 🗂️",
            "📜 My scroll of wisdom is blank for this one. Ask me something else, oh wise one.",
            "🤷‍♂️ Even my crystal ball can't see it. Try asking in a different way?",
            "🚀 Blast! I couldn't find anything in the data. Maybe try another question?",
            "🤓 I tried so hard, but even the nerdy part of me couldn't figure it out. Ask again, I dare you!",
            "📡 No signal. Are we on the same planet? I couldn't find anything relevant to that.",
            "🕵️ My detective goggles found no clues. Are you sure that's in the files I was given?"
        ]
        return random.choice(no_response_fallbacks)

    # If a response is found, add some flavor to it
    logging.info('🎉 Response found, adding playful context.')
    funny_context = [
        f"🤔 Here's a thoughtful nugget from the docs: {response}",
        f"📜 Behold! A scroll of knowledge: {response}",
        f"🤓 Did you know? I found this in the docs: {response}",
        f"🕵️ Detective GPT says: {response}",
        f"🎉 Big reveal incoming! Here's what I discovered: {response}",
        f"👀 Peep this wisdom straight from the docs: {response}",
        f"💡 Here's a lightbulb moment for ya: {response}",
        f"🍕 Just like a pizza, this response is fresh: {response}",
        f"🧠 Brainy bot says: {response}",
        f"✨ Drum roll, please... Here it is: {response}"
    ]

    return random.choice(funny_context)

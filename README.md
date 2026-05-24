# Text to JSON

A Python tool that turns free-text about a person into structured, validated JSON using an LLM.

## What it does

Takes unstructured text (e.g. "John Smith is 42 and works as an engineer in Manchester") and extracts it into clean, validated JSON. Missing details are handled gracefully rather than causing errors.

## Tech

- Python
- OpenAI API (gpt-4o-mini)
- Pydantic (validation)
- python-dotenv (key management)

## Setup & run

```bash
git clone https://github.com/dlnicks/text-json.git
cd text-json
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project folder with your OpenAI key:

```
OPENAI_API_KEY=your-key-here
```

Then run:

```bash
python main.py
```

## How it works

A system prompt puts the model in JSON mode, so it returns structured JSON instead of prose. That JSON is then validated against a Pydantic schema, which checks the fields and types. Optional fields let missing data return as `null` instead of crashing, and a try/except block catches any validation failures so the program fails gracefully.

An LLM is used here because the input is free-form text with unpredictable phrasing — something rigid rules (like regex) can't handle. For fixed, structured input, simpler parsing would be the better choice.

## What I'd improve

- **Batch processing.** Currently handles one input at a time; it could accept a file or list and extract from many at once.
- **Configurable schema.** The fields to extract are hardcoded — letting the user define their own schema would make it reusable for any data type.

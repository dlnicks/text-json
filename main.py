from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI()


class Person(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None
    location: Optional[str] = None


def extract_person(text):
    """Take any text, extract person details, return a validated Person (or None if it fails)."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a data extraction tool. Extract the person's details and return them as JSON with keys: name, age, occupation, location. Use null for anything not mentioned."},
            {"role": "user", "content": text}
        ]
    )
    raw = response.choices[0].message.content

    try:
        return Person.model_validate_json(raw)
    except Exception as e:
        print(f"Validation failed: {e}")
        return None


# --- run it ---
user_text = input("Paste some text about a person: ")
person = extract_person(user_text)

if person:
    print(person)


import json
from functools import cache

from groq import NOT_GIVEN, BadRequestError, Groq

from src.config import GROQ_API_KEY

model = ["llama-3.1-8b-instant", "llama3-70b-8192"][1]


@cache
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)


def ask_groq(query_text: str, system_content: str, json_schema: dict = None) -> dict:
    client = get_groq_client()
    response_format = NOT_GIVEN
    if json_schema:
        system_content = f"{system_content}\n Use this json schema to reply {json.dumps(json_schema)}"
        response_format = {"type": "json_object"}
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_content}, {"role": "user", "content": query_text}],
            model=model,
            response_format=response_format,
        )
        json_str = chat_completion.choices[0].message.content
        json_str = json_str.strip()
    except BadRequestError as e:
        failed_json = e.body["error"]["failed_generation"]  # noqa
        json_str = failed_json.replace('"""', '"').replace("\n", "\\n")
    if not json_schema:
        return json_str
    try:
        # json_str = re.sub("\n +", "", json_str)
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(e.doc.encode(), e.pos)
        print(f"ERROR : {e.args}")
        return {"suggestions": ["..."]}


def find_typos(query_text):
    system_content = (
        "You are a proofreading expert. Check for mistakes in spellings, casing of proper nouns"
        " and list mistakes (if any) along with suggestion, not fixes."
        "Keep it short, no explanation. Do not modify urls, usernames and hashtags."
    )
    ans = ask_groq(query_text, system_content, json_schema={"suggestions": ["str"]})
    return ans["suggestions"]


def fix_typos(query_text):
    system_content = (
        "You are a proofreading expert. Check for mistakes in spellings and answer only exact correct text "
        "without any additional info like headings, footers, etc."
        "Do not modify urls, usernames and hashtags. `~~~` is a phrase seperator, keep it as it is."
    )
    return ask_groq(query_text, system_content)


if __name__ == "__main__":
    from dotenv import load_dotenv  # noqa

    load_dotenv()
    answer = ask_groq("Debuging is hard.")  # noqa
    print(answer)

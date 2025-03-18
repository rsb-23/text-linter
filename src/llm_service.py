import json

from litellm import completion

from src.config import LLM_MODEL, PROVIDER


def ask_llm(query_text: str, system_content: str, json_schema: dict = None, provider=PROVIDER) -> dict:
    response_format = None
    if json_schema:
        system_content = f"{system_content}\n Use this json schema to reply {json.dumps(json_schema)}"
        response_format = {"type": "json_object"}
    try:
        # Send a message to the model
        response = completion(
            model=f"{provider}/{LLM_MODEL}",
            messages=[{"role": "system", "content": system_content}, {"role": "user", "content": query_text}],
            response_format=response_format,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        failed_json = e.body["error"]["failed_generation"]  # noqa
        json_str = failed_json.replace('"""', '"').replace("\n", "\\n")
    if not json_schema:
        return json_str
    try:
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
    ans = ask_llm(query_text, system_content, json_schema={"suggestions": ["str"]})
    return ans["suggestions"]


def fix_typos(query_text):
    system_content = (
        "You are a proofreading expert. Check for mistakes in spellings and answer only exact correct text "
        "without any additional info like headings, footers, etc."
        "Do not modify urls, usernames and hashtags. `~~~` is a phrase seperator, keep it as it is."
    )
    return ask_llm(query_text, system_content)


if __name__ == "__main__":
    from dotenv import load_dotenv  # noqa

    load_dotenv()
    answer = ask_llm("Debuging is hard.", system_content="")
    print(f"Response from model: {answer}")

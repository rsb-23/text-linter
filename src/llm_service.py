import json

from litellm import BadRequestError, completion, validate_environment

from src.config import LLM_API_KEY, LLM_MODEL, PROVIDER


def validate_model(provider: str = PROVIDER, model: str = LLM_MODEL) -> None:
    model_str = f"{provider}/{model}"
    assert not validate_environment(model_str)["keys_in_environment"], f"Invalid value : {model}"


def ask_llm(query_text: str, system_content: str, json_schema: dict = None, provider=PROVIDER) -> dict:
    response_format = None
    if json_schema:
        system_content = f"{system_content}\n Use this json schema to reply {json.dumps(json_schema)}"
        response_format = {"type": "json_object"}
    try:
        # Send a message to the model
        print("calling llm...")
        response = completion(
            model=f"{provider}/{LLM_MODEL}",
            api_key=LLM_API_KEY,
            messages=[{"role": "system", "content": system_content}, {"role": "user", "content": query_text}],
            response_format=response_format,
        )
        json_str = response["choices"][0]["message"]["content"]
    except BadRequestError as e:
        json_str = e.message  # reusing variable for showing error

    if json_str.startswith("litellm"):
        raise RuntimeError(json_str)

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

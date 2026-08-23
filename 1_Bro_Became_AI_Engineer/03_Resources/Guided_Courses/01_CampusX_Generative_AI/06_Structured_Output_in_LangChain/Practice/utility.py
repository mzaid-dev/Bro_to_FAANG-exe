def get_structured_output(llm, schema, prompt):
    try:
        structured_llm = llm.with_structured_output(
            schema,
            method = 'json_mode'
        )
        result = structured_llm.invoke(prompt)
        return result

    except (NotImplementedError, ValueError) as e:
        print(f"Structured output not supported: {e}")
        return None
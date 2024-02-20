def process_body_result(body: dict) -> dict[str, str]:
    values_of_interest = {}
    for _, value in body["view"]["state"]["values"].items():
        for nested_key, nested_value in value.items():
            new_value = (
                nested_value["value"]
                if "value" in nested_value
                else [nested_value["selected_option"]["value"]]
            )
            values_of_interest[nested_key] = new_value
    return values_of_interest

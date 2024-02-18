def process_body_result(body: dict) -> dict[str, str]:
    values_of_interest = {}
    for _, value in body["view"]["state"]["values"].items():
        for nested_key, nested_value in value.items():
            values_of_interest[nested_key] = nested_value["value"]
    return values_of_interest

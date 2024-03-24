base_url = "https://lelabquantique.com"


class WordPressPostStatus:
    DRAFT = "draft"
    PUBLISHED = "publish"
    PENDING_REVIEW = "pending review"


def camel_to_snake(json_data):
    if isinstance(json_data, dict):
        new_dict = {}
        for key, value in json_data.items():
            new_key = "".join(["_" + i.lower() if i.isupper() else i for i in key])
            new_dict[new_key.lstrip("_")] = camel_to_snake(value)
        return new_dict
    elif isinstance(json_data, list):
        return [camel_to_snake(item) for item in json_data]
    else:
        return json_data

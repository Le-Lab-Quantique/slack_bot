import requests

from src.llq_website.utils import base_url

query = """
query partner ($id:ID!) {
    partner(id:$id) {
        partners {
          partnerName
          partnerLogo {
            node {
              databaseId
            }
          }
        }
    }
}
"""
url = f"{base_url}/graphql"


def get_partners_by_id(partner_id: str):
    variables = {
        "id": "".join(partner_id),
    }
    response = requests.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        data = response.json()
        return data["data"]["partner"]["partners"]
    else:
        print("Error:", response.status_code)
        print(response.text)

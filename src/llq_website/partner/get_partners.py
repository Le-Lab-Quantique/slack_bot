import requests
import json

from src.llq_website.utils import base_url

# Define your GraphQL query
query = """
query partners (
  $first:Int, 
  $last:Int, 
  $before:String, 
  $after:String, 
  $where:RootQueryToPartnerConnectionWhereArgs
  ) {
  	partners(
      first:$first, 
      last:$last, 
      before:$before, 
      after:$after, 
      where:$where
    ) {
      nodes {
        id
        partners {
          partnerName
          partnerLogo {
            node {
              databaseId
              mediaItemUrl
            }
          }
        }
      }
    }
}
"""

# Define your variables
variables = {
    "first": 60,  # Number of items to retrieve
}

# Define your endpoint URL
url = f"{base_url}/graphql"

# Make the request
response = requests.post(url, json={"query": query, "variables": variables})


def get_partners():
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(
            json.dumps(data, indent=2)
        )  # Print the response data in a readable format
        return data["data"]["partners"]["nodes"]
    else:
        print("Error:", response.status_code)
        print(response.text)  # Print the error message if request fails

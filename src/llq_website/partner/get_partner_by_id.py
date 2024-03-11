from src.llq_website.client.graphql_client import GraphQLClient
from dataclasses import dataclass

from typing import Optional


@dataclass
class PartnerWithLogo:
    name: str
    database_id: int
    media_item_url: str
    alt_text: Optional[str]


query = """
query partner ($id:ID!) {
    partner(id:$id) {
        partners {
          partnerName
          partnerLogo {
            node {
              databaseId
              mediaItemUrl
              altText
            }
          }
        }
    }
}
"""


def get_partners_by_id(partner_id: str) -> PartnerWithLogo:
    variables = {
        "id": "".join(partner_id),
    }
    data = GraphQLClient(variables=variables, query=query).get()
    partner = data["data"]["partner"]["partners"]
    partner_name = partner.get("partnerName", "")
    partner_logo_node = partner.get("partnerLogo", {}).get("node", {})
    partner_image_database_id = partner_logo_node.get("databaseId", 0)
    partner_media_item_url = partner_logo_node.get("mediaItemUrl", "")
    partner_alt_text = partner_logo_node.get("altText", "")

    return PartnerWithLogo(
        name=partner_name,
        database_id=partner_image_database_id,
        media_item_url=partner_media_item_url,
        alt_text=partner_alt_text,
    )

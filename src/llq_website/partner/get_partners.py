from src.llq_website.client.graphql_client import GraphQLClient

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

variables = {
    "first": 60,
}


def get_partners():
    data = GraphQLClient(varaibles=variables, query=query).get()
    return data["data"]["partners"]["nodes"]

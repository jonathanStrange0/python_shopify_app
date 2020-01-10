import shopify as sfy
import json

def get_orders():
    orders = '''
                    {
                      draftOrders(first: 10, reverse: true) {
                        edges {
                          node {
                            id
                            createdAt
                            metafields(first:10, namespace:"testing date") {
                              edges {
                                node {
                                    key
                                    value
                                }
                              }
                            }
                          }
                        }
                      }
                    }
            '''
    # pprint(order_mutation)
    # shop_session = sfy.Session(shop_url, '2019-04', shop_token)
    # activate the shopify session to use resources.
    # sfy.ShopifyResource.activate_session(shop_session)
    client = sfy.GraphQL()
    return json.loads(client.execute(orders))
    # print(result)

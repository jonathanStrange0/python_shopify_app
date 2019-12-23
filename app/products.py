import shopify as sfy
import json, random

def upload_product_data(prod_name, max_variants=10):
    """
        Upload a single product to the shop
        input:
         - prod_name: name for the fake name creation
         - max_variants: maximum number of variants to allow this product to have
        returns:
         - graphQL post result containint the product id, shop id, and any errors
    """
    
    product_mutation = '''mutation {
                                    productCreate(input: {
                                        descriptionHtml: "test product generated via GraphQL",
                                        title: "'''+prod_name+'''"
                                        }
                                    )
                                    {
                                        product{
                                            id
                                        }
                                        shop {
                                            id
                                        }
                                        userErrors{
                                            field
                                            message
                                        }
                                    }
                            }

                        '''
    print(sfy.ShopifyResource.get_site())
    client = sfy.GraphQL()
    product_results = json.loads(client.execute(product_mutation))
    # print(product_results)
    pid = product_results['data']['productCreate']['product']['id']
    for v in range(random.randint(0,max_variants)):
        generate_fake_variant(pid,"Variant Test generate with GraphQL {}".format(v),\
                                    "variant: {}".format(v), "6.69", "2.38")
    return product_results

def generate_fake_variant(producId, option, variant_sku, variant_price, variant_cost):
    """
        Upload a single product to the shop
    """
    variant_mutation = '''mutation {
                                productVariantCreate(input: {
                                        productId: "'''+producId+'''",
                                        options: "'''+option+'''",
                                        price:"'''+variant_price+'''",
                                        sku: "'''+variant_sku+'''",
                                        inventoryItem: {
                                            cost: "'''+variant_cost+'''"
                                        }

                                    })
                                    {
                                        product{
                                            id
                                        }
                                        productVariant{
                                            id
                                        }
                                        userErrors{
                                            field
                                            message
                                        }
                                    }
                            }

                        '''
    client = sfy.GraphQL()
    result = client.execute(variant_mutation)
    return result

def create_fake_products_and_variants(num_prod, max_variants):
    prod_name_list = ['Test Product Num: {}'.format(x) for x in\
                                                range(0,num_prod)]

    return(list(map(upload_product_data, prod_name_list, [max_variants] * num_prod)))

import shopify as sfy
import json, random

def generate_fake_customer_data(records_to_create):
    """
        function that will create lists of names based on the number of desired
        synthetic customer names required.
        input:
         - records_to_create: integer representing the desired number of fake customers
        returns:
         - first_name_list: list records_to_create in length containing synthetic customer first names
         - last_name_list: list records_to_create in length containing synthetic customer last names
    """
    # range_list = [x for x in range(0,records_to_create)]
    first_name_list = ['TC{} First Name'.format(x) for x in\
                                                range(0,records_to_create)]
    last_name_list = ['TC{} Last Name'.format(x) for x in\
                                                range(0,records_to_create)]
    return first_name_list, last_name_list

def upload_customer_data(first_name, last_name):
    """
        give an first and last name, add that customer to the shopify shop
        input:
         - first_name: customer's first name
         - last_name: customer's last name
        returns:
         - result: the result of the GraphQL mutation post with the customer's
            unique id and any errors that occured.
    """
    customer = '''
                input: {
                    firstName: "''' + first_name + '''",
                    lastName: "''' + last_name + '''"
                }
                '''
    customer_mutation = '''mutation {
                                        customerCreate(''' + customer + ''')
                                            {
                                                customer {
                                                            id
                                                        }
                                                userErrors {
                                                            field message
                                                        }
                                            }
                                    }
                            '''
    client = sfy.GraphQL()
    result = client.execute(customer_mutation)
    return result

def upload_all_customers(first_name_list, last_name_list):
    """
        given lists equal in length of first and last names, apply the function
        upload_customer_data to each name pair in the list.
        input:
         - first_name_list, last_name_list list of first names, and last names
        returns:
         - the map output cast to a list.
    """
    return list(map(upload_customer_data, first_name_list, last_name_list))

def generate_fake_product_data(records_to_create):
    # description_html_list =
    pass

def upload_product_data(prod_name, max_variants):
    """
        Upload a single product to the shop
        input:
         - prod_name: name for the fake name creation
         - max_variants: maximum number of variants to allow this product to have
        returns:
         - graphQL post result containint the product id, shop id, and any errors
    """
    # product_mutation = '''mutation {
                        #             productCreate(input: {
                        #                 descriptionHtml: "test product generated via GraphQL",
                        #                 title: "A Test Product",
                        #                 variants: {
                        #                     price:"10.95",
                        #                     sku: "GQLT1",
                        #                     inventoryItem: {
                        #                         cost: "4.57"
                        #                     }
                        #                 }
                        #             })
                        #             {
                        #                 product{
                        #                     id
                        #                 }
                        #                 shop{
                        #                     id
                        #                 }
                        #                 userErrors{
                        #                     field
                        #                     message
                        #                 }
                        #             }
                        #     }
                        #
                        # '''

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
    client = sfy.GraphQL()
    product_results = json.loads(client.execute(product_mutation))
    # print(product_results)
    pid = product_results['data']['productCreate']['product']['id']
    for v in range(random.randint(0,max_variants)):
        print(v)
        print(json.loads(generate_fake_variant(pid,"Variant Test generate with GraphQL {}".format(v), "variant: {}".format(v), "6.69", "2.38")))
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


def generate_fake_order_data(records_to_create):
    pass

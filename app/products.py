import shopify as sfy
import json, random
from app.models import Product, Variant
from app import db

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
    # print(sfy.ShopifyResource.get_site())
    client = sfy.GraphQL()
    product_results = json.loads(client.execute(product_mutation))
    # print(product_results)
    pid = product_results['data']['productCreate']['product']['id']
    #add this product to the database
    prod = Product(gid = pid, name=prod_name)
    db.session.add(prod)
    db.session.commit()
    #determine number of variants
    for v in range(random.randint(0,max_variants)):
        generate_fake_variant(pid,"Variant Test generate with GraphQL {}".format(v),\
                                    "variant: {}".format(v), "6.69", "2.38")


    return product_results

def generate_fake_variant(productId, option, variant_sku, variant_price, variant_cost):
    """
        Upload a single product to the shop
    """
    variant_mutation = '''mutation {
                                productVariantCreate(input: {
                                        productId: "'''+productId+'''",
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
    # result = client.execute(variant_mutation)
    var_results = json.loads(client.execute(variant_mutation))
    # print(product_results)
    # print(var_results)
    vid = var_results['data']['productVariantCreate']['productVariant']['id']
    #upload this product's variants to the DATABASE
    var = Variant(gid = vid, name = variant_sku)
    prod = Product.query.filter_by(gid = productId).first()
    db.session.add(var)
    prod.variants.append(var)
    db.session.commit()
    return var_results

def create_fake_products_and_variants(num_prod, max_variants):
    #TODO: For new products, start the numbering sequence at the last num in database.
    num_existing_prod = len(Product.query.all())
    prod_name_list = []
    if num_existing_prod == 0:
        prod_name_list = ['Test Product Num: {}'.format(x) for x in\
                                                    range(0,num_prod)]
    else:
        prod_name_list = ['Test Product Num: {}'.format(x) for x in\
                                                    range(num_existing_prod,num_existing_prod + num_prod)]

    return(list(map(upload_product_data, prod_name_list, [max_variants] * num_prod)))

def delete_products(gid):
    product = '''
                    input: {
                        id: "''' + gid + '''"
                    }
                '''


    del_prod_mutation = '''
                            mutation {
                                productDelete(''' + product + '''){
                                    deletedProductId
                                    shop {
                                      id
                                    }
                                    userErrors {
                                      field
                                      message
                                    }
                                }
                            }
                        '''
    db.session.delete(Product.query.filter_by(gid = gid).first())
    db.session.commit()
    client = sfy.GraphQL()
    result = client.execute(del_prod_mutation)
    print('deletd product: ', gid)

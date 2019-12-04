import shopify as sfy
from dotenv import load_dotenv
from unleashed_py import Resource
import os, requests, json
# os.getenv

def upload_customer(customer_json, shopify_session):
    """
        function will take a json opject containing customer information
        and upload that customer's details to a shopify store using the GraphQL
        functionality of the Shopify_Python_API

    arguments:
        - customer_json: the json objcet with customer information
        - shopify_session: the current session you are working in
            representing the shop you are working with, and want data added to.

    returns:
        - id: the unique id of the newly created customer
    """
    first_name = str(customer_json['ContactFirstName'])
    last_name = str(customer_json['ContactLastName'])
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

def upoad_product(product_json, shopify_session):
    """
        function will take a json opject containing product information
        and upload that product's details to a shopify store using the GraphQL
        functionality of the Shopify_Python_API

    arguments:
        - product_json: the json objcet with customer information
        - shopify_session: the current session you are working in
            representing the shop you are working with, and want data added to.

    returns:
        - id: the unique id of the newly created product
    """
    descriptionHtml = '"' + product_json['ProductDescription'] + '"'
    last_name = str(customer_json['ContactLastName'])
    customer = '''
                input: {
                    firstName: "''' + first_name + '''",
                    lastName: "''' + last_name + '''"
                }
                '''#.format(first_name, last_name)
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


def upload_order():
    """
        function will take a json object containing order information
        and upload that order's details to a shopify store using the GraphQL
        functionality of the Shopify_Python_API

    arguments:
        - order_json: the json objcet with customer information
        - shopify_session: the current session you are working in
            representing the shop you are working with, and want data added to.

    returns:
        - id: the unique id of the newly created order
    """
    pass

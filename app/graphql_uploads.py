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
# customer_resource = Resource('Customers', UNLEASHED_AUTH_ID,\
#                             UNLEASHED_AUTH_SIGNATURE, \
#                             UNLEASHED_API_ADDRESS)

    # customer_resource = Resource('Customers', os.getenv('UNLEASHED_AUTH_ID'),\
    #                             os.getenv('UNLEASHED_AUTH_SIGNATURE'), \
    #                             os.getenv('UNLEASHED_API_ADDRESS'))
    # all_customers = json.loads(customer_resource.all_results())
    first_name = str(customer_json['ContactFirstName'])
    last_name = str(customer_json['ContactLastName'])
    customer = '\
                input: {\
                    firstName: {},\
                    lastName: {}\
                }'.format(first_name, last_name)
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

def upoad_product():
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
    pass

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

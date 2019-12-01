import shopify as sfy

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

    pass

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

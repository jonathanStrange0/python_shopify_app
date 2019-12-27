import shopify as sfy
import json, random
from app.models import Customer
from app import db

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
    num_existing_customers = len(Customer.query.all())
    if num_existing_customers == 0:
        first_name_list = ['TC{} First Name'.format(x) for x in\
                                                    range(0,records_to_create)]
        last_name_list = ['TC{} Last Name'.format(x) for x in\
                                                    range(0,records_to_create)]
    else:
        first_name_list = ['TC{} First Name'.format(x) for x in\
                                                    range(num_existing_customers ,num_existing_customers + records_to_create)]
        last_name_list = ['TC{} Last Name'.format(x) for x in\
                                                    range(num_existing_customers ,num_existing_customers + records_to_create )]

    upload_all_customers(first_name_list, last_name_list)
    print(first_name_list)

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
    cust_gid = json.loads(result)['data']['customerCreate']['customer']['id']
    # add this customer to the database
    cust = Customer(gid = cust_gid, first_name=first_name, last_name= last_name)
    db.session.add(cust)
    db.session.commit()
    # print(result)
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

def delete_customer(gid):
    customer = '''
                    input: {
                        id: "''' + gid + '''"
                    }
                '''

    del_cust_mutation = '''
                            mutation {
                                customerDelete(''' + customer + '''){
                                    deletedCustomerId
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
    db.session.delete(Customer.query.filter_by(gid = gid).first())
    db.session.commit()
    client = sfy.GraphQL()
    result = client.execute(del_cust_mutation)
    print(result)

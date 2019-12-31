import shopify as sfy
import json, random
import numpy as np
from app.models import Customer, Product, Variant
from pprint import pprint

def generate_orders(num_orders, max_line_items, max_qty_sold):
    """
        given the number of orders, push draft orders to shopify and complete them
    """
    # get necessary lists
    customer_list = gen_customer_list(num_orders)
    random.shuffle(customer_list)
    line_item_list = gen_line_item_list(num_orders, max_line_items)
    print('line item list: ', line_item_list)
    variant_detail_list = gen_product_list(line_item_list)
    print('variant detail list: ', variant_detail_list)
    random.shuffle(variant_detail_list)
    # vdl = [[x[0]] * x[2] for x in variant_detail_list]
    # vdl = [gid for gid_list in vdl for gid in gid_list]
    # print(vdl)
    for i in range(num_orders):
        customer_gid = customer_list.pop().gid
        num_vars = random.choice(line_item_list)
        print('number of variants on the order: ', num_vars)
        variant_list = [[random.choice(variant_detail_list), random.choice(range(1,max_qty_sold + 1))] \
                                                        for x in range(0,num_vars)]
        print(variant_list)
        gen_order(customer_gid, variant_list)


def gen_order(customer_gid, variant_list):
    """
        Creates a single order
    """
    line_items_string = ''
    for item in variant_list:
        line_item = gen_order_line_item(item[0].gid, item[1])
        line_items_string += '{variantId:  "%s",  quantity: %i }' %\
                            (line_item['variantId'], line_item['quantity'])
    print(line_items_string)

    draft_order = '''
                input: {
                    customerId: "''' + customer_gid + '''",
                    lineItems:['''+ line_items_string +''']
                }
                '''
    pprint(draft_order)
    order_mutation = '''mutation {
                                    draftOrderCreate(''' + draft_order + ''')
                                        {
                                            draftOrder {
                                                        id
                                                    }
                                            userErrors {
                                                        field
                                                        message
                                                    }
                                        }
                                    }
                            '''
    pprint(order_mutation)
    client = sfy.GraphQL()
    result = client.execute(order_mutation)

    pprint(json.loads(result))
    # pass

def gen_line_item_list(num_orders, max_line_items):
    """
        based on the number of orders, and the max number of variants selected for
        each order, return a list of integers num_orders long with a random value
        in range(1,max_line_items + 1)
    """
    return [random.choice(range(1, max_line_items + 1)) for i in range(num_orders)]


def gen_customer_list(num_orders):
    """
        takes in the number of orders to create, and generates the list of
        customers to choose from using a pareto distribution for probabilty
    """
    cust = Customer.query.all()
    cust_list_prob = apply_pareto(cust)
    return np.random.choice(cust, num_orders, cust_list_prob).tolist()

def gen_order_line_item(variant_id, quantity):
    """
        given the product variant, and quantity of items sold, create the line
        item GraphQL query necessary to add this line to a draft order.
    """
    # line_item = '''
    #
    #             '''
    line_item = {}
    line_item['variantId'] = variant_id
    line_item['quantity'] = quantity
    # return(json.dumps(line_item))
    return(line_item)

def gen_product_list(line_item_list):
    """
        Given the line item list, determine how many total line items will be needed
        and using the pareto distribution, specify how many times each product will be needed.
    """
    total_line_items = np.sum(np.array(line_item_list))
    variants_list = Variant.query.all()
    _, variant_list_prob = apply_pareto(variants_list)
    # num_variant_purchases_list = [int(round(x[1] * total_line_items)) for x in variant_list_w_prob]
    # varian_detail_list = np.concatenate((np.array(variant_list_w_prob), \
                    # np.array(num_variant_purchases_list).reshape(-1,1)), axis=1).tolist()
    # varian_detail_list shape ['variant gid', 'probability of being picked', 'number of times variant is picked']

    variant_detail_list = np.random.choice(variants_list, total_line_items, variant_list_prob).tolist()
    return(variant_detail_list)

def apply_pareto(list):
    """
        Given a list length as a distribution size, determine the probabilty
        that each item in the list is called on using a pareto distribution.
    """
    distribution = np.array([random.paretovariate(1.16) for x in range(0,len(list))])
    distribution /= np.sum(distribution)

    # return np.concatenate((np.array(list).reshape(-1,1), np.array(distribution).reshape(-1,1)), axis=1).tolist()
    return list, distribution.flatten().tolist()

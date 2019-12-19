import shopify as sfy
import json, random
import numpy as np

def generate_orders(num_orders, max_line_items, max_qty_sold):
    """
        given the number of orders, push draft orders to shopify and complete them
    """
    # get necessary lists
    customer_list = gen_customer_list(num_orders)
    random.shuffle(customer_list)
    line_item_list = gen_line_item_list(num_orders, max_line_items)
    variant_detail_list = gen_product_list(line_item_list)
    random.shuffle(variant_detail_list)
    vdl = [[x[0]] * x[2] for x in variant_detail_list]
    vdl = [gid for gid_list in vdl for gid in gid_list]
    for i in range(num_orders):
        customer_gid = customer_list.pop()
        num_vars = random.choice(line_item_list)
        variant_list = [[random.choice(vdl), random.choice(range(1,max_qty_sold))] \
                                                        for x in range(1,num_vars)]
        gen_order(customer_gid, variant_list)


def gen_order(customer_gid, variant_list):
    """
        Creates a single order
    """
    line_items_string = ''
    for item in variant_list:
        line_item = gen_order_line_item(item, 1)
        line_items_string += ' {} '.format(line_item)
    draft_order = '''
                input: {
                    customerId: "''' + customer_gid + '''",
                    lineItems:"{'''+ line_items_string +'''}"
                }
                '''
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


    pass

def gen_line_item_list(num_orders, max_line_items):
    """
        based on the number of orders, and the max number of variants selected for
        each order, return a list of integers num_orders long with a random value
        in range(1,max_line_items + 1)
    """
    return [random.choice(range(1, max_line_items + 1)) for x in range(num_orders)]


def gen_customer_list(num_orders):
    """
        takes in the number of orders to create, and generates the list of
        customers to choose from using a pareto distribution for probabilty
    """
    #TODO: get all customers from database
    cust = [] #Customer.query.all()
    cust_list_w_prob = apply_pareto(len(cust))
    pass

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
    line_item['quantity'] = str(quantity)
    return(json.dumps(line_item))

def gen_product_list(line_item_list):
    """
        Given the line item list, determine how many total line items will be needed
        and using the pareto distribution, specify how many times each product will be needed.
    """
    total_line_items = np.sum(np.array(line_item_list))
    #TODO: get the whole list of product variants
    variants_list = [] # Products.query.all()
    variant_list_w_prob = apply_pareto(len(variants_list))
    num_variant_purchases_list = [round(x[1] * total_line_items) for x in variant_list_w_prob]
    varian_detail_list = np.concatenate((np.array(variant_list_w_prob), \
                    np.array(num_variant_purchases_list).reshape(-1,1)), axis=1).tolist()
    # varian_detail_list shape ['variant gid', 'probability of being picked', 'number of times variant is picked']
    return(varian_detail_list)

def apply_pareto(list):
    """
        Given a list length as a distribution size, determine the probabilty
        that each item in the list is called on using a pareto distribution.
    """
    distribution = np.array([random.paretovariate(1.16) for x in range(1,len(list))])
    prob_list /= np.sum(distribution)
    np.concatenate((np.array(list).reshape(-1,1), np.array(prob_list).reshape(-1,1)), axis=1)
    return prob_list.tolist()

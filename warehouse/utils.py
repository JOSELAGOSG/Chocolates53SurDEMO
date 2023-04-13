from .models import Brand, Product, Provider, Purchase, PurchaseItem, Box

def get_amount_stock_per_product():
    amount_stock_dict = {}
    products = Product.objects.all()
    for product in products:
        if product.measurement == 'kg':
            amount_stock_dict[product.name] = product.get_total_amount_in_warehouse()
    return amount_stock_dict

def get_withdrawn_amount_per_product():
    withdrawn_amount_dict = {}
    products = Product.objects.all()
    for product in products:
        withdrawn_amount_dict[product.name] = product.get_total_amount_withdrawn()
    return withdrawn_amount_dict

def get_value_stock_per_product():
    value_stock_dict = {}
    products = Product.objects.all()
    for product in products:
        value_stock_dict[product.name] = product.get_total_value_in_warehouse()
    return value_stock_dict

def get_withdrawn_value_per_product():
    withdrawn_value_dict = {}
    products = Product.objects.all()
    for product in products:
        withdrawn_value_dict[product.name] = product.get_total_value_withdrawn()
    return withdrawn_value_dict

def get_total_amount_in_warehouse():
    amount = 0
    products = Product.objects.all()
    for product in products:
        if product.measurement == 'kg':
            amount += product.get_total_amount_in_warehouse()
    return amount

def get_total_amount_withdrawn():
    amount = 0
    products = Product.objects.all()
    for product in products:
        amount += product.get_total_amount_withdrawn()
    return amount

def get_total_value_in_warehouse():
    value = 0 
    products = Product.objects.all()
    for product in products:
        value += product.get_total_value_in_warehouse()
    return value

def get_total_value_withdrawn():
    value = 0 
    products = Product.objects.all()
    for product in products:
        value += product.get_total_value_withdrawn()
    return value

def get_boxes_amount_in_warehouse():
    boxes_in_warehouse = Box.objects.filter(in_warehouse=True)
    return len(boxes_in_warehouse)

def get_boxes_amount_withdrawn():
    withdrawn_boxes = Box.objects.filter(in_warehouse=False)
    return len(withdrawn_boxes)

def get_boxes_amount_soon_to_expire_in_warehouse():
    boxes = Box.objects.all()
    soon_to_expire_boxes = []
    for box in boxes:
        if box.soon_to_expire() and box.in_warehouse:
            soon_to_expire_boxes.append(box)
    return len(soon_to_expire_boxes)

def get_boxes_amount_not_soon_to_expire_in_warehouse():
    boxes = Box.objects.all()
    not_soon_to_expire_boxes = []
    for box in boxes:
        if not box.soon_to_expire() and box.in_warehouse:
            not_soon_to_expire_boxes.append(box)
    return len(not_soon_to_expire_boxes)

def get_boxes_amount_in_warehouse_per_product():
    products = Product.objects.all()
    _list = []
    for product in products:
        if product.get_boxes_amount_in_warehouse() > 0:
            _list.append((product.name, product.get_boxes_amount_in_warehouse()))
    # https://www.programiz.com/python-programming/methods/list/sort
    def take_second(elem):
        return elem[1]
    _list.sort(key=take_second, reverse=True)
    return _list

def get_amount_soon_to_expire_per_product():
    products = Product.objects.filter()
    _list = []
    for product in products:
        if product.get_amount_soon_to_expire_in_warehouse() > 0:
            _list.append((product.name, str(product.get_amount_soon_to_expire_in_warehouse()) + ' ' + product.measurement))
    def take_second(elem):
        return elem[1]
    _list.sort(key=take_second, reverse=True)
    return _list


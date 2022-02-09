from types import SimpleNamespace
def read_file(filename):

    r = SimpleNamespace()
    with open(filename, 'r') as f:
        r.number_of_rows_in_the_area_of_the_simulation , r.number_of_columns_in_the_area_of_the_simulation , r.number_of_drones_available , r.deadline_of_the_simulation , r.maximum_load_of_a_drone = [int(x) for x in f.readline().strip().split(' ')]
        r.P = int(f.readline().strip())
        r.product_types_weight = [int(x) for x in f.readline().strip().split(' ')]

        r.nb_warehouse = int(f.readline().strip())
        r.warehouses = []
        for warehouse_id in range(r.nb_warehouse):
            warehouse = SimpleNamespace()
            warehouse.position = [int(x) for x in f.readline().strip().split(' ')]
            warehouse.available_items = [int(x) for x in f.readline().strip().split(' ')]
            r.warehouses.append(warehouse)

        # customer orders
        r.C = int(f.readline().strip())
        r.customer_orders = []
        for customer_order_id in range(r.C):
            customer_order_info = SimpleNamespace()
            customer_order_info.position = [int(x) for x in f.readline().strip().split(' ')]
            customer_order_info.L = int(f.readline().strip())
            customer_order_info.product_types = [int(x) for x in f.readline().strip().split(' ')]
            r.customer_orders.append(customer_order_info)

    return r


if __name__ == '__main__':
    input_data = read_file('input/busy_day.in')
    print(input_data.number_of_drones_available)
    print(input_data.warehouses[0].available_items)
    print(input_data.C)

    print(input_data.customer_orders)

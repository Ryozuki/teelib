

class Header:
    def __init__(self, size: int, swaplen: int, num_item_types: int, num_items: int,
                 num_data: int, item_size: int, data_size: int):
        self.data_size = data_size
        self.num_items = num_items
        self.item_size = item_size
        self.num_data = num_data
        self.num_item_types = num_item_types
        self.size = size
        self.swaplen = swaplen

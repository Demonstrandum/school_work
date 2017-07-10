class List(object):
    def __init__(self):
        self.productArr = []

    def stdin(self):
        stopped = False
        name, cost = None, None

        while not stopped:
            innerArr = [None] * 2

            name = input('Enter a product\'s name: ')
            if name.lower() == 'stop' or name.capitalize() == 'None':
                print("---PRODUCT LIST TERMINATED---")
                name = None
                stopped = True
                break

            priceIsRight = False
            while not priceIsRight:
                try:
                    cost = input('Enter the product\'s cost: £')
                    if cost.lower() == 'stop' or cost.capitalize() == 'None':
                        print("---PRODUCT LISTING TERMINATED---")
                        cost = None
                        stopped = True
                        break
                    cost = float(cost)
                    priceIsRight = True
                except ValueError:
                    print("\nYour supposed cost could not be converted to a number (float),\n\nTry again:")

            if cost != None: innerArr = name, round(cost, 2)
            print("")

            if None not in innerArr:
                self.productArr.append(list(innerArr))

        return self.productArr

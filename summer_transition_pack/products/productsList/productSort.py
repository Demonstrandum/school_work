import copy

class ProductSort(object):
    def __init__(self, products):
        self.products = products

    def extrema(self):
        arranged = self.productSorter()
        return [arranged[0], arranged[-1]]

    def min(self):
        return self.extrema()[0]

    def max(self):
        return self.extrema()[1]

    def productSorter(self):
        return sorted(self.products, key=lambda product: product[1])

    def discount(self, amount=0.05):
        discounted = copy.deepcopy(self.products) # Python thinks `discounted` should just be a refrence to self.products instead of a copy...
        for i in range(0, len(discounted)):
            if discounted[i][1] > 50:
                discounted[i][1] = discounted[i][1] - (discounted[i][1] * amount)

        return discounted

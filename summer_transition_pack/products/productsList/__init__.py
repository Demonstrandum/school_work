from . import inputList
from . import productSort

def main():
    unarranged   = inputList.List().stdin()
    sortedObject = productSort.ProductSort(unarranged)

    least, most = sortedObject.extrema()
    arranged    = sortedObject.productSorter()
    discounted  = sortedObject.discount(amount=0.05)
    summation   = sum(product[1] for product in unarranged)
    discountSum = sum(discount[1] for discount in discounted)
    average     = summation / len(arranged) # or unarranged, doesn't matter.
    withVAT     = discountSum + discountSum * 0.2

    print('\n\n\'{}\' is the most expensive at: £{:.2f}'.format(most[0], most[1]))
    print('\'{}\' is the cheapes at: £{:.2f}\n'.format(least[0], least[1]))

    print('Average cost among all items is: £{:.2f}\n'.format(average))

    print('Summation of products\' costs is:        £{:.2f}'.format(summation))
    print('With 5% discount on products over £50:  £{:.2f}\n'.format(discountSum))
    print('Final cost with VAT of 20%:             £{:.2f}'.format(withVAT))
    print('===========================             ' + '=' * len('£{:.2f}'.format(withVAT)))
if __file__ == '__main__':
    main()

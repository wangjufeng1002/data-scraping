class AppBookInfo:

    def __init__(self, itemId, defaultPrice, activePrice, coupons, free,sales,originalText):
        self.itemId = itemId
        self.defaultPrice = defaultPrice
        self.activePrice = activePrice
        self.coupons = coupons
        self.free = free
        self.originalText = originalText
        self.sales = sales

    def toString(self):
        return str(self.itemId) + "||" + str(self.defaultPrice) + "||" + str(self.activePrice) + "||" + str(self.coupons) + "||" + str(self.free) + "||"+str(self.sales)+"||" + str(self.originalText)

class AppBookInfo:

    def __init__(self, itemId, defaultPrice, activePrice, coupons, free,sales,name,originalText):
        self.itemId = itemId
        self.defaultPrice = defaultPrice
        self.activePrice = activePrice
        self.coupons = coupons
        self.free = free
        self.originalText = originalText
        self.sales = sales
        self.name = name

    def toString(self):
        return str(self.itemId) +"||"+str(self.name) + "||" + str(self.defaultPrice) + "||" + str(self.activePrice) + "||" + str(self.coupons) + "||" + str(self.free) + "||"+str(self.sales)+"||" + str(self.originalText)

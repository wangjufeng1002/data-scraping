class AppBookInfo:

    def __init__(self, itemId, defaultPrice, activePrice, coupons, free):
        self.itemId = itemId
        self.defaultPrice = defaultPrice
        self.activePrice = activePrice
        self.coupons = coupons
        self.free = free

    def toString(self):
        return self.itemId + "||" + self.defaultPrice + "||" + self.activePrice + "||" + self.coupons + "||" + self.free

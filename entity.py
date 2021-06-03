from typing import Any
import threading, time


class Book:
    activeDesc = ''

    def __init__(self, tmId, name, isbn, auther, price, fixPrice, promotionPrice, promotionPriceDesc, promotionType,
                 activeDesc,
                 activeStartTime,
                 activeEndTime,
                 shopName):
        self.tmId = tmId
        self.name = name
        self.isbn = isbn
        self.auther = auther
        self.price = price
        self.fixPrice = fixPrice
        self.promotionPrice = promotionPrice
        self.promotionPriceDesc = promotionPriceDesc
        self.promotionType = promotionType
        self.activeDesc = activeDesc
        self.activeStartTime = activeStartTime
        self.activeEndTime = activeEndTime
        self.shopName = shopName

    def setFixPrice(self, fixPrice):
        self.fixPrice = fixPrice

    def getFixPrice(self):
        if self.fixPrice is None:
            return "NULL"
        return self.fixPrice

    def setName(self, name):
        self.name = name

    def getName(self):
        if self.name is None:
            return "NULL"
        return self.name

    def setIsbn(self, isbn):
        self.isbn = isbn

    def getIsbn(self):
        if self.isbn is None:
            return "NULL"
        return self.isbn

    def setAuther(self, auther):
        self.auther = auther

    def getAuther(self):
        if self.auther is None:
            return "NULL"
        return self.auther

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        if self.price is None:
            return "NULL"
        return self.price

    def setPromotionPrice(self, promotionPrice):
        self.promotionPrice = promotionPrice

    def setPromotionType(self, promotionPriceType):
        self.promotionType = promotionPriceType

    def getPromotionType(self):
        if self.promotionType is None:
            return "NULL"
        return self.promotionType

    def getPromotionPrice(self):
        if self.promotionPrice is None:
            return "NULL"
        return self.promotionPrice

    def setActiveDesc(self, activeDesc):
        self.activeDesc = activeDesc

    def getActiveDesc(self):
        if self.activeDesc is None:
            return []
        return self.activeDesc

    def getActiveDescStr(self):
        if self.activeDesc is None:
            return ''
        return ",".join(self.getActiveDesc())

    def getTmId(self):
        return self.tmId

    def getPromotionPriceDesc(self):
        return self.promotionPriceDesc

    def setPromotionPriceDesc(self, promotionPriceDesc):
        self.promotionPriceDesc = promotionPriceDesc

    def setShopName(self, shopName):
        self.shopName = shopName

    def getShopName(self):
        return self.shopName

    def setActiveStartTime(self, activeStartTime):
        self.activeStartTime = activeStartTime

    def getActiveStartTime(self):
        if self.activeStartTime is None:
            return "1996-10-02"
        activeStartTime = self.activeStartTime / 1000.0
        timearr = time.localtime(activeStartTime)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearr)

    def setActiveEndTime(self, activeEndTime):
        self.activeEndTime = activeEndTime

    def getActiveEndTime(self):
        if self.activeEndTime is None:
            return "1996-10-02"
        activeEndTime = self.activeEndTime / 1000.0
        timearr = time.localtime(activeEndTime)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearr)

    def toString(self):
        result = []
        result.append("[天猫ID:" + self.getTmId() + "]")
        result.append("[书名:" + self.getName() + "]")
        result.append("[ISBN编码:" + self.getIsbn() + "]")
        result.append("[作者:" + self.getAuther() + "]")
        result.append("[默认价格:" + self.getPrice() + "]")
        result.append("[促销价:" + self.getPromotionPrice() + "]")
        result.append("[促销价描述:" + self.getPromotionPriceDesc() + "]")
        result.append("[活动:" + (",".join(self.getActiveDesc())) + "]")
        return ",".join(result)
    # return self.getName() + "," + self.getIsbn() + "," +self.getAuther()+ "," +self.getPrice() +"," +self.getPromotionPrice() + self.getActiveDesc()


class ItemUrl:
    def __init__(self, itemId, itemUrl, shopName):
        self.itemId = itemId
        self.itemUrl = itemUrl
        self.shopName = shopName

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    # def getItemId(self):
    #     return self.itemId
    #
    # def getItemUrl(self):
    #     return self.itemUrl
    #
    # def getShopName(self):
    #     return self.shopName
    #
    # def setItemId(self, itemId):
    #     self.itemId = itemId
    #
    # def setItemUrl(self, itemUrl):
    #     self.itemUrl = itemUrl
    #
    # def setShopName(self, shopName):
    #     self.shopName = shopName

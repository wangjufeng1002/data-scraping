import time
from datetime import datetime
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


class Book:
    activeDesc = ''

    def __init__(self, tmId, name, isbn, auther, price, fixPrice, promotionPrice, promotionPriceDesc, promotionType,
                 activeDesc,
                 activeStartTime,
                 activeEndTime,
                 shopName, category, sales,press,skuId,skuName):
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
        self.category = category
        self.sales = sales
        self.press= press
        self.skuId = skuId
        self.skuName = skuName

    def setSales(self, sales):
        self.sales = sales

    def getSales(self):
        if self.sales is None:
            return "0"
        return self.sales

    def setFixPrice(self, fixPrice):
        self.fixPrice = fixPrice

    def getFixPrice(self):
        if self.fixPrice is None:
            return "0"
        return self.fixPrice

    def setName(self, name):
        self.name = name

    def getName(self):
        if self.name is None:
            return "无"
        return self.name

    def setIsbn(self, isbn):
        self.isbn = isbn

    def getIsbn(self):
        if self.isbn is None:
            return "无"
        return self.isbn

    def setAuther(self, auther):
        self.auther = auther

    def getAuther(self):
        if self.auther is None:
            return "无"
        return self.auther

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        if self.price is None:
            return "无"
        return self.price

    def setPromotionPrice(self, promotionPrice):
        self.promotionPrice = promotionPrice

    def setPromotionType(self, promotionPriceType):
        self.promotionType = promotionPriceType

    def getPromotionType(self):
        if self.promotionType is None or self.promotionType == 'None' or self.promotionType == 'NULL':
            return "无"
        return self.promotionType

    def getPromotionPrice(self):
        if self.promotionPrice is None:
            return "0"
        return self.promotionPrice

    def setActiveDesc(self, activeDesc):
        self.activeDesc = activeDesc

    def getActiveDesc(self):
        if self.activeDesc is None:
            return []
        return self.activeDesc

    def getActiveDescStr(self):
        if self.activeDesc is None or self.activeDesc == 'None' or self.activeDesc == 'NULL':
            return '无'
        return ",".join(self.getActiveDesc())

    def getTmId(self):
        return self.tmId

    def getPromotionPriceDesc(self):
        if self.promotionPriceDesc is None or self.promotionPriceDesc == 'None' or self.promotionPriceDesc == 'NULL':
            return '无'
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
        if(isinstance(self.activeStartTime,datetime)):
            return self.activeStartTime.strftime('%Y-%m-%d %H:%M:%S')
        activeStartTime = self.activeStartTime / 1000.0
        timearr = time.localtime(activeStartTime)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearr)

    def setActiveEndTime(self, activeEndTime):
        self.activeEndTime = activeEndTime

    def getActiveEndTime(self):
        if self.activeEndTime is None:
            return "1996-10-02"
        if (isinstance(self.activeEndTime, datetime)):
            return self.activeEndTime.strftime('%Y-%m-%d %H:%M:%S')
        activeEndTime = self.activeEndTime / 1000.0
        timearr = time.localtime(activeEndTime)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearr)

    def getCategory(self):
        if self.category is None or self.category == 'None' or self.category == 'NULL':
            return "无"
        return self.category

    def setCategory(self, category):
        self.category = category

    def setPress(self, press):
        self.press = press

    def getPress(self):
        if self.press is None or self.press == 'None' or self.press == 'NULL':
            return '无'
        return self.press

    def setSkuId(self, skuId):
        self.skuId = skuId

    def setSkuName(self, skuName):
        self.skuName = skuName

    def getSkuId(self):
        if self.skuId is None:
            return ""
        return self.skuId

    def getSkuName(self):
        if self.skuName is None:
            return ""
        return self.skuName
    def toDESCString(self):
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

    def toString(self):
        result = []
        result.append(self.getTmId())
        result.append(self.getName().replace("\n"," ").replace('"'," ").replace("\t","-"))
        result.append(self.getIsbn())
        result.append(self.getAuther())
        result.append(self.getPrice())
        result.append(self.getFixPrice())
        result.append(self.getPromotionPrice())
        result.append(self.getPromotionPriceDesc())
        result.append(self.getActiveDescStr())
        result.append(self.getPromotionType())
        result.append(self.getShopName())
        result.append(self.getActiveStartTime())
        result.append(self.getActiveEndTime())
        result.append(self.getSales())
        result.append(self.getCategory())
        result.append(self.getPress())
        return "\t".join(result)

    def __format__(self, format_spec: str) -> str:
        return super().__format__(format_spec)
    # return self.getName() + "," + self.getIsbn() + "," +self.getAuther()+ "," +self.getPrice() +"," +self.getPromotionPrice() + self.getActiveDesc()

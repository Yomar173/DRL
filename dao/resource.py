from config.dbconfig import pg_config, url_conn
import psycopg2

class ResourceDAO:

    def __init__(self):
        #Connect to Database
        connection_url = url_conn
        self.conn = psycopg2._connect(connection_url)


    def getAllResources(self):              #Get all resources.
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype from resource natural inner join resourcetype order by rname;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceByID(self, rid):         #Get the resource by its ID.
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype from resource natural inner join resourcetype where rid=%s;"
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        return result

    def getSupplierByResourceID(self,rid):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, adcountry, rname, rqty, rprice, rcondition " \
                "from supplier natural inner join inventory natural inner join resource " \
                "natural inner join account natural inner join address " \
                "where rid = %s and isHidden = FALSE " \
                " by aname;"
        cursor.execute(query, (rid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceByName(self, resourceName):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype from resource natural inner join resourcetype where rname = %s order by rname;"
        cursor.execute(query, (resourceName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceByCategory(self, categoryName):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype from resource natural inner join resourcetype where rtype = %s order by rname;"
        cursor.execute(query, (categoryName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceByNameAndCategory(self, resourceName, categoryName):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype from resource natural inner join resourcetype where rtype = %s and rname=%s order by rname;"
        cursor.execute(query, (categoryName,resourceName))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResources(self):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address " \
                "where rqty > 0 and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourcesByCity(self, supplier_city):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address " \
                "where rqty > 0 and rcity = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(supplier_city,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourcesByRegion(self, supplier_region):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address natural inner join region " \
                "where rqty > 0 and rregion = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(supplier_region,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourcesByName(self, resource_name):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address " \
                "where rqty > 0 and rname = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(resource_name,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourcesByNameAndCity(self, resource_name, supplier_city):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address " \
                "where rqty > 0 and rname = %s and rcity = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(resource_name,supplier_city,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourcesByNameAndRegion(self, resource_name, supplier_region):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address natural inner join region " \
                "where rqty > 0 and rname = %s and rregion = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(resource_name,supplier_region,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourcesByCategory(self, resource_category):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address " \
                "where rqty > 0 and rtype = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(resource_category,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourcesByCategoryAndSubCategory(self, resource_category, resource_subcategory):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address " \
                "where rqty > 0 and rtype = %s and rtsubcategory = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(resource_category, resource_subcategory,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourceByCategoryAndSubCategoryAndCity(self, resource_category, resource_subcategory, supplier_city):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account " \
                "natural inner join address " \
                "where rqty > 0 and rtype = %s and rtsubcategory = %s and rcity = %s and isHidden = FALSE " \
                "order by rname;"
        cursor.execute(query,(resource_category, resource_subcategory, supplier_city))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesInNeed(self):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, qty " \
                "from (select rid, sum(reqty) as qty from request where isCompleted=false group by rid) as ResourceNeed " \
                "natural inner join resource " \
                "order by rname;"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAvailableResourceByCategoryAndCity(self, resource_category, supplier_city):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account natural inner join address " \
                "where rcity = %s and  rtype = %s and isHidden = FALSE "
        cursor.execute(query, (supplier_city, resource_category,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceByCity(self, supplier_city):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, sid, aname, alastname, scompany, adneighborhood, rcity, adstate " \
                "from resource natural inner join resourcetype natural inner join inventory " \
                "natural inner join supplier natural inner join account natural inner join address " \
                "where rcity = %s and isHidden = FALSE "
        cursor.execute(query, (supplier_city,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByResourceIDAndCity(self, rid, supplier_city):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, adcountry, rname, rqty, rprice, rcondition " \
                "from supplier natural inner join inventory natural inner join resource " \
                "natural inner join account natural inner join address " \
                "where rid = %s and rcity = %s and isHidden = FALSE " \
                "order by aname;"
        cursor.execute(query, (rid, supplier_city,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Insert a Resource to Inventory
    def insertAvailableResource(self, rqty, rprice, rcondition, rid, sid):
        cursor = self.conn.cursor()
        query = 'insert into inventory(rqty, rprice, rcondition, rid, sid, isHidden) values (%s, %s, %s, %s, %s, %s) returning iid;'
        try:
            cursor.execute(query, (rqty, rprice,rcondition, rid, sid, 'FALSE',))
            iid = cursor.fetchone()[0]
            self.conn.commit()
            return iid
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    #Insert a Resource to Dictionary
    def insertResource(self, rname, rbrand, rtid):
        cursor = self.conn.cursor()
        query = 'insert into resource(rname, rbrand, rtid) values (%s, %s, %s) returning rid;'
        try:
            cursor.execute(query, (rname, rbrand, rtid,))
            rid = cursor.fetchone()[0]
            self.conn.commit()
            return rid
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def hideInventory(self, rid, sid, isHidden):
        cursor = self.conn.cursor()
        query = 'update inventory set isHidden = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (isHidden, rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def updateInventoryQty(self, rqty, rid, sid):
        cursor = self.conn.cursor()
        query = 'update inventory set rqty = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (rqty,rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def updateInventoryQtyAndPrice(self, rqty, rprice, rid, sid):
        cursor = self.conn.cursor()
        query = 'update inventory set rqty = %s, rprice = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (rqty, rprice, rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def updateInventoryQtyAndCondition(self, rqty, rcondition, rid, sid):
        cursor = self.conn.cursor()
        query = 'update inventory set rqty = %s, rcondition = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (rqty, rcondition, rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def updateInventoryQtyAndPriceAndCondition(self, rqty, rprice, rcondition, rid, sid):
        cursor = self.conn.cursor()
        query = 'update inventory set rqty = %s, rprice =  %s, rcondition = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (rqty, rprice, rcondition, rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def updateInventoryPrice(self, rprice, rid, sid):
        cursor = self.conn.cursor()
        query = 'update inventory set rprice = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (rprice,rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def updateInventoryPriceAndCondition(self, rprice, rcondition, rid, sid):
        cursor = self.conn.cursor()
        query = 'update inventory set rprice = %s, rcondition = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (rprice, rcondition ,rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def updateInventoryCondition(self, rcondition, rid, sid):
        cursor = self.conn.cursor()
        query = 'update inventory set rcondition = %s where rid = %s and sid = %s'
        try:
            cursor.execute(query, (rcondition ,rid, sid,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return None

    def getSalesByResourceID(self, rid):
        cursor = self.conn.cursor()
        query = 'select BID, Buyer.AName as BName, Buyer.ALastName as BLastName, Buyer.AEmail as BEmail, Buyer.ADCountry as BCountry, Buyer.ADState as BState, Buyer.RCity as BCity, Supplier.SID, Supplier.AName, Supplier.ALastName, Supplier.SCompany, ' \
                'TID, TDate, TAmount, TPrice, RID, RName, RBrand ' \
                'from transactions natural inner join resource natural inner join (buyer natural inner join account natural inner join address) as Buyer ' \
                'join (supplier natural inner join account) as Supplier using(SID) ' \
                'where rid = %s'
        cursor.execute(query, (rid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTotalSalesByResourceID(self, rid):
        cursor = self.conn.cursor()
        query = 'with sales as (select sid, rid, sum(tamount*tprice) as total_sales from transactions where rid = %s group by sid, rid) ' \
                'select sid, scompany, aname, alastname, rcity, rid, rname, rbrand, total_sales ' \
                'from supplier natural inner join account natural inner join address ' \
                'natural inner join region natural inner join sales natural inner join resource'
        cursor.execute(query, (rid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInventoryBySIDAndRID(self, sid, rid):
        cursor = self.conn.cursor()
        query = 'select * from inventory where rid = %s and sid = %s'
        cursor.execute(query, (rid, sid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

if __name__ == '__main__':
    dao = ResourceDAO()
    #result = dao.getResourceByNameAndCategory('Batman T-Shirt','Clothing')
    #result = dao.getAvailableResources()
    #result = dao.getResourceByName('Screwdriver')
    #result = dao.getResourcesInNeed()
    #result = dao.getResourceByID(1)
    result = dao.getResourceByCategoryAndCity('Ice', 'San Juan')
    result = dao.getResourceByCity('San Juan')
    for row in result:
        print(row)
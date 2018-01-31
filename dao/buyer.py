from datetime import datetime

from config.dbconfig import pg_config, url_conn
from datetime import datetime
import psycopg2

class BuyerDao :

    def __init__(self) :
        #Connect to Database
        connection_url = url_conn
        self.conn = psycopg2.connect(connection_url) # verify if is _connect

    # Retrieve all the Buyers...
    def getBuyers(self) :
        cursor = self.conn.cursor()

        # Get all Buyers accounts...
        query = "select BID, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone, " \
                "ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode " \
                "from buyer natural inner join account natural inner join address;"
        cursor.execute(query)
        result = []
        for row in cursor :
            result.append(row)
        return result

    # Retrieve all the Buyers by city...
    def getBuyersByCity(self, city) :
        cursor = self.conn.cursor()
        query = "select BID, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone, " \
                "ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode " \
                "from buyer natural inner join account" \
                " natural inner join address where RCity = %s" # Get all Buyers whose account has an address in the input city.
        cursor.execute(query, (city,))
        result = []
        for row in cursor :
            result.append(row)
        return result

    def getBuyersByRegion(self, region):
        cursor = self.conn.cursor()
        query = "select BID, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone, " \
                "ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode " \
                "from buyer natural inner join account natural inner join " \
                "address natural inner join Region where RRegion = %s"
        cursor.execute(query, (region,))
        result = []
        for row in cursor :
            result.append(row)
        return result

    # Retrieve the Buyer by its ID.
    def getBuyerByID(self, id) :
        cursor = self.conn.cursor()
        query = "select BID, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone, " \
                "ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode " \
                "from buyer natural inner join account natural inner join address " \
                "where BID = %s;" # Get the Buyer whose account has the input BID.
        cursor.execute(query, (id,))
        buyer = cursor.fetchone()
        result = []
        result.append(buyer)
        return result

    def getBuyerRequests(self, id) :
        cursor = self.conn.cursor()
        query = "select BID, AName, ALastName, AEmail, AGender, APPhone, ADCountry, ADState, RCity, ReID, ReQty, " \
                "ReDate, RID, RName, RBrand " \
                "from buyer natural inner join request natural inner join resource natural inner join " \
                "account natural inner join address " \
                "where BID = %s"
        cursor.execute(query, (id,))
        result = []
        for row in cursor : result.append(row)
        return result

    def getBuyerTransactions(self, BID):
        cursor = self.conn.cursor()
        query = "select BID, Buyer.AName, Buyer.ALastName, Buyer.AEmail, Buyer.ADCountry, Buyer.ADState, Buyer.RCity, Supplier.SID, Supplier.AName, Supplier.ALastName, Supplier.SCompany, " \
                "TID, TDate, TAmount, TPrice, RID, RName, RBrand "\
                "from transactions natural inner join resource natural inner join (buyer natural inner join account natural inner join address) as Buyer " \
                "join (supplier natural inner join account) as Supplier using(SID) "\
                "where BID = %s;"
        cursor.execute(query, (BID,))
        result = []
        for row in cursor : result.append(row)
        return result

    def getBuyerDonations(self, BID):
        cursor = self.conn.cursor()
        query = "select BID, Buyer.AName, Buyer.ALastName, Buyer.AEmail, Buyer.ADCountry, Buyer.ADState, Buyer.RCity, Supplier.SID, Supplier.AName, Supplier.ALastName, Supplier.SCompany, " \
                "TID, TDate, TAmount, TPrice, RID, RName, RBrand "\
                "from transactions natural inner join resource natural inner join (buyer natural inner join account natural inner join address) as Buyer " \
                "join (supplier natural inner join account) as Supplier using(SID) "\
                "where BID = %s and TPrice = 0;"
        cursor.execute(query, (BID,))
        result = []
        for row in cursor : result.append(row)
        return result

    def getBuyerPurchases(self, BID):
        cursor = self.conn.cursor()
        query = "select BID, Buyer.AName, Buyer.ALastName, Buyer.AEmail, Buyer.ADCountry, Buyer.ADState, Buyer.RCity, Supplier.SID, Supplier.AName, Supplier.ALastName, Supplier.SCompany, " \
                "TID, TDate, TAmount, TPrice, RID, RName, RBrand "\
                "from transactions natural inner join resource natural inner join (buyer natural inner join account natural inner join address) as Buyer " \
                "join (supplier natural inner join account) as Supplier using(SID) "\
                "where BID = %s and TPrice > 0;"
        cursor.execute(query, (BID,))
        result = []
        for row in cursor : result.append(row)
        return result
#Yomar__________________________________________________________________________________________________
    def insertBuyer(self, name, lname, email, gender, bdate, pphone, sphone):
        cursor = self.conn.cursor()
        query = "INSERT INTO Account(aname,alastname,aemail,agender,abdate,apphone,asphone) "\
                "values(%s,%s,%s,%s,%s,%s,%s) returning *;"
        cursor.execute(query,(name,lname,email,gender,datetime.strptime(bdate,'%m/%d/%Y'),pphone,sphone))
        buyer = cursor.fetchone()
        self.conn.commit()
        queryBuyer = "INSERT INTO Buyer(aid) values(%s);"
        cursor.execute(queryBuyer,(buyer[0],))
        self.conn.commit()
        return buyer

    def update_card_CFullName(self, bid, cnumber, CFullName):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_edit_name = "update creditcard set CFullName = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_name, (CFullName, aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CSCode(self, bid, cnumber, CSCode):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_edit_cscode = "update creditcard set CSCode = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CSCode, aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CExpDate(self, bid, cnumber, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_edit_cscode = "update creditcard set CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (self.get_date(CExpDate), aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CFullName_CSCode(self, bid, cnumber, CFullName, CSCode):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_edit_cscode = "update creditcard set CFullName = %s, CSCode = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CFullName, CSCode, aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CFullName_CExpDate(self, bid, cnumber, CFullName, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_edit_cscode = "update creditcard set CFullName = %s, CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CFullName, self.get_date(CExpDate), aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CSCode_CExpDate(self, bid, cnumber, CSCode, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_edit_cscode = "update creditcard set CSCode = %s, CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CSCode, self.get_date(CExpDate), aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_all(self, bid, cnumber, CFullName, CSCode, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_edit_cscode = "update creditcard set CFullName = %s, CSCode = %s, CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CFullName, CSCode, self.get_date(CExpDate), aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def get_card_info(self, cid):
        cursor = self.conn.cursor()
        query = "select CID, CFullName, CNumber, CSCode, BID, CExpDate from creditcard natural inner join buyer where CID = %s;"
        cursor.execute(query, (cid,))
        card = cursor.fetchone()
        result = []
        for row in card :
            result.append(row)
        return result

    def get_date(self, date):
        date = datetime.strptime(date, '%d%b%Y')
        return date

    def insert_card(self, bid, CFullName, CNumber, CType, CSCode, CExpDate):
        cursor = self.conn.cursor()
        query_cti = "select CTI from cardtype where CompanyName = %s;"
        query_account = "select AID from account natural inner join buyer where BID = %s;"
        query_card = "insert into creditcard(AID, CFullName, CNumber, CTI, CSCode, CExpDate) values(%s, %s, %s, %s, %s, %s) returning CID;"
        try:
            cursor.execute(query_account, (bid,))
            aid = cursor.fetchone()
            cursor.execute(query_cti, (CType,))
            cti = cursor.fetchone()
            cursor.execute(query_card, (aid, CFullName, CNumber, cti, CSCode, CExpDate,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None


if __name__ == '__main__':
    dao = BuyerDao()
    # data = dao.getBuyers()
    # for row in data :
    #     print(row)
    #
    # data = dao.getBuyerByID(1)
    # for row in data :
    #     print(row)
    #
    # data = dao.getBuyerRequests(1)
    # for row in data :
    #     print(row)
    #
    # data = dao.getBuyersByRegion("San Juan")
    # for row in data:
    #     print(row)
    #
    # print("")
    # data = dao.getBuyersByCity('San Juan')
    # for row in data :
    #     print(row)


    # print("")
    # data = dao.getBuyerTransactions(3)
    # for row in data :
    #     print(row)
    bid = 1
    cid = dao.update_card_CFullName(bid, "1111222233334420", "Juan Nevarez")
    card = dao.get_card_info(cid)
    print(card)


from datetime import datetime

from config.dbconfig import pg_config, url_conn
import psycopg2

class SupplierDAO:
    def __init__(self):
        #Connect to Database
        connection_url = url_conn
        self.conn = psycopg2._connect(connection_url)

    def getAllSupplier(self):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone from supplier natural inner join account natural inner join address;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByID(self, sid):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone " \
                "from supplier natural inner join account natural inner join address " \
                "where sid=%s;"
        cursor.execute(query, (sid,))
        result = []
        result = cursor.fetchone()
        return result

    def getResourceBySupplierId(self,sid):
        cursor = self.conn.cursor()
        query = "select rid, rname, rbrand, rtype, rtsubcategory, rqty, rprice, sid, aname, alastname, scompany, rcity, adstate " \
                "from supplier natural inner join account natural inner join address natural inner join inventory natural inner join resource natural inner join resourcetype " \
                "where sid = %s"
        cursor.execute(query, (sid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByCity(self, supplierCity):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone " \
                "from supplier natural inner join account natural inner join address " \
                "where rcity=%s"
        cursor.execute(query, (supplierCity,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByCompany(self, supplierCompany):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone from supplier where scompany = %s;"
        cursor.execute(query, (supplierCompany,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByName(self, supplierName):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone from supplier natural inner join account where aname = %s;"
        cursor.execute(query, (supplierName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByCityAndCompany(self, supplierCity, supplierCompany):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone from supplier natural inner join account natural inner join address where rcity= %s and scompany = %s;"
        cursor.execute(query, (supplierCity, supplierCompany,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByCityAndName(self, supplierCity, supplierName):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone from supplier natural inner join account natural inner join address where rcity= %s and aname = %s;"
        cursor.execute(query, (supplierCity, supplierName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByCompanyAndName(self, supplierCompany, supplierName):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone from supplier natural inner join account where scompany= %s and aname = %s;"
        cursor.execute(query, (supplierCompany, supplierName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByCityAndCompanyAndName(self, supplierCity, supplierCompany, supplierName):
        cursor = self.conn.cursor()
        query = "select sid, aname, alastname, scompany, rcity, adstate, aemail, apphone from supplier natural inner join account natural inner join address where scompany= %s and aname = %s and rcity=%s;"
        cursor.execute(query, (supplierCompany, supplierName, supplierCity,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, SCompany, AID):
        cursor = self.conn.cursor()
        query = "insert into Supplier(SCompany, AID) values (%s, %s);"
        try :
            cursor.execute(query, (SCompany, AID,)) # Creating the new supplier...
            cursor.execute('SELECT LASTVAL()')
            SID = cursor.fetchone()[0]
            print(SID)
            self.conn.commit()
            return SID

        except psycopg2.Error as e:
            return None

    def insert_supplier(self, SCompany, SName, SLastName, SEmail, SGender, SBDate, SPPhone, SSPhone, CFullName, CNumber,
                        CType, CSCode, CExpDate, ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber,
                        ADZipCode):
        cursor = self.conn.cursor()
        query_account = "insert into Account(AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone) values (%s, %s, %s, %s, %s, %s, %s);"
        query_ctype = "select CTI from cardtype where CompanyName = %s;"
        query_card = "insert into CreditCard(CFullName, CNumber, CTI, CSCode, CExpDate, AID) values (%s, %s, %s, %s, %s, %s);"
        query_address = "insert into Address(ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode, AID) values (%s, %s, %s, %s, %s, %s, %s, %s);"
        query_supplier = "insert into Supplier(SCompany, AID) values (%s, %s);"
        try :
            cursor.execute(query_account, (SName, SLastName, SEmail, SGender, self.get_date(SBDate), SPPhone, SSPhone,)) # Creating the new account...
            cursor.execute('SELECT LASTVAL()')
            aid = cursor.fetchone()[0]
            # At this point, the account has been 'inserted' but not committed.
            cursor.execute(query_ctype, (CType,))
            cti = cursor.fetchone() # the ID for the credit card type...
            cursor.execute(query_card, (CFullName, CNumber, cti, CSCode, self.get_date(CExpDate), aid,))
            # At this point, the credit card has been 'inserted' but not committed.
            cursor.execute(query_address, (ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode, aid,))
            # At this point, the address has been 'inserted' but not committed.
            cursor.execute(query_supplier, (SCompany, aid,))
            # At this point, the supplier has been 'inserted'. Lets commit.
            cursor.execute('SELECT LASTVAL()')
            sid = cursor.fetchone()[0]
            self.conn.commit() # GGWP.
            return sid # supplier id.

        except psycopg2.Error as e : # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None


    def get_date(self, date):
        date = datetime.strptime(date, '%d%b%Y')
        return date

    def insert_supplier_no_company(self, SName, SLastName, SEmail, SGender, SBDate, SPPhone, SSPhone, CFullName,
                                   CNumber, CType, CSCode, CExpDate, ADCountry, ADState, RCity, ADNeighborhood,
                                   ADStreet, ADNumber, ADZipCode):
        cursor = self.conn.cursor()
        query_account = "insert into Account(AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone) values (%s, %s, %s, %s, %s, %s, %s) returning AID;"
        query_ctype = "select CTI from cardtype where CompanyName = %s;"
        query_card = "insert into CreditCard(CFullName, CNumber, CTI, CSCode, CExpDate, AID) values (%s, %s, %s, %s, %s, %s);"
        query_address = "insert into Address(ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode, AID) values (%s, %s, %s, %s, %s, %s, %s, %s);"
        query_supplier = "insert into Supplier(AID) values (%s) returning sid;"
        try:
            cursor.execute(query_account, (SName, SLastName, SEmail, SGender, self.get_date(SBDate), SPPhone,
                                           SSPhone,))  # Creating the new account...
            aid = cursor.fetchone()[0]
            # At this point, the account has been 'inserted' but not committed.
            cursor.execute(query_ctype, (CType,))
            cti = cursor.fetchone()  # the ID for the credit card type...

            cursor.execute(query_card, (CFullName, CNumber, cti, CSCode, self.get_date(CExpDate), aid,))
            # At this point, the credit card has been 'inserted' but not committed.
            cursor.execute(query_address,
                           (ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode, aid,))
            # At this point, the address has been 'inserted' but not committed.
            cursor.execute(query_supplier, (aid,))
            # At this point, the supplier has been 'inserted'. Lets commit.
            sid = cursor.fetchone()[0]
            self.conn.commit()  # GGWP.
            return sid  # supplier id.

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CFullName(self, sid, cnumber, CFullName):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_edit_name = "update creditcard set CFullName = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (sid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_name, (CFullName, aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CSCode(self, sid, cnumber, CSCode):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_edit_cscode = "update creditcard set CSCode = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (sid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CSCode, aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CExpDate(self, sid, cnumber, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_edit_cscode = "update creditcard set CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (sid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (self.get_date(CExpDate), aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CFullName_CSCode(self, sid, cnumber, CFullName, CSCode):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_edit_cscode = "update creditcard set CFullName = %s, CSCode = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (sid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CFullName, CSCode, aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CFullName_CExpDate(self, sid, cnumber, CFullName, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_edit_cscode = "update creditcard set CFullName = %s, CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (sid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CFullName, self.get_date(CExpDate), aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_card_CSCode_CExpDate(self, sid, cnumber, CSCode, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_edit_cscode = "update creditcard set CSCode = %s, CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (sid,))
            aid = cursor.fetchone()
            cursor.execute(query_edit_cscode, (CSCode, self.get_date(CExpDate), aid, cnumber,))
            cid = cursor.fetchone()
            self.conn.commit()
            return cid

        except psycopg2.Error as e:  # An error occurred... ABORT!
            print(e)
            self.conn.rollback()
            return None

    def update_all(self, sid, cnumber, CFullName, CSCode, CExpDate):
        cursor = self.conn.cursor()
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_edit_cscode = "update creditcard set CFullName = %s, CSCode = %s, CExpDate = %s where AID = %s and CNumber = %s returning CID;"
        try:
            cursor.execute(query_account, (sid,))
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
        query = "select CID, CFullName, CNumber, CSCode, SID, CExpDate from creditcard natural inner join supplier where CID = %s;"
        cursor.execute(query, (cid,))
        card = cursor.fetchone()
        result = []
        for row in card :
            result.append(row)
        return result

    def insert_card(self, sid, CFullName, CNumber, CType, CSCode, CExpDate):
        cursor = self.conn.cursor()
        query_cti = "select CTI from cardtype where CompanyName = %s;"
        query_account = "select AID from account natural inner join supplier where SID = %s;"
        query_card = "insert into creditcard(AID, CFullName, CNumber, CTI, CSCode, CExpDate) values(%s, %s, %s, %s, %s, %s) returning CID;"
        try:
            cursor.execute(query_account, (sid,))
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
    dao = SupplierDAO()
    #result = dao.getAllSupplier()
    #result = dao.getResourceBySupplierId(1)
    #result = dao.getSupplierByCity('Loiza')
    result = dao.getSupplierByName('Hernan')
    for row in result:
        print(row)
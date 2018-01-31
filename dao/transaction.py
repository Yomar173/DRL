from datetime import datetime

from config.dbconfig import pg_config, url_conn
import psycopg2

class TransactionDAO:
    def __init__(self):
	    #Connect to Database
        connection_url = url_conn
        self.conn = psycopg2._connect(connection_url)

    def getAllTransactions(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM Transactions;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionBySID(self, sid):
        cursor = self.conn.cursor()
        query = "SELECT * FROM Transactions WHERE SID=%s;"
        cursor.execute(query,(sid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert_transaction(self, TAmount, BID, CID, IID) : # this method presumes that CID belongs to BID.
        cursor = self.conn.cursor()
        query_inventory = "select SID, RID, RPrice from inventory where IID = %s and RQty >= %s and RQty > 0 and RPrice > 0 " \
                          "and isHidden = FALSE;"
        query_card = "select CID from creditcard natural inner join account natural inner join buyer where BID = %s and CID = %s;"
        query_purchase = "insert into transactions(TDate, TAmount, TPrice, BID, SID, RID, CID) values (%s, %s, %s, %s, %s, %s, %s) returning tid;"
        query_update_inventory = "update inventory set RQty = RQty - %s where IID = %s;"
        try :
            cursor.execute("select RPrice from inventory where IID = %s;", (IID,))
            cursor.execute(query_card, (BID, CID,))
            cid = cursor.fetchone()
            cursor.execute(query_inventory, (IID, TAmount,))
            inventory = cursor.fetchone()
            if not inventory: return None
            sid = inventory[0]
            rid = inventory[1]
            rprice = inventory[2]
            cursor.execute(query_purchase, (datetime.today(), TAmount, rprice, BID, sid, rid, cid,))
            tid = cursor.fetchone()
            cursor.execute(query_update_inventory, (TAmount, IID,))
            print(tid)
            self.conn.commit()
            return tid
        except psycopg2.Error as e :
            print(e)
            self.conn.rollback()

    def get_transaction(self, transaction):
        cursor = self.conn.cursor()
        query = "select TID, TDate, TAmount, TPrice, BID, SID, RID, CID, ReID from transactions where TID = %s;"
        cursor.execute(query, (transaction,))
        t = cursor.fetchone()
        return t

    def insert_donation(self, TAmount, BID, CID, IID):
        cursor = self.conn.cursor()
        query_inventory = "select SID, RID, RPrice from inventory where IID = %s and RQty >= %s and RQty > 0 and RPrice = 0 " \
                          "and isHidden = FALSE;"
        query_card = "select CID from creditcard natural inner join account natural inner join buyer where BID = %s and CID = %s;"
        query_purchase = "insert into transactions(TDate, TAmount, TPrice, BID, SID, RID, CID) values (%s, %s, %s, %s, %s, %s, %s) returning tid;"
        query_update_inventory = "update inventory set RQty = RQty - %s where IID = %s;"
        try :
            cursor.execute("select RPrice from inventory where IID = %s;", (IID,))
            cursor.execute(query_card, (BID, CID,))
            cid = cursor.fetchone()
            cursor.execute(query_inventory, (IID, TAmount,))
            inventory = cursor.fetchone()
            if not inventory : return None
            sid = inventory[0]
            rid = inventory[1]
            rprice = inventory[2]
            cursor.execute(query_purchase, (datetime.today(), TAmount, rprice, BID, sid, rid, cid,))
            tid = cursor.fetchone()
            cursor.execute(query_update_inventory, (TAmount, IID,))
            self.conn.commit()
            return tid
        except psycopg2.Error as e :
            print(e)
            self.conn.rollback()

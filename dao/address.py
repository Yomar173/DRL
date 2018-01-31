from config.dbconfig import pg_config, url_conn
import psycopg2

class AddressDAO:
    def __init__(self):
        connection_url = url_conn
        self.conn = psycopg2._connect(connection_url)

    def insertAddress(self, aid, country, state, city, neighborhood, street, number, zipcode):
        if self.getAddressByAID(aid):
            addr = self.changeAddress(aid, country, state, city, neighborhood, street, number, zipcode)
        else:
            addr = self.insert(aid,country, state,city,neighborhood,street,number,zipcode)
        return addr

    def changeAddress(self, aid, country, state, city, neighborhood, street, number, zipcode):
        self.delete(aid)
        addr = self.insert(aid,country,state,city,neighborhood,street,number,zipcode)
        return addr


    def delete(self, AID):
        cursor = self.conn.cursor()
        query = "UPDATE Address set IsHidden=True WHERE AID=%s AND IsHidden=False returning *;"
        cursor.execute(query,(AID,))
        self.conn.commit()
        return AID

    def insert(self, aid, country, state, city, neighborhood, street, number, zipcode):
        cursor = self.conn.cursor()
        query = "INSERT INTO Address(adcountry,adstate,rcity,adneighborhood,adstreet,adnumber,ADZipCode,ishidden,aid)"\
                " Values(%s,%s,%s,%s,%s,%s,%s, False,%s) returning *;"
        cursor.execute(query,(country,state, city,neighborhood,street,number,zipcode,aid))
        addr = cursor.fetchone()
        self.conn.commit()
        return addr

    def update(self, aid, country, state, city, neighborhood, street, number, zipcode):
        cursor = self.conn.cursor()
        query = "UPDATE Address SET adcountry=%s, adstate=%s, rcity=%s, adneighborhood=%s, adstreet=%s, adnumber =%s, adzipcode=%s "\
                "WHERE AID=%s AND ishidden=false returning *;"

        cursor.execute(query, (country,state,city,neighborhood,street,number,zipcode, aid))
        addr = cursor.fetchone()
        self.conn.commit()
        return addr

    def getAddressByAID(self, id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM Address WHERE AID=%s AND IsHidden=False;"
        cursor.execute(query,(id,))
        return cursor.fetchone()

from datetime import datetime

from config.dbconfig import pg_config, url_conn
import psycopg2


class AccountDao:

    def __init__(self):
        #Connect to Database
        connection_url = url_conn
        self.conn = psycopg2.connect(connection_url) # verify if is _connect

    # Retrieve all the accounts...
    def getAccounts(self):
        cursor = self.conn.cursor()
        query = "select AID, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone, " \
                "ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode " \
                "from account natural inner join address;" # Get all Accounts...
        cursor.execute(query)
        result = []
        for row in cursor :
            result.append(row)
        return result

    # Retrieve an account by AID...
    def getAccountByID(self, id):
        cursor = self.conn.cursor()
        query = "select AID, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone, " \
                "ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode " \
                "from account natural inner join address " \
                "where AID = %s;" # Get the Account whose account has the input AID.
        cursor.execute(query, (id,))
        account = cursor.fetchone()
        result = []
        result.append(account)
        return result


    def getAccountsByCity(self, city):
        cursor = self.conn.cursor()
        query = "select AID, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone, " \
                "ADCountry, ADState, RCity, ADNeighborhood, ADStreet, ADNumber, ADZipCode " \
                "from account natural inner join address " \
                "where RCity = %s" # Get all Accounts whose account has an address in the input city.
        cursor.execute(query, (city,))
        result = []
        for row in cursor :
            result.append(row)
        return result

    def insert_account(self, AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone): # Creating a new account...
        cursor = self.conn.cursor()
        query = "insert into Account(AName, ALastName, AEmail, AGender, ABDate, APPhone, ASPhone) values (%s, %s, %s, %s, %s, %s, %s);"
        try :
            cursor.execute(query, (AName, ALastName, AEmail, AGender, self.get_date(ABDate), APPhone, ASPhone,)) # Creating the new account...
            cursor.execute('SELECT LASTVAL()')
            AID = cursor.fetchone()[0]
            print(AID)
            self.conn.commit()
            return AID

        except psycopg2.Error as e:
            print (e)
            return None

    def get_date(self, date):
        date = datetime.strptime(date, '%d%b%Y')
        return date

if __name__ == '__main__':
    # dao = AccountDao()
    # allAccounts = dao.getAccounts()
    # account1 = dao.getAccountByID(1)
    # accountsInSanJuan = dao.getAccountsByCity("San Juan")
    #
    # for row in allAccounts : print(row)
    # print()
    # for row in account1 : print(row)
    # print()
    # for row in accountsInSanJuan : print(row)
    print(AccountDao().get_date("01Sep1996"))

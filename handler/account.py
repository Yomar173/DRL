from flask import jsonify

from dao.account import AccountDao

class AccountHandler:

    def getAllAccounts(self):
        dao = AccountDao()
        data = dao.getAccounts()
        data = self.buildAccountDictionaries(data)
        if len(data) == 0: return jsonify(ERROR = "Accounts not found."), 404
        return jsonify(Account = data)


    def buildAccountDictionaries(self, data):
        if len(data) == 0 or data[0] == None :
            return []
        result = []
        for element in data:
            t = {
                'AID' : int(element[0]),
                'AName' : element[1],
                'ALastName' : element[2],
                'AEmail' : element[3],
                'AGender' : element[4],
                'ABDate' : element[5],
                'APPhone' : element[6],
                'ASPhone' : element[7],
                'ADCountry' : element[8],
                'ADState' : element[9],
                'RCity' : element[10],
                'ADNeighborhood' : element[11],
                'ADStreet' : element[12],
                'ADNumber' : element[13],
                'ADZipCode' : element[14]
            }
            result.append(t)
        return result

    # def searchAccount(self, args):


    def getAccountByID(self, id):
        dao = AccountDao()
        data = dao.getAccountByID(id)
        data = self.buildAccountDictionaries(data)
        if len(data) == 0: return jsonify(ERROR="Account not found."), 404
        return jsonify(Account = data)

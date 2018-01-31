from flask import jsonify

from dao.buyer import BuyerDao


class BuyerHandler :

    def getBuyers(self) :
        dao = BuyerDao()
        data = dao.getBuyers()
        data = self.buildBuyerDictionaries(data)
        if len(data) == 0 : return jsonify(ERROR = "Buyers not found."), 404
        return jsonify(Buyer = data)


    def getFrom(self, city) :
        dao = BuyerDao()
        data = dao.getBuyersByCity(city)
        data = self.buildBuyerDictionaries(data)
        if len(data) == 0 : return jsonify(ERROR = "Buyers not found."), 404
        return jsonify(Buyer = data)

    def getBuyerByID(self, id) :
        dao = BuyerDao()
        data = dao.getBuyerByID(id)
        data = self.buildBuyerDictionaries(data)
        print(len(data))
        if len(data) == 0: return jsonify(ERROR="Buyer not found."), 404
        return jsonify(Buyer = data)

    def getBuyerRequests(self, id) :
        dao = BuyerDao()
        data = dao.getBuyerRequests(id)
        data = self.buildBuyerRequestsDictionaries(data)
        if len(data) == 0 : return jsonify(ERROR = "Requests not found"), 404
        return jsonify(BuyerRequest = data)

    def getBuyerPurchases(self, BID):
        dao = BuyerDao()
        data = dao.getBuyerTransactions(BID)
        data = self.buildBuyerTransactionsDictionaries(data)
        if len(data) == 0 : return jsonify(ERROR = "Transactions not found"), 404
        return jsonify(BuyerTransactions = data)

    def getDonations(self, BID):
        dao = BuyerDao()
        data = dao.getBuyerDonations(BID)
        data = self.buildBuyerTransactionsDictionaries(data)
        if len(data) == 0 : return jsonify(ERROR = "Donations not found"), 404
        return jsonify(BuyerDonations = data)

    def findPurchases(self, BID):
        dao = BuyerDao()
        data = dao.getBuyerPurchases(BID)
        data = self.buildBuyerTransactionsDictionaries(data)
        if len(data) == 0 : return jsonify(ERROR = "Purchases not found"), 404
        return jsonify(BuyerPurchases = data)

    def buildBuyerDictionaries(self, data) : # Dictionary must be updated (according to the DB output)...
        if len(data) == 0 or data[0] == None :
            return []
        result = []
        for element in data:
            t = {
                'BID' : int(element[0]),
                'BName' : element[1],
                'BLastName' : element[2],
                'BEmail' : element[3],
                'BGender' : element[4],
                'BBDate' : element[5],
                'BPPhone': element[6],
                'BSPhone': element[7],
                'BCountry' : element[8],
                'BState' : element[9],
                'BCity' : element[10],
                'BNeighborhood' : element[11],
                'BStreet' : element[12],
                'BNumber' : element[13],
                'BZipCode' : element[14]
            }
            result.append(t)
        return result

    def buildBuyerRequestsDictionaries(self, data) :
        if len(data) == 0 or data[0] == None :
            return []
        result = []
        for element in data:
            t = {
                'BID' : int(element[0]),
                'BName' : element[1],
                'BLastName' : element[2],
                'BEmail' : element[3],
                'BGender' : element[4],
                'BPPhone' : element[5],
                'BCountry': element[6],
                'BState': element[7],
                'BCity' : element[8],
                'ReID' : element[9],
                'ReQTY' : element[10],
                'ReDate' : element[11],
                'RID' : element[12],
                'RName' : element[13],
                'RBrand' : element[14]
            }
            result.append(t)
        return result

    def buildBuyerTransactionsDictionaries(self, data) :
        if len(data) == 0 or data[0] == None :
            return []
        result = []
        for element in data:
            t = {
                'BID' : int(element[0]),
                'BName' : element[1],
                'BLastName' : element[2],
                'BEmail' : element[3],
                'BCountry' : element[4],
                'BState' : element[5],
                'BCity': element[6],
                'SID': element[7],
                'SName' : element[8],
                'SLastName' : element[9],
                'SCompany' : element[10],
                'TID' : element[11],
                'TDate' : element[12],
                'TAmount' : element[13],
                'TPrice' : element[14],
                'RID' : element[15],
                'RName' : element[16],
                'RBrand' : element[17]
            }
            result.append(t)
        return result


    def build_card_dictionary(self, data):
        if len(data) != 6 or data[0] == None:
            return []
        result = []
        t = {
            'CID': int(data[0]),
            'CFullName': data[1],
            'CNumber': data[2],
            'CSCode': data[3],
            'BID': data[4],
            'CExpDate': data[5],
        }
        result.append(t)
        return result

    def update_credit_card(self, bid, cnumber, args):
        dao = BuyerDao()
        card = None
        try :
            CFullName = args['CFullName']
        except KeyError as e :
            CFullName = None
        try :
            CSCode = args['CSCode']
        except KeyError as e :
            CSCode = None
        try :
            CExpDate = args['CExpDate']
        except KeyError as e :
            CExpDate = None
        if len(args) == 1 :
            if CFullName :
                card = dao.update_card_CFullName(bid, cnumber, CFullName)
            elif CSCode :
                card = dao.update_card_CSCode(bid, cnumber, CSCode)
            elif CExpDate :
                card = dao.update_card_CExpDate(bid, cnumber, CExpDate)
        elif len(args) == 2 :
            if CFullName and CSCode :
                card = dao.update_card_CFullName_CSCode(bid, cnumber, CFullName, CSCode)
            elif CFullName and CExpDate :
                card = dao.update_card_CFullName_CExpDate(bid, cnumber, CFullName, CExpDate)
            elif CSCode and CExpDate :
                card = dao.update_card_CSCode_CExpDate(bid, cnumber, CSCode, CExpDate)
        elif len(args) == 3 :
            if CFullName and CSCode and CExpDate :
                card = dao.update_all(bid, cnumber, CFullName, CSCode, CExpDate)
        if card :
            card = dao.get_card_info(card)
            card = self.build_card_dictionary(card)
            return jsonify(Card = card)
        return jsonify(ERROR = 'Malformed URL.'), 404

    def add_credit_card(self, bid, args):
        if len(args) != 5 :
            return jsonify(ERROR='Malformed URL.'), 404
        try :
            CFullName = args['CFullName']
            CNumber = args['CNumber']
            CType = args['CType']
            CSCode = args['CSCode']
            CExpDate = args['CExpDate']
        except KeyError :
            return jsonify(ERROR='Malformed URL.'), 404
        dao = BuyerDao()
        card = dao.insert_card(bid, CFullName, CNumber, CType, CSCode, CExpDate)
        if card :
            card = dao.get_card_info(card)
            card = self.build_card_dictionary(card)
            return jsonify(Card = card), 201
        return jsonify(ERROR='Malformed URL.'), 404

#Yomar________________________________________________________________________________________________________
    def _build_account_dict(self, row):
        result = {}
        result['AID'] = row[0]
        result['AName'] = row[1]
        result['ALastName'] = row[2]
        result['AEmail'] = row[3]
        result['AGender'] = row[4]
        result['ABDate'] = row[5]
        result['APPhone'] = row[6]
        result['ASPhone'] = row[7]
        return result

    def insertBuyer(self, form):
        if form:
            dao = BuyerDao()
            name = form.get('AName')
            lname = form.get('ALastName')
            email = form.get('AEmail')
            gender = form.get('AGender')
            birthdate = form.get('ABDate')
            phone = form.get('APPhone')
            sphone = form.get('ASPhone')
            if name and lname and email and gender and birthdate and phone:
                buyer = dao.insertBuyer(name,lname,email,gender,birthdate,phone, sphone)
                account = self._build_account_dict(buyer)
                return jsonify(Buyer = account), 201
            else:
                return jsonify(Error="Malformed post request"), 400
        else:
            return jsonify(Error="Malformed post request"), 400


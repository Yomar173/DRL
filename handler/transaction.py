from dao.transaction import TransactionDAO
from flask import jsonify

class TransactionHandler:
    def build_transaction_dict(self,row):
        result = {}
        result['TID'] = row[0]
        result['TDate'] = row[1]
        result['TAmount'] = row[2]
        result['TPrice'] = row[3]
        result['BID'] = row[4]
        result['SID'] = row[5]
        result['RID'] = row[6]
        result['CID'] = row[7]
        result['ReID'] = row[7]
        return result

    def getAllTransactions(self):
        dao = TransactionDAO()
        transaction_list = dao.getAllTransactions()
        result_list = []
        for row in transaction_list:
            result = self.build_transaction_dict(row)
            result_list.append(result)
        return jsonify(Transactions=result_list)

    def getTransactionsBySID(self, sid):
        dao = TransactionDAO()
        transactionList = dao.getTransactionBySID(sid)
        resultList = []
        for row in transactionList:
            result = self.build_transaction_dict(row)
            resultList.append(result)
        return jsonify(Transactions = resultList)

    def purchase(self, args):
        if len(args) != 4 :
            return jsonify(ERROR='Malformed URL.'), 404
        try :
            TAmount = args['TAmount']
            BID = args['BID']
            CID = args['CID']
            IID = args['IID']
        except KeyError :
            return jsonify(ERROR='Malformed URL.'), 404
        dao = TransactionDAO()
        transaction = dao.insert_transaction(TAmount, BID, CID, IID)
        if transaction :
            transaction = dao.get_transaction(transaction)
            transaction = self.build_transaction_dict(transaction)
            return jsonify(Transaction = transaction), 201
        return jsonify(ERROR='Malformed URL.'), 404

    def purchase_donation(self, args):
        if len(args) != 4 :
            return jsonify(ERROR='Malformed URL.'), 404
        try :
            TAmount = args['TAmount']
            BID = args['BID']
            CID = args['CID']
            IID = args['IID']
        except KeyError :
            return jsonify(ERROR='Malformed URL.'), 404
        dao = TransactionDAO()
        transaction = dao.insert_donation(TAmount, BID, CID, IID)
        if transaction :
            transaction = dao.get_transaction(transaction)
            transaction = self.build_transaction_dict(transaction)
            return jsonify(Transaction = transaction), 201
        return jsonify(ERROR='Malformed URL.'), 404

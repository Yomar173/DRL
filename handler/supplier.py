from flask import jsonify

from dao.account import AccountDao
from dao.supplier import SupplierDAO
from handler.transaction import TransactionHandler

class SupplierHandler:
    def build_supplier_dict(self,row):
        result = {}
        result['SID'] = int(row[0])
        result['SName'] = row[1]
        result['SLastName'] = row[2]
        result['SCompany'] = row[3]
        result['SCity'] = row[4]
        result['SState'] = row[5]
        result['SEmail'] = row[6]
        result['SPrimaryPhone'] = row[7]
        return result

    def build_resource_dict(self,row):
        result = {}
        result['RID'] = int(row[0])
        result['RName'] = row[1]
        result['RBrand'] = row[2]
        result['RCategory'] = row[3]
        result['RSubCategory'] = row[4]
        result['RQty'] = row[5]
        result['RPrice'] = row[6]
        result['SID'] = row[7]
        result['SName'] = row[8]
        result['SLastName'] = row[9]
        result['SCompany'] = row[10]
        result['SCity'] = row[11]
        result['SState'] = row[12]
        return result

    def getAllSupplier(self):
        dao = SupplierDAO()
        supplier_list = dao.getAllSupplier()
        result_list = []
        for row in supplier_list:
            result = self.build_supplier_dict(row)
            result_list.append(result)
        return jsonify(Supplier=result_list)

    def getSupplierByID(self, sid):
        dao = SupplierDAO()
        row = dao.getSupplierByID(sid)
        if not row:
            return jsonify(Error="Supplier Not Found"), 404
        else:
            supplier = self.build_supplier_dict(row)
            return jsonify(Supplier=supplier)

    def getResourceBySupplierId(self, rid):
        dao = SupplierDAO()
        supplier_list = dao.getResourceBySupplierId(rid)
        result_list = []
        if not supplier_list:
            return jsonify(Error="Resource Not Found"), 404
        for row in supplier_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def searchSupplier(self, args):
        dao = SupplierDAO()
        city = args.get('SCity')
        company = args.get('SCompany')
        name = args.get('SName')
        if (len(args) == 1) and city:
            supplier_list = dao.getSupplierByCity(city)
        elif (len(args) == 1) and company:
            supplier_list = dao.getSupplierByCompany(company)
        elif (len(args) == 1) and name:
            supplier_list = dao.getSupplierByName(name)
        elif (len(args) == 2) and city and company:
            supplier_list = dao.getSupplierByCityAndCompany(city,company)
        elif (len(args) == 2) and city and name:
            supplier_list = dao.getSupplierByCityAndName(city,name)
        elif (len(args) == 2) and name and company:
            supplier_list = dao.getSupplierByCompanyAndName(company,name)
        elif (len(args) == 3) and city and company and name:
            supplier_list = dao.getSupplierByCityAndCompanyAndName(city,company,name)
        else:
            return jsonify(Error="Malformed query string"), 400
        if not supplier_list:
            return jsonify(Error="Supplier Not Found"), 404
        result_list = []
        for row in supplier_list:
            result = self.build_supplier_dict(row)
            result_list.append(result)
        return jsonify(Supplier=result_list)

    def getAllOrders(self, sid):
        dao = SupplierDAO()
        supplier = dao.getSupplierByID(sid)
        if not supplier:
            return jsonify("Supplier Not Found"),404
        transactions = TransactionHandler().getTransactionsBySID(sid)
        return transactions

    def insert_supplier(self, form):
        if form : # Insert Supplier with SCompany...
            if len(form) == 20 :
                SCompany = form['SCompany']
                SName = form['SName']
                SLastName = form['SLastName']
                SEmail = form['SEmail']
                SGender = form['SGender']
                SBDate = form['SBDate']
                SPPhone = form['SPPhone']
                SSPhone = form['SSPhone']
                CFullName = form['CFullName']
                CNumber = form['CNumber']
                CType = form['CType']
                CSCode = form["CSCode"]
                CExpDate = form['CExpDate']
                ADCountry = form['ADCountry']
                ADState = form['ADState']
                RCity = form['RCity']
                ADNeighborhood = form['ADNeighborhood']
                ADStreet = form['ADStreet']
                ADNumber = form['ADNumber']
                ADZipCode = form['ADZipCode']
                if SCompany and SName and SLastName and SEmail and SGender and SBDate and SPPhone and SSPhone \
                    and CFullName and CNumber and CType and CSCode and CExpDate and ADCountry and ADState \
                    and RCity and ADNeighborhood and ADStreet and ADNumber and ADZipCode : # All requirements...

                    dao = SupplierDAO()
                    sid = dao.insert_supplier(SCompany, SName, SLastName, SEmail, SGender, SBDate, SPPhone, SSPhone,
                                              CFullName, CNumber, CType, CSCode, CExpDate, ADCountry, ADState, RCity,
                                              ADNeighborhood, ADStreet, ADNumber, ADZipCode)
                    if sid :
                        return self.getSupplierByID(sid)

            if len(form) == 19 : # Insert Supplier without SCompany... # *** TO BE TESTED...
                SName = form['SName']
                SLastName = form['SLastName']
                SEmail = form['SEmail']
                SGender = form['SGender']
                SBDate = form['SBDate']
                SPPhone = form['SPPhone']
                SSPhone = form['SSPhone']
                CFullName = form['CFullName']
                CNumber = form['CNumber']
                CType = form['CType']
                CSCode = form["CSCode"]
                CExpDate = form['CExpDate']
                ADCountry = form['ADCountry']
                ADState = form['ADState']
                RCity = form['RCity']
                ADNeighborhood = form['ADNeighborhood']
                ADStreet = form['ADStreet']
                ADNumber = form['ADNumber']
                ADZipCode = form['ADZipCode']
                if SName and SLastName and SEmail and SGender and SBDate and SPPhone and SSPhone \
                    and CFullName and CNumber and CType and CSCode and CExpDate and ADCountry and ADState \
                    and RCity and ADNeighborhood and ADStreet and ADNumber and ADZipCode : # All requirements...

                    dao = SupplierDAO()
                    sid = dao.insert_supplier_no_company(SName, SLastName, SEmail, SGender, SBDate, SPPhone, SSPhone,
                                              CFullName, CNumber, CType, CSCode, CExpDate, ADCountry, ADState, RCity,
                                              ADNeighborhood, ADStreet, ADNumber, ADZipCode)
                    if sid :
                        return self.getSupplierByID(sid)
        return jsonify(ERROR="Malformed POST Request"), 400

    def update_credit_card(self, sid, cnumber, args):
        dao = SupplierDAO()
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
                card = dao.update_card_CFullName(sid, cnumber, CFullName)
            elif CSCode :
                card = dao.update_card_CSCode(sid, cnumber, CSCode)
            elif CExpDate :
                card = dao.update_card_CExpDate(sid, cnumber, CExpDate)
        elif len(args) == 2 :
            if CFullName and CSCode :
                card = dao.update_card_CFullName_CSCode(sid, cnumber, CFullName, CSCode)
            elif CFullName and CExpDate :
                card = dao.update_card_CFullName_CExpDate(sid, cnumber, CFullName, CExpDate)
            elif CSCode and CExpDate :
                card = dao.update_card_CSCode_CExpDate(sid, cnumber, CSCode, CExpDate)
        elif len(args) == 3 :
            if CFullName and CSCode and CExpDate :
                card = dao.update_all(sid, cnumber, CFullName, CSCode, CExpDate)
        if card :
            card = dao.get_card_info(card)
            card = self.build_card_dictionary(card)
            return jsonify(Card = card)
        return jsonify(ERROR = 'Malformed URL.'), 404


    def build_card_dictionary(self, data):
        if len(data) != 6 or data[0] == None:
            return []
        result = []
        t = {
            'CID': int(data[0]),
            'CFullName': data[1],
            'CNumber': data[2],
            'CSCode': data[3],
            'SID': data[4],
            'CExpDate': data[5],
        }
        result.append(t)
        return result

    def add_credit_card(self, sid, args):
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
        dao = SupplierDAO()
        card = dao.insert_card(sid, CFullName, CNumber, CType, CSCode, CExpDate)
        if card :
            card = dao.get_card_info(card)
            card = self.build_card_dictionary(card)
            return jsonify(Card = card)
        return jsonify(ERROR='Malformed URL.'), 404



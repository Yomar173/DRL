from flask import jsonify
from dao.account import AccountDao
from dao.address import AddressDAO

class AddressHandler:

    def _build_addr_dict(self, row):
        result = {}
        result['ADID'] = row[0]
        result['ADCountry'] = row[1]
        result['ADState'] = row[2]
        result['RCity'] = row[3]
        result['ADNeighborhood'] = row[4]
        result['ADStreet'] = row[5]
        result['ADNumber'] = row[6]
        result['ADZipCode'] = row[7]
        result['IsHidden'] = row[8]
        result['AID'] = row[9]
        return result

    def updateAddress(self, aid, form):
        dao = AccountDao()
        if not dao.getAddressByID(aid):
            return jsonify(Error = "Account not found."), 404
        if form:
             country = form.get('ADCountry')
             state = form.get('ADState')
             city = form.get('RCity')
             neighborhood = form.get('ADNeighborhood')
             street = form.get('ADStreet')
             number = form.get('ADNumber')
             zip = form.get('ADZipCode')
             if country and state and city and street and zipcode:
                 addr = dao.updateAddress(aid, country, state, city, neighborhood,street,number,zip)
                 result = self._build_addr_dict(addr)
                 return jsonify(Address = result),200
             else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def insertAddress(self, aid, form):
        if AccountDao().getAccountByID(aid):
            if form and len(form)>=5:
                 country = form.get('ADCountry')
                 state = form.get('ADState')
                 city = form.get('RCity')
                 neighborhood = form.get('ADNeighborhood')
                 street = form.get('ADStreet')
                 number = form.get('ADNumber')
                 zip = form.get('ADZipCode')
                 if country and state and city and street and zip:
                     dao = AddressDAO()
                     addr = dao.insertAddress(aid, country, state, city, neighborhood,street,number,zip)
                     result = self._build_addr_dict(addr)
                     return jsonify(Address = result), 201
                 else:
                     return jsonify(Error="Unexpected attributes in post request"), 400
            return jsonify(Error = "Malformed post request"), 400
        else:
            return jsonify(Error = "Account not Found."), 404


    def updateAddress(self,aid, form):
        if AccountDao().getAccountByID(aid):
            if form and len(form)>=5:
                 country = form.get('ADCountry')
                 state = form.get('ADState')
                 city = form.get('RCity')
                 neighborhood = form.get('ADNeighborhood')
                 street = form.get('ADStreet')
                 number = form.get('ADNumber')
                 zip = form.get('ADZipCode')
                 if country and state and city and street and zip:
                     dao = AddressDAO()
                     addr = dao.update(aid, country, state, city, neighborhood,street,number,zip)
                     result = self._build_addr_dict(addr)
                     return jsonify(Address = result), 201
                 else:
                     return jsonify(Error="Unexpected attributes in post request"), 400
            return jsonify(Error = "Malformed post request"), 400
        else:
            return jsonify(Error = "Account not Found."), 404

    def getAddressByAID(self, id):
        if AccountDao().getAccountByID(id):
            dao = AddressDAO()
            addr = dao.getAddressByAID(id)
            return jsonify(Address = self._build_addr_dict(addr)), 201
        else:
            return jsonify(Error = "Account not Found."), 404

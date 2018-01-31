from flask import jsonify

from dao.account import AccountDao
from dao.supplier import SupplierDAO
from dao.request import RequestDAO
from handler.account import AccountHandler


class RequestHandler:

	def _build_request_dict(self, row):
		result = {}
		result['RID'] = row[1]
		result['ReID'] = row[2]
		result['ReQty'] = row[3]
		result['ReDate'] = row[4]
		result['BID'] = row[5]
		result['IsHidden'] = row[6]
		result['IsCompleted'] = row[7]
		result['RName'] = row[8]
		result['RBrand'] = row[9]
		result['RType'] = row[10]
		result['RSubcategory'] = row[11]
		return result

	def getAllRequest(self):
		dao = RequestDAO()
		requestList = dao.getAllRequest()
		resultList = []
		for row in requestList:
			result = self._build_request_dict(row)
			resultList.append(result)
		return jsonify(Requests = resultList)

	def getRequestByID(self, rid):
		dao = RequestDAO()
		request = dao.getRequestById(rid)
		if not request:
			return jsonify(Error = "Request Not Found"), 404
		else:
            		result = self._build_request_dict(request)
            		return jsonify(Request = result)

	def searchRequest(self, args):
		dao = RequestDAO()
		resultList = []
		if (len(args) == 0):
			return jsonify(Error = "Malformed query string"), 400
		else:
			requestList = dao.getRequestByKeyword(args)
		if not requestList:
			return jsonify(Error = "Request Not Found"), 404
		for row in requestList:
			result = self._build_request_dict(row)
			resultList.append(result)

		return jsonify(Requests = resultList)

	def getRequestByBID(self, bid):
		adao = AccountDao()
		buyer = adao.getBuyerByID(bid)
		if not buyer:
			return jsonify(ERROR = 'Buyer Not Found'),404
		dao = RequestDAO()
		requestList = dao.getRequestByBID(bid)
		resultList = []
		for row in requestList:
			result = self._build_request_dict(row)
			resultList.append(result)
		for dict in resultList:#Why?
			dict['AName'] = AccountHandler().getFNameByID(bid)
			dict['ALastName'] = AccountHandler().getLNameByID(bid)
		return jsonify(Requests = resultList)


	def insertRequest(self, form):
		if len(form) != 3 :
			return jsonify(Error = "Malformed post request"), 400
		else:
			ReQty = form.get('ReQty')
			BID = form.get('BID')
			RID = form.get('RID')
			if ReQty and BID and RID:
				dao = RequestDAO()
				req = dao.insert(ReQty, BID, RID)
				result = self._build_request_dict(req)
				return jsonify(Request=result), 201
			else:
				return jsonify(Error="Unexpected attributes in post request"), 400

	def deleteRequest(self, ReqID):
		dao = RequestDAO()
		if not dao.getRequestById(ReqID):
			return jsonify(Error = "Request not found."), 404
		else:
			dao.delete(ReqID)
			return jsonify(DeleteStatus = "OK"), 200

	def updateRequest(self, reqid, form):
		dao = RequestDAO()
		if not dao.getRequestByID(reqid):
			return jsonify(Error = "Request not found."), 404
		else:
			if len(form) > 2 or len(form) == 0:
				return jsonify(Error="Malformed update request"), 400
			else:
				rid = form.get('RID')
				reqty = form.get('ReQty')
				bid = form.get('BID')
				if rid or reqty or bid:
					req = dao.update(reqid, rid, reqty, bid)
					result = self._build_request_dict(req)
					return jsonify(Request=result), 200
				else:
					return jsonify(Error="Unexpected attributes in update request"), 400

if __name__ == '__main__':
	handler = RequestHandler()
	content = handler.getAllRequests()
	print(content)
	content = handler.getRequestById(3)
	print(content)
	content = handler.searchRequest({'category': 'Canned Food'})
	print(content)
	content = handler.searchRequest({'name': 'Tuna'})
	print(content)

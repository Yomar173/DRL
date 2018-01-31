from flask import Flask, jsonify, request

from handler.Handlers import PersonHandler
from handler.buyer import BuyerHandler
from handler.resource import ResourceHandler
from handler.request import RequestHandler
from handler.supplier import SupplierHandler
from handler.account import AccountHandler
from handler.transaction import TransactionHandler
from handler.dashboard import DashboardHandler
from handler.address import AddressHandler

application = Flask(__name__)

@application.route("/DRL_Backend/")
def hello():
    return "<h1>Thanks for using DRL Services.</h1><h2>This consists on the first phase of the ICOM 5016 Introduction to Database Systems.</h2><h3>Authors: Keila Enid Hernandez Rivera, Pedro Luis Rivera Gomez, Yomar Ruiz Santos.</h3><h4>12/05/2017</h4>"

@application.route("/DRL_Backend/Account/")
def accounts():
    if(not request.args) : return AccountHandler().getAllAccounts()
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Account/<int:id>/")
def findByID(id):
    if(not request.args) :
        return AccountHandler().getAccountByID(id)
    return jsonify(Error = "Malformed URL"), 404

@application.route("/DRL_Backend/Buyer/<int:id>/Request/")
def findrequests(id):
    if(not request.args) :
        return BuyerHandler().getBuyerRequests(id) # MODS TO BE CONSIDERED...
    return jsonify(Error = "Malformed URL"), 404
"""
@application.route("/DRL_Backend/Buyer/")
def person():
    if(not request.args) : return BuyerHandler().getBuyers()
    return jsonify(ERROR = "Malformed URL"), 404
"""

@application.route("/DRL_Backend/Buyer/<string:city>/")
def findByCity(city):
    if(not request.args) : return BuyerHandler().getFrom(city)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Buyer/<int:BID>/")
def findPerson(BID):
    if (not request.args) : return BuyerHandler().getBuyerByID(BID)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Buyer/<int:BID>/Transaction/")
def findPurchases(BID):
    if(not request.args) : return BuyerHandler().getBuyerPurchases(BID)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Buyer/<int:BID>/Transaction/Donation/")
def findDonations(BID) :
    if(not request.args) : return BuyerHandler().getDonations(BID)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Buyer/<int:BID>/Transaction/Purchase/")
def findPurchase(BID) :
    if(not request.args) : return BuyerHandler().findPurchases(BID)
    return jsonify(ERROR = "Malformed URL"), 404


@application.route("/DRL_Backend/Buyer/<int:bid>/<string:cnumber>/", methods = ['PUT']) # I'm here
def updateBuyerCreditCard(bid, cnumber) :
    if request.method == 'PUT' :
        return BuyerHandler().update_credit_card(bid, cnumber, request.args)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Buyer/<int:bid>/AddCreditCard/", methods = ['POST'])
def addBuyerCredicCard(bid) :
    if request.method == 'POST' :
        return BuyerHandler().add_credit_card(bid, request.args)
    return jsonify(ERROR = "Malformed URL"), 404


@application.route('/DRL_Backend/Resource/', methods = ['GET', 'POST']) # Working Here ...
def getAllResources():
    if request.method == 'POST':
        return ResourceHandler().insertResource(request.args)
    if not request.args:
        return ResourceHandler().getAllResources()
    return ResourceHandler().searchResource(request.args)

@application.route('/DRL_Backend/Resource/<int:rid>/')
def getResourceById(rid):
    return ResourceHandler().getResourceByID(rid)

@application.route('/DRL_Backend/Resource/<int:rid>/Suppliers/')
def getSuppliersByResourceId(rid):
    if not request.args:
        return ResourceHandler().getSupplierByResourceID(rid)
    return ResourceHandler().searchSupplierByResourceID(rid, request.args)

@application.route('/DRL_Backend/Resource/Available/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def getAvailableResources():
    if request.method == 'POST':
        return ResourceHandler().insertAvailableResource(request.args)
    if request.method == 'PUT':
        return ResourceHandler().updateInventory(request.args)
    if request.method == 'DELETE':
        return ResourceHandler().hideResource(request.args)
    if not request.args:
        return ResourceHandler().getAvailableResources()
    return ResourceHandler().getAvailableResourcesByCity(request.args)

@application.route('/DRL_Backend/Resource/Available/<string:rcategory>/')
def getAvailableResourcesByCategory(rcategory):
    if not request.args:
        return ResourceHandler().getAvailableResourcesByCategory(rcategory)
    return ResourceHandler().getAvailableResourceByCategoryAndCity(rcategory, request.args)

@application.route('/DRL_Backend/Resource/Available/<string:rcategory>/<string:rsubcategory>/')
def getAvailableResourcesByCategoryAndSubCategory(rcategory, rsubcategory):
    if not request.args:
        return ResourceHandler().getAvailableResourcesByCategoryAndSubCategory(rcategory, rsubcategory)
    return ResourceHandler().getAvailableResourceByCategoryAndSubCategoryAndCity(rcategory, rsubcategory, request.args)

@application.route('/DRL_Backend/Resource/Need/')
def getResourcesInNeed():
    return ResourceHandler().getResourcesInNeed()


@application.route('/DRL_Backend/Resource/<int:rid>/Sales/')
def getSalesByResourceID(rid):
    return ResourceHandler().getSalesByResourceId(rid)

@application.route('/DRL_Backend/Resource/<int:rid>/TotalSales/')
def getTotalSalesByResourceID(rid):
    return ResourceHandler().getTotalSalesByResourceId(rid)
  
@application.route('/DRL_Backend/Supplier/', methods = ['GET', 'POST']) # Working here...
def getAllSupplier():
    if request.method == 'POST' :
        return SupplierHandler().insert_supplier(request.args)
    if not request.args:
        return SupplierHandler().getAllSupplier()
    return SupplierHandler().searchSupplier(request.args)

@application.route('/DRL_Backend/Supplier/<int:sid>/<string:cnumber>/', methods = ['PUT'])
def updateCreditCard(sid, cnumber) :
    if request.method == 'PUT' :
        return SupplierHandler().update_credit_card(sid, cnumber, request.args)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Supplier/<int:sid>/AddCreditCard/", methods = ['POST'])
def addSupplierCredicCard(sid) :
    if request.method == 'POST' :
        return SupplierHandler().add_credit_card(sid, request.args)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route('/DRL_Backend/Supplier/<int:sid>/')
def getSupplierById(sid):
    return SupplierHandler().getSupplierByID(sid)

@application.route('/DRL_Backend/Supplier/<int:sid>/Resources/')
def getResourceBySupplierId(sid):
    return SupplierHandler().getResourceBySupplierId(sid)

@application.route('/DRL_Backend/Transaction/')
def getAllTransactions():
    return TransactionHandler().getAllTransactions()

@application.route('/DRL_Backend/Dashboard/')
def getDashboard():
    return DashboardHandler().getDashboard()

@application.route('/DRL_Backend/Supplier/<int:sid>/Orders/')
def getOrdersBySupplierID(sid):
    return SupplierHandler().getAllOrders(sid)

@application.route('/DRL_Backend/Dashboard/Week/')
def getWeeklyStats():
    return "<h1>To be implemented in Phase 3. </h1>"

@application.route('/DRL_Backend/Dashboard/Month/')
def getMonthStats():
    return "<h1>To be implemented in Phase 3. </h1>"


@application.route("/DRL_Backend/Purchase/Donation/", methods = ['POST'])
def purchaseDonation() :
    if request.method == 'POST' :
        return TransactionHandler().purchase_donation(request.args)
    return jsonify(ERROR = "Malformed URL"), 404

@application.route("/DRL_Backend/Purchase/", methods = ['POST'])
def purchase() :
    if request.method == 'POST' :
        return TransactionHandler().purchase(request.args)
    return jsonify(ERROR = "Malformed URL"), 404

#Yomar__________________________________________________________________________________________________
@application.route("/DRL_Backend/Account/<int:id>/Address", methods=['GET','POST','PUT'])
def addressByID(id):
    if request.method=='GET':
        return AddressHandler().getAddressByAID(id)
    elif request.method == 'PUT':
        return AddressHandler().updateAddress(id, request.args)
    elif request.method == 'POST':
        return AddressHandler().insertAddress(id, request.args)
    else:
        return jsonify(Error="Method not allowed."), 405

@application.route("/DRL_Backend/Buyer/", methods=['GET', 'POST'])
def person():
    if request.method == 'POST' and request.args is not None:
        return BuyerHandler().insertBuyer(request.args)
    else:
        if(not request.args) : return BuyerHandler().getBuyers()
        return jsonify(ERROR = "Malformed URL"), 404

@application.route('/DRL_Backend/Request/', methods=['GET','POST'])
def getAllRequests():
    if request.method == 'POST':
        return RequestHandler().insertRequest(request.args)
    else:
        if not request.args:
            return RequestHandler().getAllRequest()
        return RequestHandler().searchRequest(request.args)

@application.route('/DRL_Backend/Request/<int:reqid>/', methods=['GET','PUT','DELETE'])
def getRequest(reqid):
    if request.method=='GET':
        RequestHandler.getRequestByID(reqid)
    elif request.method == 'PUT':
        return RequestHandler().updateRequest(reqid, request.args)
    elif request.method == 'DELETE':
        return RequestHandler().deleteRequest(reqid)
    else:
        return jsonify(Error="Method not allowed."), 405


# Launching the applicationlication...
if __name__ == '__main__':
    application.run()

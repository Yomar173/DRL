from flask import jsonify
from dao.resource import ResourceDAO



class ResourceHandler:
    def build_available_resource_dict(self,row):
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

    def build_resource_dict(self,row):
        result = {}
        result['RID'] = int(row[0])
        result['RName'] = row[1]
        result['RBrand'] = row[2]
        result['RCategory'] = row[3]
        return result

    def build_need_resource_dict(self,row):
        result = {}
        result['RID'] = int(row[0])
        result['RName'] = row[1]
        result['RBrand'] = row[2]
        result['Rqty'] = int(row[3])
        return result

    def build_supplier_dict(self, row):
        result = {}
        result['SID'] = int(row[0])
        result['SName'] = row[1]
        result['SLastName'] = row[2]
        result['SCompany'] = row[3]
        result['SCity'] = row[4]
        result['SState'] = row[5]
        result['SCountry'] = row[6]
        return result

    def build_resource_supplier_inventory_dict(self, row):
        result = {}
        result['SID'] = int(row[0])
        result['SName'] = row[1]
        result['SLastName'] = row[2]
        result['SCompany'] = row[3]
        result['SCity'] = row[4]
        result['SState'] = row[5]
        result['SCountry'] = row[6]
        result['RName'] = row[7]
        result['RQty'] = int(row[8])
        result['RPrice'] = float(row[9])
        result['RCondition'] = row[10]
        return result

    def build_resource_sales_dict(self, row):
        result = {}
        result['BID'] = int(row[0])
        result['BName'] = row[1]
        result['BLastName'] = row[2]
        result['BEmail'] =row[3]
        result['BCountry'] = row[4]
        result['BState'] = row[5]
        result['BCity'] = row[6]
        result['SID'] = row[7]
        result['SName'] = row[8]
        result['SLastName'] = row[9]
        result['SCompany'] = row[10]
        result['TID'] = row[11]
        result['TDate'] = row[12]
        result['TAmount'] = row[13]
        result['TPrice'] = row[14]
        result['RID'] = row[15]
        result['RName'] = row[16]
        result['RBrand'] = row[17]
        return result

    def build_total_sales_dict(self, row):
        result = {}
        result['SID'] = int(row[0])
        result['SCompany'] = row[1]
        result['SName'] = row[2]
        result['SLastName'] = row[3]
        result['SCity'] = row[4]
        result['RID'] = int(row[5])
        result['RName'] = row[6]
        result['RBrand'] = row[7]
        result['TotalSales'] = row[8]
        return result

    def getAllResources(self):
        dao = ResourceDAO()
        resource_list = dao.getAllResources()
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getResourceByID(self, rid):
        dao = ResourceDAO()
        row = dao.getResourceByID(rid)
        if not row:
            return jsonify(Error="Resource Not Found"), 404
        else:
            resource = self.build_resource_dict(row)
            return jsonify(Resource=resource)

    def getSupplierByResourceID(self, rid):
        dao = ResourceDAO()
        supplier_list = dao.getSupplierByResourceID(rid)
        result_list = []
        if not supplier_list:
            return jsonify(Error="Supplier Not Found"), 404
        for row in supplier_list:
            result = self.build_resource_supplier_inventory_dict(row)
            result_list.append(result)
        return jsonify(Supplier=result_list)

    def searchResource(self, args):
        dao = ResourceDAO()
        name = args.get('RName')
        category = args.get('RCategory')
        if (len(args) == 1) and name:
            resource_list = dao.getResourceByName(name)
        elif (len(args) == 1) and category:
            resource_list = dao.getResourceByCategory(category)
        elif (len(args) == 2) and name and category:
            resource_list = dao.getResourceByNameAndCategory(name,category)
        else:
            return jsonify(Error="Malformed query string"), 400
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getAvailableResources(self):
        dao = ResourceDAO()
        resource_list = dao.getAvailableResources()
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result =  self.build_available_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getAvailableResourcesByCity(self, args):
        dao = ResourceDAO()
        city = args.get('SCity')
        region = args.get('SRegion')
        resource_name = args.get('RName')
        resource_list = []
        if (len(args) == 1) and city:
            resource_list = dao.getAvailableResourcesByCity(city)
        elif (len(args) == 1) and region:
            resource_list = dao.getAvailableResourcesByRegion(region)
        elif (len(args) == 1) and resource_name:
            resource_list = dao.getAvailableResourcesByName(resource_name)
        elif (len(args) == 2) and resource_name and city:
            resource_list = dao.getAvailableResourcesByNameAndCity(resource_name, city)
        elif (len(args) == 2) and resource_name and region:
            resource_list = dao.getAvailableResourcesByNameAndRegion(resource_name, region)
        else:
            return jsonify(Error="Malformed query string"), 400
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result =  self.build_available_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getAvailableResourcesByCategory(self, resource_category):
        dao = ResourceDAO()
        resource_list = dao.getAvailableResourcesByCategory(resource_category)
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result =  self.build_available_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getAvailableResourcesByCategoryAndSubCategory(self, resource_category, resource_subcategory):
        dao = ResourceDAO()
        resource_list = dao.getAvailableResourcesByCategoryAndSubCategory(resource_category, resource_subcategory)
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result =  self.build_available_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getAvailableResourceByCategoryAndSubCategoryAndCity(self, resource_category, resource_subcategory, args):
        dao = ResourceDAO()
        city = args.get('SCity')
        resource_list =[]
        if (len(args) == 1) and city:
            resource_list = dao.getAvailableResourceByCategoryAndSubCategoryAndCity(resource_category, resource_subcategory, city)
        else:
            return jsonify(Error="Malformed query string"), 400
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result = self.build_available_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getResourcesInNeed(self):
        dao = ResourceDAO()
        resource_list = dao.getResourcesInNeed()
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result = self.build_need_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getAvailableResourceByCategoryAndCity(self, resource_category, args):
        dao = ResourceDAO()
        city = args.get('SCity')
        resource_list =[]
        if (len(args) == 1) and city:
            resource_list = dao.getAvailableResourceByCategoryAndCity(resource_category, city)
        else:
            return jsonify(Error="Malformed query string"), 400
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        result_list = []
        for row in resource_list:
            result = self.build_available_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def searchSupplierByResourceID(self, rid, args):
        dao = ResourceDAO()
        city = args.get('SCity')
        supplier_list = []
        if (len(args) == 1) and  city:
            supplier_list = dao.getSupplierByResourceIDAndCity(rid, city)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        if not supplier_list:
            return jsonify(Error="Supplier Not Found"), 404
        for row in supplier_list:
            result = self.build_resource_supplier_inventory_dict(row)
            result_list.append(result)
        return jsonify(Supplier=result_list)

    #Insert a resource to inventory
    def insertAvailableResource(self, form):
        if form and len(form)== 5:
            rqty = form['rqty']
            rprice = form['rprice']
            rcondition = form['rcondition']
            rid = form['rid']
            sid = form['sid']
            #isHidden = form['isHidden']
            if rqty and rprice and rcondition and rid and sid:
                dao = ResourceDAO()
                iid = dao.insertAvailableResource(rqty, rprice, rcondition, rid, sid)
                #change to a method that returns the resource name, price, supplier, condition and quantity.
                result = {}
                result['RQty'] = rqty
                result['RPrice'] = rprice
                result['RCondition'] = rcondition
                result['RID'] = rid
                result['SID'] = sid
                return jsonify(Resource=result), 201
            else:
                return jsonify(Error="Malformed post request"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

    #Insert a resource to dictionary
    def insertResource(self, form):
        if form and len(form)== 3:
            rname = form['rname']
            rbrand = form['rbrand']
            rtid = form['rtid']
            if rname and rbrand and rtid:
                dao = ResourceDAO()
                rid = dao.insertResource(rname, rbrand, rtid)
                #change to a method that returns the resource name, price, supplier, condition and quantity.
                result = self.getResourceByID(rid)
                return result, 201
            else:
                return jsonify(Error="Malformed post request"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

    #Remove a resource from the inventory
    def hideResource(self, form):
        if form and len(form)== 3:
            rid = form['rid']
            sid = form['sid']
            isHidden = form['isHidden']
            if rid and sid and isHidden:
                dao = ResourceDAO()
                dao.hideInventory(rid, sid, isHidden)
                result = {}
                result['RID'] = rid
                result['SID'] = sid
                return jsonify(Resource=result), 201
            else:
                return jsonify(Error="Malformed post request"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

    #Update inventory information / Remove a resource from the inventory
    def updateInventory(self, form):
        if form:
            rid = form.get('rid')
            sid = form.get('sid')
            rqty = form.get('rqty')
            rprice = form.get('rprice')
            rcondition = form.get('rcondition')
            isHidden = form.get('isHidden')
            result = {}
            dao = ResourceDAO()
            # if (len(form) == 3) and rid and sid and isHidden:
            #     dao.hideInventory(rid, sid, isHidden)
            #     result['RID'] = rid
            #     result['SID'] = sid
            #     result['isHidden'] = isHidden
            inventory_exist = dao.getInventoryBySIDAndRID(sid, rid)
            if not inventory_exist:
                return jsonify(Error='Inventory Not Found'), 404
            if (len(form) == 5) and rid and sid and rprice and rcondition and rqty:
                dao.updateInventoryQtyAndPriceAndCondition(rqty,rprice, rcondition, rid, sid)
                result['RID'] = rid
                result['SID'] = sid
                result['RQty'] = rqty
                result['RPrice'] = rprice
                result['RCondition'] = rcondition
            elif (len(form) == 4) and rid and sid and rprice and rcondition:
                dao.updateInventoryPriceAndCondition(rprice, rcondition, rid, sid)
                result['RID'] = rid
                result['SID'] = sid
                result['RPrice'] = rprice
                result['RCondition'] = rcondition
            elif (len(form) == 4) and rid and sid and rprice and rqty:
                dao.updateInventoryQtyAndPrice(rqty, rprice, rid, sid)
                result['RID'] = rid
                result['SID'] = sid
                result['RQty'] = rqty
                result['RPrice'] = rprice
            elif (len(form) == 4) and rid and sid and rcondition and rqty:
                dao.updateInventoryQtyAndCondition(rqty, rcondition, rid, sid)
                result['RID'] = rid
                result['SID'] = sid
                result['RQty'] = rqty
                result['RCondition'] = rcondition
            elif (len(form) == 3) and rid and sid and rprice:
                dao.updateInventoryPrice(rprice, rid, sid)
                result['RID'] = rid
                result['SID'] = sid
                result['RPrice'] = rprice
            elif (len(form) == 3) and rid and sid and rcondition:
                print('ENtra')
                dao.updateInventoryCondition(rcondition, rid, sid)
                result['RID'] = rid
                result['SID'] = sid
                result['RCondition'] = rcondition
            elif (len(form) == 3) and rid and sid and rqty:
                dao.updateInventoryQty(rqty, rid, sid)
                result['RID'] = rid
                result['SID'] = sid
                result['RQty'] = rqty
            else:
                return jsonify(Error="Malformed query string"), 400
            return jsonify(Resource=result), 201 #Returns tuple after update
        else:
            return jsonify(Error="Malformed post request"), 400

    def getSalesByResourceId(self, rid):
        dao = ResourceDAO()
        resource_list = dao.getSalesByResourceID(rid)
        result_list = []
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        for row in resource_list:
            result = self.build_resource_sales_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getTotalSalesByResourceId(self, rid):
        dao = ResourceDAO()
        resource_list = dao.getTotalSalesByResourceID(rid)
        result_list = []
        if not resource_list:
            return jsonify(Error="Resource Not Found"), 404
        for row in resource_list:
            result = self.build_total_sales_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

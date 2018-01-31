from config.dbconfig import pg_config, url_conn
from datetime import date
import psycopg2



class RequestDAO:
	def __init__(self):
		connection_url = url_conn
		self.conn = psycopg2._connect(connection_url)
		self.requestColumns = ['RID','ReID','ReQty','ReDate','BID','IsHidden','IsCompleted','RName','RType','RSubcategory']

	def getAllRequest(self):
		cursor = self.conn.cursor()
		paramDict = {}
		paramDict['IsHidden'] = False
		query,paramList = self._build_sql_statement(paramDict)
		cursor.execute(query,tuple(paramList))
		result = []
		for row in cursor:
			result.append(row)
		return result

	def getRequestById(self, reqid):
		cursor = self.conn.cursor()
		paramDict={}
		paramDict['ReID']=reqid
		query, paramList = self._build_sql_statement(paramDict)
		cursor.execute(query,tuple(paramList))
		result = cursor.fetchone()
		return result

	def getRequestByBID(self, bid):
		cursor = self.conn.cursor()
		paramDict = {}
		paramDict['BID']=bid
		query, paramList = self._build_sql_statement(paramDict)
		cursor.execute(query,tuple(paramList))
		resultList = []
		for row in cursor:
			resultList.append(row)
		return result

	def getRequestByKeyword(self, keywordDict):
		cursor = self.conn.cursor()
		query, paramList = self._build_sql_statement(keywordDict)
		cursor.execute(query,tuple(paramList))
		resultList = []
		for row in cursor:
			resultList.append(row)
		return resultList

	def insert(self, qty, bid, rid):
		cursor = self.conn.cursor()
		query = "INSERT INTO Request(ReQty, ReDate, BID, RID,IsHidden, IsCompleted)"\
				"values(%s,%s,%s,%s,'False','False') returning reid;"
		cursor.execute(query,(qty,date.today(),bid,rid))
		request = cursor.fetchone()[0]
		self.conn.commit()
		request = self.getRequestById(request)
		return request

	def delete(self, ReqID):
		cursor = self.conn.cursor()
		query = "UPDATE Request set isHidden = True WHERE ReID=%s returning reid;"
		cursor.execute(query,(ReqID,))
		self.conn.commit()
		request = self.getRequestById(str(ReqID))
		return request

	def update(self, reid, rid, reqty):
		cursor = self.conn.cursor()
		query = "UPDATE Request set RID = %s AND ReQty=%s WHERE ReID=%s returning *;"
		cursor.execute(query,(rid,reqty,reid))
		request = cursor.fetchone()
		self.conn.commit()
		return request

	def _build_sql_statement(self, keywordDict):
		if not keywordDict:
			return "SELECT * FROM Request Natural Inner Join Resource Natural Inner Join ResourceType;"
		query = "SELECT * FROM Request Natural Inner Join Resource Natural Inner Join ResourceType WHERE "
		paramList = []
		for column in self.requestColumns:
			if keywordDict.get(column) is not None or keywordDict.get(column)=='':
				query += column + "=%s AND "
				paramList.append(keywordDict.get(column))
		query = query[:len(query)-4]
		query +="ORDER BY RName;"
		return query, paramList

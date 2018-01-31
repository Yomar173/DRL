import psycopg2

from config.dbconfig import url_conn


class DashboardDAO:
	def __init__(self):
		connection_url = url_conn
		self.conn = psycopg2._connect(connection_url)
#CheckForNewDB
	def getDailyResourcesInNeed(self):
		cursor = self.conn.cursor()
		query = 'SELECT RID, RName, RBrand, sum(ReQty) FROM Resource Natural Inner Join Request WHERE IsCompleted=False Group By RID;'
		cursor.execute(query)
		result = []
		for row in cursor:
			result.append(row)
		return result

	def getDailyResourcesAvailable(self):
		cursor = self.conn.cursor()
		query = 'SELECT RID, RName, RBrand, sum(RQty) FROM Resource Natural Inner Join Inventory Group By RID;'
		cursor.execute(query)
		result = []
		for row in cursor:
			result.append(row)
		return result

	def getDailyMatching(self):
		cursor = self.conn.cursor()
		query = 'SELECT RID, RName, RBrand, sum(RQty) as ResourceQty, sum(ReQty) as RequestQty FROM Resource Natural Inner Join Inventory Natural Inner Join Request Group By RID;'
		cursor.execute(query)
		result = []
		for row in cursor:
			result.append(row)
		return result

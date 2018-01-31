from flask import jsonify
from dao.dashboard import DashboardDAO

class DashboardHandler:

	def _build_resource_dict(self, row, isRequest = None):
		result = {}
		result['RID'] = row[0]
		result['RName'] = row[1]
		result['RBrand'] = row[2]
		if isRequest is None:
			result['Total Resources'] = row[3]
			result['Total Request'] = row[4]
		else:
			if isRequest:
				result['Total Request'] = row[3]
			else:
				result['Total Resources'] = row[3]
		return result

	def getDashboard(self):
		dailyInNeedRes = self._getDailyResourcesInNeed()
		dailyAvailRes = self._getDailyAvailableResources()
		dailyMatching = self._getDailyMatching()
		return jsonify(DailyResoucesInNeed = dailyInNeedRes, DailyAvailableResources = dailyAvailRes,
						DailyMatching = dailyMatching)

	def _getDailyAvailableResources(self):
		dao = DashboardDAO()
		resultsAvail = dao.getDailyResourcesAvailable()
		resultsList = []
		for row in resultsAvail:
			resultsList.append(self._build_resource_dict(row,False))
		return resultsList

	def _getDailyResourcesInNeed(self):
		dao = DashboardDAO()
		resultsNeed = dao.getDailyResourcesInNeed()
		resultsList = []
		for row in resultsNeed:
			resultsList.append(self._build_resource_dict(row,True))
		return resultsList

	def _getDailyMatching(self):
		dao = DashboardDAO()
		dailyMatching = dao.getDailyMatching()
		matchingList = []
		for row in dailyMatching:
			matchingList.append(self._build_resource_dict(row))
		return matchingList

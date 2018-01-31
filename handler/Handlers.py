
class PersonHandler:

    def getAllPerson(self):
        fhand = open('data/Buyer', 'r')
        list = []
        for line in fhand:
            t = line.split(',')
            d = {
                'PID' : int(t[0]),
                'FName' : t[1],
                'LName' : t[2],
                'Municipality' : t[3],
                'Phone' : t[4],
                'Gender' : t[5],
                'BDate' : t[6]
            }
            list.append(d)
        return list

    def searchPerson(self, l):
        data = self.getAllPerson()
        print(l)
        print(l['PID'])
        people = []
        #for element in data:
            # if
        return people

# class ResourceHandler:
#
#     def getAllResources(self):
#         fhand = open('data/Resource', 'r')
#         list = []
#         for line in fhand:
#             t = line.split()
#             d = {
#                 'RID' : int(t[0]),
#                 'RName' : t[1],
#                 'Description' : t[2],
#                 'Category' : t[3],
#                 'SubCategory' : t[6],
#                 'Brand' : t[4],
#                 'Condition' : t[5],
#             }
#             list.append(d)
#         return list
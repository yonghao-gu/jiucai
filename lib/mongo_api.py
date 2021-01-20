# -*- coding: utf-8 -*-

import pymongo

class CMongodbManager(object):
    def __init__(self, db_name, addr, port, user = None, password = None):
        self.m_conf = {
            "addr" : addr,
            "port" : port,
            "user" : user,
            "password" : password,
        }
        print(self.m_conf)
        self.m_name = db_name
        self.m_dbobj = None
    
    def Client(self):
        if self.m_dbobj:
            return self.m_dbobj
        if not self.m_conf["user"] :
            url = "mongodb://%s:%s/%s"%(self.m_conf["addr"], str(self.m_conf["port"]), self.m_name)
        else:
            url = "mongodb://%s:%s@%s:%s/%s"%(self.m_conf["user"], self.m_conf["password"], self.m_conf["addr"], str(self.m_conf["port"]), self.m_name)
        print(url)
        self.m_dbobj = pymongo.MongoClient(url)

        return self.m_dbobj

    def DB(self):
        return self.Client()[self.m_name]
 

    def Collection(self, collaction):
        return self.DB()[collaction]


# if __name__ == "__main__":
#     obj = CMongodbManager("_game", "192.168.6.108", "27017")
#     col = obj.Collection("role")
#     print(col.find_one({},{"_id":0,"pay_prestige":1, "guides":1}))







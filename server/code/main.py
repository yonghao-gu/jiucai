import sys
import os
libpath = os.path.abspath("./lib")
sys.path.append(libpath)

import globals
import mongo_api




def main():
    obj = mongo_api.CMongodbManager("_game", "192.168.6.108", "27017")
    globals.set_obj("gamedb", obj)


if __name__ == "__main__":
    main()
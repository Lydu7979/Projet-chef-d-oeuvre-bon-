
import pymongo
import dns

def get_client_mongodb(user_name = "Thmo89",psw = "Authentication "):
    
    uri2 = "mongodb+srv://{}:{}@cluster1.mknx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(user_name, psw)

    client = pymongo.MongoClient(uri2)
    return client
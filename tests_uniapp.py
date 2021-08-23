import unittest



class Test(unittest.TestCase):

    def test_read_main():
        response = client.get("/Bienvenue")
        assert response.status_code == 200
        assert response.json() == {"Message": "Bonjour, ceci est la beta d'un algorithm d'analyse de sentiment", "Status Code": 200}

        


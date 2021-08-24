import pytest
from os import environ
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection
from time import sleep
import requests
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope='class')
def driver(request):
    driver = webdriver.Chrome()
    request.cls.driver = driver
    yield
    driver.close()

@pytest.mark.usefixtures('driver')
class Test_api:
    pass
class Test_url(Test_api):
    def test_titre(self):
        self.driver.get('http://localhost:8501/')
        sleep(4)

        h1_text = self.driver.find_element_by_css_selector("#cr-er-votre-compte").text
        assert "votre compte" in h1_text

    def test_création_compte(self):
        self.driver.get('http://localhost:8501/')
        sleep(4)
        
        n_name = '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[3]/div/div[1]/div/input'
        p_mdp = '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div[1]/div/input'
        l_sub = '//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[6]/div/button'
        
        

        self.driver.find_element_by_xpath(n_name).send_keys("Nom_utilisateur")
        self.driver.find_element_by_xpath(p_mdp).send_keys("Mot_de_passe")
        sleep(4)
        self.driver.find_element_by_xpath(l_sub).click()
        sleep(4)

    def test_connexion(self):
        self.driver.get('http://localhost:8501/')
        sleep(4)
        n_name2 = '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/input'
        p_mdp2 = '//*[@id="root"]/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div/input'


        self.driver.find_element_by_xpath(n_name2).send_keys("Nom_utilisateur")
        self.driver.find_element_by_xpath(p_mdp2).send_keys("Mot_de_passe")
        sleep(4)
        self.driver.find_element_by_xpath(p_mdp2).send_keys(Keys.ENTER)
        sleep(4)

        #Titre principal de l'application

        
        h1_tp = self.driver.find_element_by_css_selector("#app-prix-production-de-tomates").text
        assert "tomates" in h1_tp

        #Titre de la base de données

        h1_tbdd = self.driver.find_element_by_css_selector("#base-de-donn-es-mongodb").text
        assert "Mongodb" in h1_tbdd

        #affichage base de données

        self.driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div/div/section[2]/div/div[1]/div[7]/div/div/div[1]/div[2]/div[2]')


    

        


        
        
        


        
    
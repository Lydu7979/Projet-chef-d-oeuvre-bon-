import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import streamlit as st

def csv_downloader(data):
	csvfile = data.to_csv()
	b64 = base64.b64encode(csvfile.encode()).decode()
	new_filename = "new_text_file_{}_.csv".format(timestr)
	st.markdown("#### Télécharger fichier ###")
	href = f'<a href="data:file/csv;base64,{b64}" Téléchargement="{new_filename}">Cliquer ici!!!</a>'
    return href
	




class download(object):

    def __init__(self, data, filename="mon_fichier", file_ext='csv'):
        super(download, self).__init__()
        self.data = data
        self.filename = filename
        self.file_ext = file_ext

    def tele(self):
        b64 = base64.b64encode(self.data.encode()).decode()
        new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
        st.markdown("#### Télécharger fichier ###")
        href = f'<a href="data:file/{self.file_ext};base64,{b64}" Téléchargement="{new_filename}">Cliquer ici!!!</a>'
        st.markdown(href,unsafe_allow_html=True)




        
        

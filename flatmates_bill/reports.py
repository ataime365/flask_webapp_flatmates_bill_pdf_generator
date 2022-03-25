import webbrowser
from fpdf import FPDF
import os
from filestack import Client

class PdfReport:
    """
    Creates a pdf file that contains data about the flatmates,
    such as their names, their due amount and the period of the bill.
    """
    
    def __init__(self, filename):
        self.filename = filename
        
    def generate(self, *flatmates, bill):
        pdf = FPDF(orientation='P', unit='pt', format='A4') #Default (orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.image('files/house.png', w=40, h=40)
        # title
        pdf.set_font(family='Times', style= 'B', size=24) #B means Bold
        pdf.cell(w=0, h=80, txt="Flatmates Bill", border=0, align="C", ln=1) #"C" means center
        #w and h are in pt units as defined in the FPDF, ln=1 takes it to the next line, if not, it will just be in front of it
        pdf.set_font(family='Times', style= 'B', size=18)
        pdf.cell(w=100, h=40, txt="Period: ", border=0)
        pdf.cell(w=150, h=40, txt=bill.period_month , border=0, ln=1)
        flatmates = list(flatmates) #changing the tuple to a list is very important
        pdf.set_font(family='Times', style= '', size=14)
        for flatmate in set(flatmates):
            # print('********************************')
            pdf.cell(w=150, h=25, txt=flatmate.name + ': ', border=0) #txt is a string
            flatmates.remove(flatmate)
            print(flatmate.name)
            pdf.cell(w=150, h=25, txt=str(flatmate.pays(bill, *flatmates)), border=0, ln=1) #def pays can also take a list i.e *list or *tuple
            flatmates.append(flatmate)
            print([flatmate.name for flatmate in flatmates])

        pdf.set_font(family='Times', style= 'B', size=16) #B means Bold
        pdf.cell(w=150, h=50, txt="Total: ", border=0)
        pdf.cell(w=150, h=50, txt=str(bill.amount) , border=0, ln=1)
            
        # This is the only part that changes, and it would be saved in the files directory
        os.chdir("files") #This changes the working directory to 'files' while the python code is still running
        pdf.output(self.filename)
        webbrowser.open(self.filename)
        
        
class Uploads:
    
    def __init__(self, filepath, api_key):
        self.filepath = filepath
        self.api_key = api_key
    
    def to_cloud(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath )
        return new_filelink.url
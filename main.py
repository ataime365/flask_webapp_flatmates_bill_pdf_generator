from flask.views import MethodView
from flask import Flask, render_template, request
from wtforms import Form, StringField, SubmitField
from flatmates_bill.reports import PdfReport, Uploads
from flatmates_bill.flat import Bill, Flatmate  
from wtforms import Form, RadioField
from wtforms.validators import Required
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
cdn_api_key = os.getenv('CDN_APIKEY') #cloud fileshare

app = Flask(__name__) #instanciating an object or a Flask object

class HomePage(MethodView):
    
    def get(self):
        return render_template("index.html")


class BillFormPage(MethodView):
    def get(self):
        billform = BillForm() #Initializing the BillForm class
        return render_template("bill_form_page.html" , billform = billform ) 

    def post(self):
        billform = BillForm(request.form) #Initializing the BillForm class, but adding the formdata argument
        # This is where we do the calculations
        amount = int(billform.amount.data)
        period = billform.period.data #Input
        
        the_bill = Bill(amount, period)
        
        all_flatmates = []
        
        flatmate_name1 = billform.name1.data
        flatmate_days_in_house1 = int(billform.days_in_house1.data)
        flatmate_name2 = billform.name2.data
        flatmate_days_in_house2 = int(billform.days_in_house2.data)
        flatmate_name3 = billform.name3.data
        flatmate_days_in_house3 = int(billform.days_in_house3.data)
        
        flatmate1 = Flatmate(flatmate_name1, flatmate_days_in_house1)
        flatmate2 = Flatmate(flatmate_name2, flatmate_days_in_house2)
        flatmate3 = Flatmate(flatmate_name3, flatmate_days_in_house3)
        all_flatmates.append(flatmate1)
        all_flatmates.append(flatmate2)
        all_flatmates.append(flatmate3)
        
        # Just for showing on the front page
        f1pays = flatmate1.pays(the_bill, flatmate2, flatmate3) #The pays method already does the_bill.amount
        f2pays = flatmate2.pays(the_bill, flatmate1, flatmate3) #The pays method already does the_bill.amount
        f3pays = flatmate3.pays(the_bill, flatmate1, flatmate2) #The pays method already does the_bill.amount
        
        f1name = flatmate1.name
        f2name = flatmate2.name
        f3name = flatmate3.name
        
        # Main part
        new_pdf = PdfReport(f"{the_bill.period_month} bill.pdf") #meant to be just bill.pdf #filepath #filename
        new_pdf.generate(*all_flatmates , bill=the_bill) # *all_flatmates , just learnt this
        uploads = Uploads(f"{the_bill.period_month} bill.pdf", 'AdMfuC8rYRg1iMm4tMYOUz') #Or new_pdf.filename
        cloud_link = uploads.to_cloud()
        return render_template("bill_form_page.html" , billform=billform, result=True, f1pays = f1pays, f2pays= f2pays, f3pays=f3pays,
                f1name=f1name, f2name=f2name , f3name=f3name, cloud_link=cloud_link)

class ResultsPage(MethodView): #This class processes the form data and outputs the results_page
    
    def post(self): #comment this out, not needed anymore
        billform = BillForm(request.form) #Initializing the BillForm class, but adding the formdata argument
        # This is where we do the calculations
        amount = int(billform.amount.data)
        period = billform.period.data #Input
        
        the_bill = Bill(amount, period)
        
        all_flatmates = []
        
        flatmate_name1 = billform.name1.data
        flatmate_days_in_house1 = int(billform.days_in_house1.data)
        flatmate_name2 = billform.name2.data
        flatmate_days_in_house2 = int(billform.days_in_house2.data)
        flatmate_name3 = billform.name3.data
        flatmate_days_in_house3 = int(billform.days_in_house3.data)
        
        flatmate1 = Flatmate(flatmate_name1, flatmate_days_in_house1)
        flatmate2 = Flatmate(flatmate_name2, flatmate_days_in_house2)
        flatmate3 = Flatmate(flatmate_name3, flatmate_days_in_house3)
        all_flatmates.append(flatmate1)
        all_flatmates.append(flatmate2)
        all_flatmates.append(flatmate3)
        
        # Just for showing on the front page
        f1pays = flatmate1.pays(the_bill, flatmate2, flatmate3) #The pays method already does the_bill.amount
        f2pays = flatmate2.pays(the_bill, flatmate1, flatmate3) #The pays method already does the_bill.amount
        f3pays = flatmate3.pays(the_bill, flatmate1, flatmate2) #The pays method already does the_bill.amount
        
        f1name = flatmate1.name
        f2name = flatmate2.name
        f3name = flatmate3.name
        
        # Main part
        new_pdf = PdfReport(f"{the_bill.period_month} bill.pdf") #meant to be just bill.pdf #filepath #filename
        new_pdf.generate(*all_flatmates , bill=the_bill) # *all_flatmates , just learnt this
        uploads = Uploads(f"{the_bill.period_month} bill.pdf", cdn_api_key) #Or new_pdf.filename
        cloud_link = uploads.to_cloud()
        return render_template("results.html" , f1pays = f1pays, f2pays= f2pays, f3pays=f3pays,
                f1name=f1name, f2name=f2name , f3name=f3name, cloud_link=cloud_link)



class BillForm(Form): #This is not a page, but a form
    amount = StringField("Bill amount: ", default= "500") #default values for StringFields
    period = StringField("Bill Period: ", default= "July 2021")
    # number_of_flatmates determines how many fields we will get, according to our for loop
    number_of_flatmates = 3
    list_1 = []
    for i in range(number_of_flatmates):
        data_dict = {} 
        data_dict[f'name{i+1}'] = StringField(f"Name of Flatmate{i+1}: ")
        data_dict[f'days_in_house{i+1}'] = StringField(f"Days in house{i+1}: ")
        list_1.append(data_dict)
        
    # Make sure the variables to be used in the html are clearly stated here
    name1 = list_1[0].get('name1')
    name2 = list_1[1].get('name2')
    name3 = list_1[2].get('name3')
    days_in_house1 = list_1[0].get('days_in_house1')
    days_in_house2 = list_1[1].get('days_in_house2')
    days_in_house3 = list_1[2].get('days_in_house3')
    
    button = SubmitField("Calculate")
    

# StringField(label=None, validators=None, filters=tuple(), description='', id=None, default=None, widget=None, render_kw=None,
#             _form=None, _name=None, _prefix='', _translations=None, _meta=None)
# SubmitField(label=None, validators=None, false_values=None, **kwargs: Any)
# BillForm(formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs: Any)

app.add_url_rule('/', view_func=HomePage.as_view('home_page')) #as_view is gotten from MethodView, home_page, using same name as the class is a good practice
app.add_url_rule('/bill', view_func=BillFormPage.as_view('bill_form_page')) #view_fun, treats this class as a function e.g @app.route('/bill'), def bill_form_page()
# app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))


if __name__ == "__main__":
    app.debug = True #This also enables auto reloading
    app.run()

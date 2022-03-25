from reports import PdfReport, Uploads
from flat import Bill, Flatmate    

# Input to bill class
bill_amount= int(input("Input Bill amount: ")) 
period= input("Input period e.g December 2021: ")
the_bill = Bill(bill_amount, period) #already instantiated the class here

# Input amount of flatmates you want
number_of_flatmates = int(input("Input amount of Flatmates you want: "))

# Input list of flatmates
all_flatmates = []
for n in range(1, number_of_flatmates+1): #This will allow is input 4 sets of values
    name = input(f"Input name of Flatmate{n}: ")
    name = name.title()
    days_in_house = int(input(f"Input days_in_house of Flatmate{n}: ")) #could also use {name}
    flatmates1 = Flatmate(name, days_in_house)
    all_flatmates.append(flatmates1)
    
new_pdf = PdfReport(f"{the_bill.period_month} bill.pdf") #meant to be just bill.pdf #filepath #filename
new_pdf.generate(*all_flatmates , bill=the_bill) # *all_flatmates , just learnt this

uploads = Uploads(f"{the_bill.period_month} bill.pdf", 'AdMfuC8rYRg1iMm4tMYOUz') #Or new_pdf.filename
print(uploads.to_cloud())


# john = Flatmate("John", 20)
# mary = Flatmate("Mary", 25)
# lina = Flatmate("Lina", 15)
# obone = Flatmate("Obone", 17)

# print(f"John pays {john.pays(the_bill, mary, lina)}")
# print(f"Mary pays {mary.pays(the_bill, john, lina)}")
# print(f"Lina pays {lina.pays(the_bill, john, mary)}")
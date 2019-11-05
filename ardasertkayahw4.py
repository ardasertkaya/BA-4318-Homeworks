import pandas as pd

df = pd.read_csv("Plaza Coffee.csv", sep=";")

company_names = df["Company"].unique()
payment_types = df["Payment"].unique()
order_types   = df["Order"].unique()

s=""
for n in company_names : # For each company
  
  s+="From Company "
  s+=n
  employer_count =0
  assistant_count=0
  for j in payment_types: # For Each payment type
    if (j == "Credit"):
      
      assistant_count=(df[(df["Company"]== n) & (df["Payment"]==j)].count()[0])
      s+=" " +str(assistant_count)+"assistants have bought "
    else:
      
      employer_count=(df[(df["Company"]== n) & (df["Payment"]==j)].count()[0])
      s+= " " +str(employer_count)+" employess have bought "
    for k in order_types: # For each order type
      indexes = (df["Company"]== n) & (df["Payment"]==j) & (df["Order"]== k) 
      #indexes of specific company, payment type and order,ie, PWC,Credit,Coffee
      summ=df[indexes]["Quantity"].sum() #Their sum counts


      if summ>0:
        s+= str(summ) +" servings of " +k+", "
      #print("Company", i , "Payment" , j ,"Order",k, indexes.count()[0])
  s=s[:-2] # get rid of ", " before "."
  s+=".\n" # newline
print(s)
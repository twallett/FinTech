#%% 
import pandas as pd

df = pd.read_csv("MD_Property_Data.csv")

df = df[df.DESCLU == "Residential"]

df = df[["ACCTID", # Id
        "X", # Longitude
        "Y", # Latitude
        "ZIPCODE",
        "STRUGRAD", # Structure Grade 
        "YEARBLT", # Year Built 
        "SQFTSTRC", # Square-foot 
        "TRADATE", # Transfer Date 
        "CONSIDR1", # Consideration
        "NFMLNDVL", # New Appraised Land Value
        "NFMIMPVL"]] # New Appraised Improved Value

df.rename(columns={"ACCTID": "id",
                   "X": "longitude",
                   "Y": "latitude",
                   "ZIPCODE": "zipcode",
                   "STRUGRAD": "grade",
                   "YEARBLT": "year_built",
                   "SQFTSTRC": "sqft",
                   "TRADATE": "trade_date",
                   "CONSIDR1": "consideration",
                   "NFMLNDVL": "land_value",
                   "NFMIMPVL": "land_improvements"}, 
          inplace = True)

df.replace(" ", pd.NA, inplace = True)
df.dropna(inplace = True)

df = df[(df.zipcode.astype(int) >= 20812) & 
        (df.zipcode.astype(int) <= 21930)]

df.set_index("id", inplace= True)

df = df[df.consideration != 0]

df.to_csv("Clean_MD_Property_Data.csv")


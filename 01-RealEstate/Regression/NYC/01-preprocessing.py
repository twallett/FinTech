#%%
import pandas as pd
import seaborn as sns

df = pd.read_csv("NYC_Property_Data.csv", 
                 index_col=0)

# Keeping features of interest by looking at the data dictionary
df = df[["BORO", # Borough
         "BLDGCL", # Building Class
         "TAXCLASS",  
         "LTFRONT", # Lot Width
         "LTDEPTH", # Lot Depth 
         "FULLVAL", # Market Value 
         "AVLAND", # Actual Land Value 
         "AVTOT", # Actual Total Value 	
         "EXLAND", # Actual Exempt Land Value 	
         "EXTOT", # Actual Exempt Land Total
         "Latitude",
         "Longitude",
         "POSTCODE"]]

# Renaming features
df.rename(columns={"BORO": "borough", # Borough
                   "BLDGCL": "building_class", # Building Class
                   "TAXCLASS": "tax_class",
                   "LTFRONT": "lot_width", # Lot Width
                   "LTDEPTH": "lot_depth", # Lot Depth 
                   "FULLVAL": "market_value", # Market Value 
                   "AVLAND": "land_value", # Actual Land Value 
                   "AVTOT": "total_value", # Actual Total Value 	
                   "EXLAND": "exempt_land_value", # Actual Exempt Land Value 	
                   "EXTOT": "total_exempt_land_value", # Actual Exempt Land Total
                   "Latitude": "latitude",
                   "Longitude": "longitude",
                   "POSTCODE": "zipcode"},
          inplace = True) 	

# Removing Null Values
df.replace(" ", pd.NA, inplace = True)
df.dropna(inplace = True)

# Dropping considerations of 0 value
df = df[df.market_value != 0]

df.building_class = df.building_class.factorize()[0] + 1
df.tax_class = df.tax_class.factorize()[0] + 1

df.to_csv("Clean_NYC_Property_Data.csv")
# %%

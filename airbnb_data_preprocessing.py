#-------------------------------------------------------------------------#
# Project overview:                                                       #
#           Processing Airbnb data in json and converting it to csv file. #
# The processed data will be used for visualization using streamlit and   # 
# Power BI                                                                #
#-------------------------------------------------------------------------#
#-------------------------------------------------------------------------#
# Import all the required components                                      #
#-------------------------------------------------------------------------#
import json
import pandas as pd
import pprint

#-------------------------------------------------------------------------#
# Load the JSON data                                                      #
#-------------------------------------------------------------------------#
with open("D:/Study/Guvi/MDTM33/Projects/1 03 Airbnb/sample_airbnb.json") as airbnb_file:
    airbnb_json = json.load(airbnb_file)
    # pprint.pprint(airbnb_json)

#-------------------------------------------------------------------------#
# Extract data using list comprehensions                                  #
#-------------------------------------------------------------------------#
airbnb_data = [
    [
        i.get("_id"),
        i.get("listing_url"),
        i.get("name"),
        i.get("description"),
        i.get("house_rules"),
        i.get("property_type"),
        i.get("room_type"),
        i.get("bed_type"),
        i.get("minimum_nights"),
        i.get("maximum_nights"),
        i.get("cancellation_policy"),
        i.get("accommodates"),
        i.get("bedrooms"),
        i.get("beds"),
        i.get("bathrooms"),
        i.get("availability",{}).get("availability_365"),
        i.get("price"),
        i.get("security_deposit"),
        i.get("cleaning_fee"),
        i.get("extra_people"),
        i.get("guests_included"),
        i.get("number_of_reviews"),
        i.get("review_scores", {}).get("review_scores_rating"),
        ", ".join(i["amenities"]),  
        i.get("host", {}).get("host_id"),
        i.get("host", {}).get("host_name"),
        i.get("address", {}).get("street"),
        i.get("address", {}).get("country"),
        i.get("address", {}).get("country_code"),      
        i.get("address", {}).get("location", {}).get("type"),
        i.get("address", {}).get("location", {}).get("coordinates")[0],
        i.get("address", {}).get("location", {}).get("coordinates")[1],
        i.get("address", {}).get("location", {}).get("is_location_exact") 
        ] 
    for i in airbnb_json
]
# pprint.pprint(airbnb_data)

#-------------------------------------------------------------------------#
# Create dataframe                                                        #
#-------------------------------------------------------------------------#
airbnb_df_columns = [
    "ID", "url", "Name", "Description", "House_Rules", "Property_Type", "Room_Type", "Bed_Type",
    "Minimum_Nights", "Maximum_Nights", "Cancelation_Policy", "Accomodates", "Bedrooms",
    "Beds", "Bathrooms", "Availability_365", "Price", "Security_Deposit", "Cleaning_Fee", "Extra_People",
    "Guests_Included", "No_Of_Reviews", "Review_Scores", "Amenities", "Host_ID", "Host_Name",
    "Street", "Country", "Country_Code", "Location_Type", "Latitude", "Longitude", "Exact_Location"
]

airbnb_df = pd.DataFrame(airbnb_data, columns=airbnb_df_columns)

# print(airbnb_df)

airbnb_df.info()
# print(airbnb_df.isnull().sum())

#-------------------------------------------------------------------------#
# Filling unknown values                                                  #
#-------------------------------------------------------------------------#
airbnb_df.Bedrooms.fillna(airbnb_df.Bedrooms.median(),inplace=True)
airbnb_df.Beds.fillna(airbnb_df.Beds.median(),inplace= True)
airbnb_df.Bathrooms.fillna(airbnb_df.Bathrooms.mode()[0],inplace= True)
airbnb_df.Review_Scores.fillna(airbnb_df.Review_Scores.median(),inplace=True)
airbnb_df.Security_Deposit.fillna(airbnb_df.Security_Deposit.median(),inplace=True)
airbnb_df.Cleaning_Fee.fillna(airbnb_df.Cleaning_Fee.median(), inplace=True)
airbnb_df.Description.replace(to_replace="",value="No Description Provided",inplace=True)
airbnb_df.House_Rules.replace(to_replace="",value="No House rules Provided",inplace=True)
airbnb_df.Amenities.replace(to_replace="",value="Not Available",inplace=True)

#-------------------------------------------------------------------------#
# Changing desired data types                                             #
#-------------------------------------------------------------------------#
airbnb_df["Minimum_Nights"] = airbnb_df["Minimum_Nights"].astype(int)
airbnb_df["Maximum_Nights"] = airbnb_df["Maximum_Nights"].astype(int)
airbnb_df["Bedrooms"] = airbnb_df["Bedrooms"].astype(int)
airbnb_df["Beds"] = airbnb_df["Beds"].astype(int)
airbnb_df["Bathrooms"] = airbnb_df["Bathrooms"].astype(int)
airbnb_df["Extra_People"] = airbnb_df["Extra_People"].astype(int)
airbnb_df["Guests_Included"] = airbnb_df["Guests_Included"].astype(int)

#-------------------------------------------------------------------------#
# Remove unwanted rows and drop duplicates                                #
#-------------------------------------------------------------------------#
# count_empty_string = airbnb_df["Name"].eq("").any()
# print("empty string", count_empty_string)
airbnb_df.drop(airbnb_df.index[airbnb_df['Name'] == ''], inplace=True)
airbnb_df.drop_duplicates(inplace=True)
airbnb_df.reset_index(drop=True,inplace=True)
# print(airbnb_df.isnull().sum())
airbnb_df.info()

#-------------------------------------------------------------------------#
# Format "\n" new line values in Data frame                               #
#-------------------------------------------------------------------------#
for i in range(airbnb_df.shape[0]):
    txt = airbnb_df.iloc[i]["Street"]
    fmt_txt = txt.replace("\n", "")
    airbnb_df.at[i, "Street"] = fmt_txt

#-------------------------------------------------------------------------#
# Convert processed data as csv for analysis                              #
#-------------------------------------------------------------------------#
airbnb_df.to_csv("D:/Study/Guvi/MDTM33/Projects/1 03 Airbnb/sample_airbnb.csv",index=False)

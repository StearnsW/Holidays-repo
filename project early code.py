import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
      
    name: str
    date: datetime        
    
    def __str__ (self):
        return '%s (%s)' % (self.name, self.date)

           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
       self.innerHolidays = []
       self.test=Holiday("test",'2019-12-04')

    def addHoliday(self,holidayObj,internal):
        # Make sure holidayObj is an Holiday Object by checking the type
        is_holiday=False
        if type(holidayObj)==type(self.test):
            is_holiday=True
        else:
            print("not a holiday, please try again")
        # Use innerHolidays.append(holidayObj) to add holiday
        if is_holiday:
            self.innerHolidays.append(holidayObj)
            # print to the user that you added a holiday
            if not internal:
                print("A holiday was added to the list")

    def findHoliday(self,HolidayName, Date):
        # Find Holiday in innerHolidays
        holiday_to_find=Holiday(HolidayName,Date)
        holiday_in_list=False
        for holiday in self.innerHolidays:
            if holiday==holiday_to_find:
                holiday_in_list=True
                # Return Holiday
                return(holiday)
        #Message if entered holiday not in list
        if not holiday_in_list:
            print("that holiday is not in the list")
            return None
        
    def removeHoliday(self,HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        holiday_to_remove=self.findHoliday(HolidayName,Date)
        # remove the Holiday from innerHolidays
        if holiday_to_remove!=None:
            self.innerHolidays.remove(holiday_to_remove)
            # inform user you deleted the holiday
            print("That holiday has been removed from the list")

    def read_json(self,filelocation):
        # Read in things from json file location
        file=open(f'{filelocation}.json')
        holidays_json = json.load(file)
        file.close()
        holidays_list=holidays_json['holidays']
        internal_addition=True
        for holiday in holidays_list:
            holiday_object=Holiday(holiday["name"],holiday["date"])
            self.addHoliday(holiday_object,internal_addition)
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self,filelocation):
        # Write out json file to selected file.
        file=open(f'{filelocation}.json','w') # open the file to edit
        holidays_list=[]
        for holiday in self.innerHolidays:
            holiday_as_dict={}
            name=holiday.name
            date=holiday.date
            holiday_as_dict["name"]=name
            holiday_as_dict["date"]=date
            holidays_list.append(holiday_as_dict)
        json_dict={}
        json_dict["holidays"]=holidays_list
        json.dump(json_dict,file)
        file.close()

    def scrapeHolidays():
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.
        print("hello")   

test1=Holiday("tester",'2019-12-04') 
test2=14
test3=Holiday("tester2",'2019-12-04')
test_list=HolidayList()
test_list.addHoliday(test1,False)
test_list.addHoliday(test2,False)
test_list.addHoliday(test3,False)
test_list.removeHoliday("tester2",'2019-12-04')
test_list.findHoliday("tester",'2019-12-04')
test_list.findHoliday("tester2",'2019-12-04')
test_list.read_json("holidays")
test_list.findHoliday("Margaret Thatcher Day","2021-01-10")
test_list.save_to_json("test")
second_test_list=HolidayList()
second_test_list.read_json("test")      

#     def numHolidays():
#         # Return the total number of holidays in innerHolidays
    
#     def filter_holidays_by_week(year, week_number):
#         # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
#         # Week number is part of the the Datetime object
#         # Cast filter results as list
#         # return your holidays

#     def displayHolidaysInWeek(holidayList):
#         # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
#         # Output formated holidays in the week. 
#         # * Remember to use the holiday __str__ method.

#     def getWeather(weekNum):
#         # Convert weekNum to range between two days
#         # Use Try / Except to catch problems
#         # Query API for weather in that week range
#         # Format weather information and return weather string.

#     def viewCurrentWeek():
#         # Use the Datetime Module to look up current week and year
#         # Use your filter_holidays_by_week function to get the list of holidays 
#         # for the current week/year
#         # Use your displayHolidaysInWeek function to display the holidays in the week
#         # Ask user if they want to get the weather
#         # If yes, use your getWeather function and display results



# def main():
#     # Large Pseudo Code steps
#     # -------------------------------------
#     # 1. Initialize HolidayList Object
#     # 2. Load JSON file via HolidayList read_json function
#     # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
#     # 3. Create while loop for user to keep adding or working with the Calender
#     # 4. Display User Menu (Print the menu)
#     # 5. Take user input for their action based on Menu and check the user input for errors
#     # 6. Run appropriate method from the HolidayList object depending on what the user input is
#     # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


# if __name__ == "__main__":
#     main();


# # Additional Hints:
# # ---------------------------------------------
# # You may need additional helper functions both in and out of the classes, add functions as you need to.
# #
# # No one function should be more then 50 lines of code, if you need more then 50 lines of code
# # excluding comments, break the function into multiple functions.
# #
# # You can store your raw menu text, and other blocks of texts as raw text files 
# # and use placeholder values with the format option.
# # Example:
# # In the file test.txt is "My name is {fname}, I'm {age}"
# # Then you later can read the file into a string "filetxt"
# # and substitute the placeholders 
# # for example: filetxt.format(fname = "John", age = 36)
# # This will make your code far more readable, by seperating text from code.






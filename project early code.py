import datetime
from datetime import datetime,date
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
    formater_string="%Y-%m-%d"
    date: datetime        
    
    def __str__ (self):
        return '%s (%s)' % (self.name, self.date.strftime(self.formater_string))

           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
       self.innerHolidays = []
       self.test=Holiday("test",'2019-12-04')

    def addHoliday(self,holidayObj,internalBool):
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
            if not internalBool:
                print("A holiday was added to the list")

    def findHoliday(self,HolidayName,Date):
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
        
    def removeHoliday(self,HolidayName,Date):
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
            # Use addHoliday function to add holidays to inner list.
            self.addHoliday(holiday_object,internal_addition)
        
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

    def scrapeHolidays(self):
        this_year=date.today().year
        internal_addition=True
        def getHTML(url):
            response=requests.get(url)
            return response.text
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        years_off_set={-2,-1,0,1,2}
        for year_offset in years_off_set:
            year=this_year+year_offset
            # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
            html_text=getHTML(f"https://www.timeanddate.com/holidays/us/{year}?hol=43119487")
            soup = BeautifulSoup(html_text,'html.parser')
            holiday_table=soup.find('table',attrs={'id':'holidays-table'})
            table_rows=holiday_table.find_all('tr')
            for row in table_rows:
                date_value=row.find('th',attrs={'class':'nw'})
                holiday_name=row.find('a')
                html_formal='%b %d %Y'
                if date_value!=None and holiday_name!=None:
                    date_text=date_value.text
                    as_datetime=datetime.strptime(f"{date_text} {year}",html_formal)
                    holiday_name_text=holiday_name.text
                    holiday_to_add=Holiday(holiday_name_text,as_datetime)
                    # Check to see if name and date of holiday is in innerHolidays array
                    if holiday_to_add not in self.innerHolidays:
                        # Add non-duplicates to innerHolidays 
                        self.addHoliday(holiday_to_add,internal_addition)
        # Handle any exceptions.
   
    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return(len(self.innerHolidays))
    
    def filter_holidays_by_week(self,weekNum,year):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        holidays_this_year=list(filter(lambda x:x.date.year==year,self.innerHolidays))
        holidays_this_week=list(filter(lambda x:int(x.date.strftime('%U'))==weekNum,holidays_this_year))
        # return your holidays
        return holidays_this_week

    def displayHolidaysInWeek(self,holidayList,weatherList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        yesterday=""
        for i in range(len(holidayList)):
            current_day=holidayList[i].date.strftime('%A')
            day_of_week=int(holidayList[i].date.strftime('%w'))
            if current_day!=yesterday:
                print(f"{current_day}  {weatherList[day_of_week]}")
            # Output formated holidays in the week.
            # * Remember to use the holiday __str__ method. 
            print(f"    {holidayList[i]}")
            yesterday=holidayList[i].date.strftime('%A')
            
    def getWeather(self,weekNum,year):
        # Convert weekNum to range between two days
        reference_day=int(datetime.strftime(date.today(),"%j"))
        reference_weekday=date.today().weekday()
        first_sunday=(reference_day-reference_weekday-1)%7
        sunday_of_weekNum="{0:0>3}".format(first_sunday+7*(weekNum-1))
        saturday_of_weekNum="{0:0>3}".format(first_sunday+7*(weekNum-1)+6)
        start_week_day=datetime.strptime(f"{sunday_of_weekNum} {year}","%j %Y")
        end_week_day=datetime.strptime(f"{saturday_of_weekNum} {year}","%j %Y")
        # Query API for weather in that week range
        url = "https://weatherapi-com.p.rapidapi.com/history.json"
        querystring = {"q":"milwaukee","dt":f"{datetime.strftime(start_week_day,'%Y-%m-%d')}","lang":"en","hour":"12","end_dt":f"{datetime.strftime(end_week_day,'%Y-%m-%d')}"}
        headers = {
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
            "X-RapidAPI-Key": "2c98c4ffe8mshd2948e701baa19ep196868jsn0719c00cd518"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        # Format weather information and return weather string.
        weather_json_data = json.loads(response.text)
        weather_list=[]
        for i in range(7):
            weather_list.append("")
        for i in range(len(weather_json_data["forecast"]["forecastday"])):
            weather_list[i]=weather_json_data["forecast"]["forecastday"][i]["day"]["condition"]["text"]
        return weather_list
        # Use Try / Except to catch problems
        

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        this_year=date.today().year
        this_week=int(datetime.strftime(date.today(),"%U"))
        # Use your filter_holidays_by_week function to get the list of holidays for the current week/year
        holiday_list=self.filter_holidays_by_week(this_week,this_year) 
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        weather_list=self.getWeather(this_week,this_year)
        self.displayHolidaysInWeek(holiday_list,weather_list)       


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


# test=HolidayList()
# test.scrapeHolidays()
# test.viewCurrentWeek()
# print(test.numHolidays())
# test.displayHolidaysInWeek(test.filter_holidays_by_week(2022,3))
# test1=Holiday("tester",datetime.strptime('2019-12-04','%Y-%m-%d'))
# print(type(test1.date))
# test2=14
# test3=Holiday("tester2",'2019-12-04')
# test_list=HolidayList()
# test_list.addHoliday(test1,False)
# test_list.addHoliday(test2,False)
# test_list.addHoliday(test3,False)
# test_list.removeHoliday("tester2",'2019-12-04')
# test_list.findHoliday("tester",'2019-12-04')
# test_list.findHoliday("tester2",'2019-12-04')
# test_list.read_json("holidays")
# test_list.findHoliday("Margaret Thatcher Day","2021-01-10")
# test_list.save_to_json("test")
# second_test_list=HolidayList()
# second_test_list.read_json("test")      

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






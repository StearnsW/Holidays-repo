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
        self.inner_holidays = []
        self.test=Holiday("test",datetime.strptime('2019-12-04',"%Y-%m-%d"))
        self.weather_list=[]
        for i in range(7):
            self.weather_list.append("")
        self.up_to_date=True
                
    def addHoliday(self,holidayObj,internalBool):
        # Make sure holidayObj is an Holiday Object by checking the type
        is_holiday=False
        if type(holidayObj)==type(self.test):
            is_holiday=True
        else:
            print("not a holiday, please try again")
        # Use innerHolidays.append(holidayObj) to add holiday
        if is_holiday:
            self.inner_holidays.append(holidayObj)
            # print to the user that you added a holiday
            if not internalBool:
                print(f"{holidayObj} was added to the list")
            self.up_to_date=False

    def findHoliday(self,HolidayName,Date):
        # Find Holiday in innerHolidays
        holiday_to_find=Holiday(HolidayName,Date)
        holiday_in_list=False
        for holiday in self.inner_holidays:
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
            self.inner_holidays.remove(holiday_to_remove)
            # inform user you deleted the holiday
            print(f"Success:\n{HolidayName} has been removed from the list")
            self.up_to_date=False

    def read_json(self,filelocation):
        # Read in things from json file location
        try:
            file=open(f'{filelocation}.json')
            holidays_json = json.load(file)
            file.close()
            holidays_list=holidays_json['holidays']
            internal_addition=True
            for holiday in holidays_list:
                holiday_object=Holiday(holiday["name"],datetime.strptime(holiday["date"],"%Y-%m-%d"))
                # Use addHoliday function to add holidays to inner list.
                self.addHoliday(holiday_object,internal_addition)
        except:
            print("There was an error in the file reading process, I'm sorry")
        
    def save_to_json(self,filelocation):
        # Write out json file to selected file.
        try:
            file=open(f'{filelocation}.json','w') # open the file to edit
            holidays_list=[]
            for holiday in self.inner_holidays:
                holiday_as_dict={}
                name=holiday.name
                date_as_string=datetime.strftime(holiday.date,"%Y-%m-%d")
                holiday_as_dict["name"]=name
                holiday_as_dict["date"]=date_as_string
                holidays_list.append(holiday_as_dict)
            json_dict={}
            json_dict["holidays"]=holidays_list
            json.dump(json_dict,file)
            file.close()
            self.up_to_date=True
            print("Success:\nYour changes have been saves.")
        except:
            print("There was an error in the save process, I'm sorry")

    def scrapeHolidays(self):
        this_year=date.today().year
        internal_addition=True
        def getHTML(url):
            response=requests.get(url)
            return response.text
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        years_off_set={-2,-1,0,1,2}
        # Handle any exceptions.
        try:
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
                        if holiday_to_add not in self.inner_holidays:
                            # Add non-duplicates to innerHolidays 
                            self.addHoliday(holiday_to_add,internal_addition)
        except:
            print("Something seems to have gone wrong sraping the web for holidays, I'm sorry")
        
    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return(len(self.inner_holidays))
    
    def filter_holidays_by_week(self,weekNum,year):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        holidays_this_year=list(filter(lambda x:x.date.year==year,self.inner_holidays))
        holidays_this_week=list(filter(lambda x:int(x.date.strftime('%U'))==weekNum,holidays_this_year))
        # return your holidays
        return holidays_this_week

    def displayHolidaysInWeek(self,holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        yesterday=""
        for i in range(len(holidayList)):
            current_day=holidayList[i].date.strftime('%A')
            day_of_week=int(holidayList[i].date.strftime('%w'))
            if current_day!=yesterday:
                if self.weather_list[day_of_week]!="":
                    print(f"Day: {current_day}  Weather: {self.weather_list[day_of_week]}")
                else:
                    print(f"Day: {current_day}")
            # Output formated holidays in the week.
            # * Remember to use the holiday __str__ method. 
            print(f"    {holidayList[i]}")
            yesterday=holidayList[i].date.strftime('%A')
            
    def getWeather(self,weekNum,year):
        # Convert weekNum to range between two days
        reference_day=int(datetime.strftime(date.today(),"%j"))
        reference_weekday=date.today().weekday()
        first_sunday=(reference_day-reference_weekday-1)%7
        # Use Try / Except to catch problems
        try:
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
            for i in range(len(weather_json_data["forecast"]["forecastday"])):
                self.weather_list[i]=weather_json_data["forecast"]["forecastday"][i]["day"]["condition"]["text"]
        except:
            print("Something seems to have gone wrong getting the weather data, I'm sorry")    
        return self.weather_list

    def resetWeather(self):
        for i in range(7):
            self.weather_list[i]=""

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        this_year=date.today().year
        this_week=int(datetime.strftime(date.today(),"%U"))
        # Use your filter_holidays_by_week function to get the list of holidays for the current week/year
        holiday_list=self.filter_holidays_by_week(this_week,this_year) 
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        self.getWeather(this_week,this_year)
        self.displayHolidaysInWeek(holiday_list)       



def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    Holidays=HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    Holidays.read_json("holidays")
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    Holidays.scrapeHolidays()
    # 3. Create while loop for user to keep adding or working with the Calender
    editing_file=True
    while editing_file:
        # 4. Display User Menu (Print the menu)
        user_choice=User_Menu()
        # 6. Run appropriate method from the HolidayList object depending on what the user input is
        if user_choice==1:
            internal_add=False
            holiday_name=Add_Holiday_Menu()
            holiday_date=Date_Check(holiday_name)
            Holidays.addHoliday(Holiday(holiday_name,holiday_date),internal_add)
            print("\n\n")
        elif user_choice==2:
            holiday_name=Remove_Holiday_Menu()
            holiday_date=Date_Check(holiday_name)
            Holidays.removeHoliday(holiday_name,holiday_date)
            print("\n\n")
        elif user_choice==3:
            file_name=Save_Holiday_List_Menu()
            if file_name!="":
                Holidays.save_to_json(file_name)
        elif user_choice==4:
            year_to_view=View_Holidays_Menu()
            week_to_view=Get_Week()
            print("\n")
            if week_to_view=="":
                Holidays.viewCurrentWeek()
            else:
                holidays_to_view=Holidays.filter_holidays_by_week(week_to_view,year_to_view)
                Holidays.resetWeather()
                Holidays.displayHolidaysInWeek(holidays_to_view)
        else:
            editing_file=not Exit_Menu(Holidays.up_to_date)
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


def User_Menu():
    print("Holiday Menu")
    print("==================")
    # options
    print("1. Add a Holiday")
    print("2. Remove a Holiday")
    print("3. Save Holiday List")
    print("4. View Holidays")
    print("5. Exit")
    #loop to make sure they choose a valid option
    choice_made = False
    # 5. Take user input for their action based on Menu and check the user input for errors
    while not choice_made:
        choice=input("What would you like to do, please enter the corresponging number: ")
        if choice not in {'1','2','3','4','5'}:
            print("Not a recognized choice, please try agian")
        else:
            choice_made = True
    print("\n\n")
    return int(choice)

def Add_Holiday_Menu():
    print("Add a Holiday")
    print("==================")
    holiday_name_input=input("Holiday Name: ")
    return holiday_name_input

def Remove_Holiday_Menu():
    print("Remove a Holiday")
    print("==================")
    holiday_name_input=input("Holiday Name: ")
    return holiday_name_input

def Save_Holiday_List_Menu():
    print("Save Holiday List")
    print("==================")
    run_save = False
    save_file_name=""
    while not run_save:
        save_changes=input("Are you sure you want to save your changes? [y/n]: ")
        if save_changes!='y' and save_changes!='n': # invalid reply
            print("That wasn't one of the options, please resond only 'y' or 'n'")
        elif save_changes == 'n': # not to edit existing, leave edit conflict loop
            print("Canceled:\nHoliday list file save canceled.")
            run_save = True
        else: # want to edit existing, leave edit conflict loop and same name loop, change edit boolean
            save_file_name=input("What would like the file to be called?\n")
            run_save=True
    return save_file_name

def View_Holidays_Menu():
    print("View Holidays")
    print("==================")
    found_year=False
    while not found_year:
        year_input=input("Which year?: ")
        if year_input.isnumeric():
            if int(year_input)>1899 and int(year_input)<2100:
                return int(year_input)
            else:
                print("Invalid year, please try again")
        else:
            print("Not recognized as a year, please try again")

def Exit_Menu(nothing_to_save):
    print("Exit")
    print("==================")
    want_to_exit=False
    is_exiting = False
    while not is_exiting:
        if nothing_to_save:
            exiting=input("Are you sure you want to exit? [y/n] ")
        else:
            exiting=input("Are you sure you want to exit?\nYour changes will be lost.\n[y/n] ")
        if exiting!='y' and exiting!='n': # invalid reply
            print("That wasn't one of the options, please resond only 'y' or 'n'")
        elif exiting == 'n': # don't exit program, exit loop
            print("You will be returned to the Main Menu")
            is_exiting = True
        else: # exit loop, change want to exit to Main Menu
            print("Goodbye!")
            is_exiting = True
            want_to_exit = True
    return want_to_exit
    

def Date_Check(name):
    date_to_check=input("Date (YYYY-MM-DD): ")
    retry=False
    try:
        date_to_return=datetime.strptime(date_to_check,"%Y-%m-%d")
    except:
        print("Error:\nInvalid date.  Please try agian")
        retry=True
    while retry:
        date_to_check=input(f"Date for {name} (YYYY-MM-DD): ")
        try:
            date_to_return=datetime.strptime(date_to_check,"%Y-%m-%d")
            retry=False
        except:
            print("Error:\nInvalid date.  Please try agian")
    return date_to_return

def Get_Week():
    valid_week=False
    while not valid_week:
        week_to_check=input("Which week? #[1-52, Leave blank for the current week]: ")
        if week_to_check.isnumeric():
            if int(week_to_check)>0 and int(week_to_check)<53:
                week_to_return=int(week_to_check)
                valid_week=True
            else:
                print("That week number is out of range, please try again")
        elif week_to_check=="":
                week_to_return=week_to_check
                valid_week=True
        else:
            print("That wasn't recognized as a number or [blank], please try again")
    return week_to_return
        

#main()
# test=HolidayList()
# print(test.weather_list)
# test.scrapeHolidays()
# holidays=test.filter_holidays_by_week(0,2022)
# test.displayHolidaysInWeek(holidays)
# weather=test.getWeather(0,2022)
# print(test.weather_list)
# print(test.numHolidays())
# test.displayHolidaysInWeek(test.filter_holidays_by_week(2022,3))
# test1=Holiday("tester",datetime.strptime('2019-12-04','%Y-%m-%d'))
# print(type(test1.date))
# test2=14
# test3=Holiday("tester2",'2019-12-04')
# test_list=HolidayList()
# test_list.scrapeHolidays()
# test_list.save_to_json("test")
# second_test_list=HolidayList()
# second_test_list.read_json("test")      

if __name__ == "__main__":
    main();


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






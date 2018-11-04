import csv
import re
import datetime
import sys
import os
import pytz


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu():
    clear_screen()

    print("Hello and welcome to your Meeting/Task organizer.")
    print("Let us begin...\n")
    print("""
     Type '1' to add a task
     Type '2' to search for a task
     Type '3' to quit\n""")
    user_answer = None
    while not user_answer:
        user_answer = input("Please choose from the list:  ")
        if user_answer == '1':
            add()
        elif user_answer == '2':
            search_by()
        elif user_answer == '3':
            clear_screen()
            print("Thank you and have a good day!")
            break


def add():
    clear_screen()
    the_task = user_time = user_notes = None
    while True:
        the_task = input("Please enter your task:  ")
        while user_time is None:
            user_time = input("Please enter time to the nearest minutes: ")
        try:
            user_time = int(user_time)
        except ValueError:
            print("Please enter a valid length of time.")
            user_time = input("Please enter time to the nearest minute:  ")
        user_notes = input("Please enter any additional notes for this task (OPTIONAL):  ")
        user_date = datetime.datetime.now().strftime("%m/%d/%Y")
        with open("work_log.csv", "a+", newline='') as cvsfile:
            fields = ['Task', 'Time Spent', 'Additional Notes', 'Date']
            write = csv.DictWriter(cvsfile, fieldnames=fields)
            if os.stat('work_log.csv').st_size == 0:  # Checks to see if file has been previously created, if not, create it and write the headers
                write.writeheader()
            write.writerow({"Task": the_task, "Time Spent": user_time, "Additional Notes": user_notes, "Date": user_date})

        user_input = input("Please enter Y/Yes to go back or N/No to quit  ").lower()

        if user_input != 'y':
            print("Have a great day!")  # prints 'Have a great day!'
            break
        else:
            menu()

def search_by():
    clear_screen()
    user_search = None

    print("""
    Please Select from the options below...
    Find by..
    1 - Date
    2 - Time Spent
    3 - Exact Match
    4 - Regex expression
    5 - Return to main menu
    """)

    while not user_search:
        user_search = input("Please choose an option (1-5):   ")
        if user_search == '1':
            find_date()
        elif user_search == '2':
            find_time()
        elif user_search == '3':
            find_exact()
        elif user_search == '4':
            find_regex()
        elif user_search == '5':
            menu()

def date_list(date_entered): # Allows for usage in program by acting as a list
    while len(date_entered) == 0:
        try:
            date_input = input("Please enter the date:  ")
            date_entered.append(datetime.datetime.strptime(date_input, '%m/%d/%Y'))
        except ValueError:
            print("Please enter the date in a MM/DD/YYYY format.")

def find_date():
    first_search_date = []
    second_search_date = []
    searched = None
    while not searched:
        clear_screen()
        searched = input("""
        Please enter 
        1: to find an exact date 
        2: to find within a range of two dates
        >>>   """)
        if searched not in ['1' , '2']:
            print("Not a valid selection. Please enter 1 or 2.")
            searched = None
    date_list(first_search_date)
    if searched == '2':
        print("Please enter an end date in MM/DD/YYYY format")
        while not second_search_date:
            date_list(second_search_date)
            if first_search_date[0] > second_search_date[0]:
                print("The first date cannot be later than the second date. Please enter end date again")
                second_search_date = []
    results = []
    with open('work_log.csv') as file:
        reader = csv.DictReader(file)
        if searched == '1':
            for row in reader:
                if(datetime.datetime.strptime(row['Date'], '%m/%d/%Y') == first_search_date[0]): 
                    results.append(row)
        else:
            for row in reader:
                if ((datetime.datetime.strptime(row['Date'], '%m/%d/%Y') >= first_search_date[0]) and 
                    (datetime.datetime.strptime(row['Date'], '%m/%d/%Y') <= second_search_date[0])):
                    results.append(row)
    if len(results) == 0:
        print("No results found.")
        search_by()
    else:
        show_results(results)

def find_time():
    searched_time = None
    searched_results = []
    print("Please enter a task length to search for.")
    while searched_time is None:
        searched_time = input("Please enter time to the nearest minutes: ")
        try:
            searched_time = int(searched_time)
        except ValueError:
            print("Please enter a valid length of time.")
            searched_time = None
        else:
            searched_time = str(searched_time)
    with open('work_log.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Time Spent'] == searched_time:
                searched_results.append(row)
    if len(searched_results) == 0:
        print("No results found.")
        search_by()
    else:
        show_results(searched_results)

def find_exact():
    searched_string = None
    searched_results = []
    print("Enter text to be searched")
    while searched_string is None or searched_string.isspace():
        searched_string = input("Enter text:  ")
        if searched_string.strip() == '':
            print("Please enter some text")
            searched_string = None
    with open('work_log.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['Task'].find(searched_string) > -1 or row['Additional Notes'].find(searched_string) > -1):
                searched_results.append(row)
    if len(searched_results) == 0:
        print("No results found.")
        search_by()
    else:
        show_results(searched_results)

def find_regex():
    searched_exp = None
    searched_results = []
    print("Enter a regular expression to search")
    while searched_exp is None:
        searched_exp = input("Enter a regex: ")
        try:
            searched_exp = re.compile(searched_exp) # Sets pattern into an object for usage
        except re.error:
            print("Sorry, that is not a valid regular expression.")
            searched_exp = None
    with open('work_log.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (re.search(searched_exp, row['Task']) or
                re.search(searched_exp, row['Time Spent']) or
                re.search(searched_exp, row['Additional Notes']) or
                re.search(searched_exp, row['Date'])):
                searched_results.append(row)
        if len(searched_results) == 0:
            print("No task found.")
            search_by()
        else:
            show_results(searched_results)

def show_results(result_list):
    clear_screen()
    counter = 1 #used for pagination 
    for item in result_list:
        print("""
            Result {} of {}\n
            Task: {}
            Time Length: {}
            Date: {}
            Notes: {}\n""".format(counter, len(result_list), item["Task"], item['Time Spent'], item['Date'], item['Additional Notes']))
        user_selection = None
        while not user_selection:
            user_selection = input("""
            Please Select...
            {}
            [E] for Edit entry, 
            [D] for Delete entry, 
            [S] for the Search Menu:  
            """.format('''
            [N] for Next Result ''' if counter < len(result_list) else ''))
            if user_selection.lower() == 'e':
                edit_entry(item)
            elif user_selection.lower() == 'd':
                delete_entry(item)
            elif user_selection.lower() == 's':
                return search_by()
            elif user_selection.lower() == 'n':
                user_selection == None  
                clear_screen()          
        counter += 1
    print("End of search results\n")
    search_by()

def edit_entry(task_list):
    dict_header = {'1': 'Task', '2': 'Time Spent', '3': 'Additional Notes', '4': 'Date'}
    user_field = None
    while not user_field:
        user_field = input('''
            Select what field to edit:
            1: Task Name
            2: Task Length
            3: Task Notes
            4: Task Date
            5: Go back to search results
            6: Go back to main menu\n
            >>  ''')
        if user_field == '5':
            return
        if user_field == '6':
            return search_by()
    new_entry = None
    while not new_entry:
        new_entry = input("Enter new {}: ".format(dict_header[user_field]))
        if new_entry.isspace():
            new_entry = None
            continue
        if user_field == '2':
            try:
                new_entry = int(new_entry)
            except:
                print("Please enter a valid number")
                new_entry = None
            else:
                new_entry = str(new_entry)
        if user_field == '3':
            try:
                datetime.datetime.strptime(new_entry, '%m/%d/%Y')
            except ValueError:
                print("Dates need to be valid and in MM/DD/YYYY format")
                new_entry = None
    new_edit = []
    with open('work_log.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row == task_list:
                row[dict_header[user_field]] = new_entry
                new_edit.append(row)
            else:
                new_edit.append(row)
    with open('work_log.csv', 'w', newline='') as file:
        fields = ['Task', 'Time Spent', 'Additional Notes', 'Date']
        write = csv.DictWriter(file, fieldnames=fields)
        write.writeheader()
        for row in new_edit:
            write.writerow({'Task': row['Task'], 
                            'Time Spent': row['Time Spent'], 
                            'Additional Notes': row['Additional Notes'], 
                            'Date': row['Date']})

def delete_entry(the_entry):
    edit = []
    with open("work_log.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row == the_entry:
                continue
            else:
                edit.append(row)
    with open("work_log.csv", 'w', newline='') as file:
        fields = ['Task', 'Time Spent', 'Additional Notes', 'Date']
        write = csv.DictWriter(file, fieldnames=fields)
        write.writeheader()
        for row in edit:
            write.writerow({'Task': row['Task'], 
                            'Time Spent': row['Time Spent'], 
                            'Additional Notes': row['Additional Notes'], 
                            'Date': row['Date']})

if __name__ == "__main__":
    menu()
    
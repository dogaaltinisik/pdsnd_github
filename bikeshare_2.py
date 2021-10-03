import time
import datetime
import pandas as pd
import numpy as np
import operator as op
import ipython_genutils


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = ""
    while len(city_input) == 0:
        city_input = input("Please type the name of the city to analyze:")
        city_input = city_input.lower()
        # Add some flexibilty to new york city as it can be called new york or NYC at times
        if op.__eq__(city_input,"new york") or op.__eq__(city_input,"NYC") or op.__eq__(city_input,"newyork"):
            city_input = "new york city"
        # Check if input is good or not   
        if op.__eq__(city_input,"chicago") or op.__eq__(city_input,"new york city") or op.__eq__(city_input,"washington"):
            print("Entry Recieved City Selected is: {}".format(city_input.title()))
        else: 
            print("Your input wasn't recognized: please enter one of the following:  chicago, new york city, washington")
            city_input = ""
    city = city_input        
    
    # get user input for month (all, january, february, ... , june)
    month_input = ""
    # make a list of months to reference
    months = ["january", "february", "march", "april", "may", "june"]
    # these months are out of range of the dataset
    other_months = ["july", "august", "september", "october", "november", "december"]
    
    while len(month_input) == 0:
        month_input = input("Please type the month name, or enter 'all' for all months: ").lower()
        # Check to see if string inputs are valid.
        if month_input == "all":
            print("You entered to pick all months january to june")
            month = month_input
        elif months.__contains__(month_input):
            print("Entry Recieved Month Selected is: {}".format(month_input.title())) 
            month = months.index(month_input)+1
        elif other_months.__contains__(month_input):
            print("Your selected month is: {} but it is out of range. Please try months between January and June".format(month_input.title()))
            month_input = ""
        else:
            print("Your input wasn't recognized, please enter a month name")
            month_input = ""

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_input = ""
    # make a list of days to reference
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    while len(day_input) == 0:
        day_input = input("Please type the day, or enter 'all' for all days: ").lower()
        # Check to see if string inputs are valid.
        if day_input == "all":
            print("You entered to pick all days Monday to Sunday")
            day = day_input
        elif days.__contains__(day_input):
            print("Entry recieved day selected is: {}".format(day_input.title()))
            day = days.index(day_input)+1
        else:
            print("Your input wasn't recognized, please enter a day name")
            day_input = ""
    

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour, month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df["start_hour"] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    # Convert from number to month for more readability
    months = ["january", "february", "march", "april", "may", "june"]
    month = months[df["month"].mode()[0]-1]
    print("The most common month is {} and it appeared {} many times.".format(month,df['month'].value_counts().iloc[[0]].values[0]))
    
    # display the most common day of week
    # Convert from number to day for more readability
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = days[df["day_of_week"].mode()[0]-1]
    print("The most common day is {} and it appeared {} many times.".format(day,df['day_of_week'].value_counts().iloc[[0]].values[0]))

    # display the most common start hour
    #Convert from 24hr to 12hr for more readability
    hours = ["1 AM", "2AM", "3AM", "4AM", "5AM", "6AM", "7AM", "8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM", "10PM", "11PM", "12 AM"]
    hour = hours[df["start_hour"].mode()[0]-1]
    print("The most common start hour is {} and it appeared {} many times.".format(hour,df["start_hour"].value_counts().iloc[[0]].values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is {} and it was used {} many times.".format(df["Start Station"].mode()[0],df["Start Station"].value_counts().iloc[[0]].values[0]))

    # display most commonly used end station
    print("The most common end station is {} and it was used {} many times.".format(df["End Station"].mode()[0],df["End Station"].value_counts().iloc[[0]].values[0]))

    # display most frequent combination of start station and end station trip
    df["Start and End Station"] = df["Start Station"] + " to " + df["End Station"]
    print("The most common combination trip is {} and it was used {} many times.".format(df["Start and End Station"].mode()[0],df["Start and End Station"].value_counts().iloc[[0]].values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    #Create travel time column
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["Travel Time"] = (df["End Time"] - df["Start Time"]).values
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    time_sum = datetime.timedelta()
    for times in df["Travel Time"]: time_sum += times
    time_average = (time_sum/len(df["Travel Time"])).round('1s')
    
    # display total travel time
    print("The total travel time was: {}".format(time_sum))

    # display mean travel time
    print("The average travel time was: {}".format(time_average))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_types = df['User Type'].value_counts().index.tolist()
    user_type_counts = df["User Type"].value_counts()
    # Display counts of user types
    if len(user_types) == 3:
        print("User types, \n{} : {}'s, \n{} : {}'s \nand {} : {}'s".format(user_type_counts[0], user_types[0], user_type_counts[1], user_types[1], user_type_counts[2], user_types[2]))
    elif len(user_types) == 2:
        print("User types, \n{} : {}'s \n{} : {}'s".format(user_type_counts[0], user_types[0], user_type_counts[1], user_types[1]))
    else: 
        print("All users were {} and there were {} many of them".format(user_types[0], user_type_counts[0]))
    # Display counts of gender
    print("Gender demographic is: {} {} users and {} {} users.".format(df["Gender"].value_counts()[0],df['Gender'].value_counts().index.tolist()[0],df["Gender"].value_counts()[1],df['Gender'].value_counts().index.tolist()[1]))

    # Display earliest, most recent, and most common year of birth
    print("The earliest year of birth is: {}".format(df["Birth Year"].sort_values().iloc[0].astype(int)))
    print("The most recent year of birth is: {}".format(df["Birth Year"].sort_values(ascending=False).iloc[0].astype(int)))
    print("The most common year of birth is: {}".format(int(df["Birth Year"].value_counts().index.tolist()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    """ 
    Asks user uf they would like to view raw data selected 5 rows at a time. 
    Prints the outputs to the console.
    Creates interactive menu style viewing with UP DOWN QUIT options.
    """
    #Settings so that data table doesn't get truncated
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.width', 0)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 2)
    
    next_step =""
    want_view =""
    #This variable is to remember which 5 rows of data are being viewed.
    index_holder = 0
    want_view = input("Would you like to view data, type(yes/y or no/n:  ").lower()
    while want_view == "yes" or want_view == "y" :
        print("You chose to view the raw data. Type 'u' to go up, 'd' to go down and 'quit' to quit viewing.")
        while next_step != "quit":
            print(df[index_holder:index_holder + 5])
            next_step = input("Type 'u' to go up, 'd' to go down and 'quit' to quit viewing:").lower()
            if op.__eq__(next_step,"quit"):
                print("Quitting")
                want_view = ""
                break
            elif op.__eq__(next_step,"u"):
                if index_holder == 0:
                    print("Can't go further up you are at top")
                else:
                    index_holder -= 5
                    print("Viewing upper 5 rows")
            elif op.__eq__(next_step,"d"):
                if index_holder == int(len(df)/5):
                    print("You have reached the end you cannot go further.")
                else:
                    index_holder += 5
                    print("Viewing lower 5 rows")
            else:
                print("Your input was invalid. Controls: 'u' to go up, 'd' to go down or 'quit' to quit viewing.")
            
    if op.__eq__(want_view,"no") or op.__eq__(want_view,"n"):
        print("You chose not to view data")
    print('-'*40)
    return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

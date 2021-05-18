import time
import pandas as pd
import numpy as np
import logging as log

# generate log file to trace program behavior using logging mechanism
# information about logging are got from stackoverflow website and python documentation.
log.basicConfig(filename="general.log", level=log.DEBUG, format='%(asctime)s -%(levelname)s- %(message)s')

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    log.debug(msg="Enter the method get_filters ")
    print('Hello! Let\'s explore some US bikeshare data!')
    is_user_input_right = True
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while is_user_input_right:
        # if the user enter an invalid value that can't be casted to string the except block will start the loop from scratch
        try:
            city = str (
                input("please enter a valid city name either washington or chicago or new york city in lower case "))
            log.debug("Entered city value is \t " + city)
            city = city.lower()
            if (city != "chicago") and (city != "new york city") and (city != "washington"):
                continue
        except ValueError:
            log.debug("The entered value for city can't be converted to string" + city)
            print("The entered city value can't be converted to string")
            continue

        # get user input for month (all, january, february, ... , june)
        try:
            month = str(input(
                "please enter a valid month name from january till june or all if you want all months between January & june "))
            log.debug("Entered value for month is \t" + month)
            month = month.lower()
            if (month != "january") and (month != "february") and (month != "march") and (month != "april") and (
                    month != "may") and (month != "june") and (month != "all"):
                continue
        except ValueError:
            log.debug("The Entered value for the month can't be converted to string")
            print("The entered month value can't be converted to string ")
            continue
        # get user input for day of week (all, monday, tuesday, ... sunday)
        try:

            day = str(input("Please enter a valid week day in lower case like sunday or type all to get all week days"))
            log.debug("The value entered for day was \t"+day)
            day = day.lower()
            if (day != "all") and (day != "sunday") and (day != "monday") and (day != "tuesday") and (
                    day != "wednesday") and (day != "thursday") and (day != "friday") and (day != "saturday") and (
                    day != "all"):
                continue
        except ValueError:
            log.debug("The entered value for day can't be converted to string ")
            print("The entered day value can't be converted to string")
            continue
        is_user_input_right = False

    print('-' * 40)
    log.debug("Exit get_filters method")
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
    log.debug("Enter the method load_data ")
    month = month.title()
    day = day.title()
    df = pd.read_csv("./" + CITY_DATA[city])
    # convert the date time to date time
    log.debug("Conver the start time & end Time to date time ")
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # get hour
    log.debug("Get hour & month digit values from start time column")
    df['Hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month
    # the information about get month_name & day_name functions are got from  Stakeoverflow website
    # https://stackoverflow.com/questions/30222533/create-a-day-of-week-column-in-a-pandas-dataframe-using-python
    log.debug("Get month name and day name ")
    df['Month Name'] = df['Start Time'].dt.month_name()
    df['Week Day'] = df['Start Time'].dt.day_name()
    # filter month
    if (month != "All"):
        log.debug("Filter data based on the month name ")
        df = df[df['Month Name'] == month]
    # filter day
    if (day != "All"):
        log.debug("Filter data based on the week day name ")
        df = df[df['Week Day'] == day]

    log.debug("Exit the method load_data")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    log.debug("Enter the method time_stats")
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    row, columns = df.shape
    log.debug("Check if the data after applied filters has data or not ")
    print(row)
    log.debug("The number of rows is \t"+str(row))
    if (row > 0):
        # display the most common month
        common_month = df['Month Name'].mode()[0]
        log.debug("Common month is \t"+common_month)
        print("Common Month is \t" + str(common_month))
        # display the most common day of week
        common_day = df['Week Day'].mode()[0]
        log.debug("Common day is \t"+common_day)
        print("Common week day is \t" + str(common_day))
        # display the most common start hour
        common_hour = df['Hour'].mode()[0]
        log.debug("Common Hour is \t"+str(common_hour))
        print("Common hour is \t" + str(common_hour))
        print("\nThis took %s seconds." % (time.time() - start_time))
    log.debug("Exit the method time_stats")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    log.debug("Enter the method station_stats")
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    log.debug("Common start station is\t"+common_start_station)
    print(common_start_station)
    # display most commonly used end station
    common_end_station = df['Start Station'].mode()[0]
    log.debug("Common End Station is \t"+common_end_station)
    print(common_end_station)
    # display most frequent combination of start station and end station trip
    df['Combine Start & End '] = df['Start Station'] + " - " + df['End Station']
    common_Stations = df['Combine Start & End '].mode()[0]
    common_start_station_in_combination, common_end_station_in_combination = str(common_Stations).split(sep="-")
    print("Common Stations are " + common_Stations)
    log.debug("Commnon start station in combination is \t "+common_start_station)
    log.debug("Common end station in combination is \t "+common_end_station_in_combination)
    print("common start station in the combination is \t" + common_start_station_in_combination)
    print("common end station in the combination is \t" + common_end_station_in_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    log.debug("Exit the method station_stats")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    log.debug("Enter the method trip_duration_stats")
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duaration = df['Trip Duration'].sum()
    print("Total Trip Duration is \t" + str(total_trip_duaration) + "  Second")
    log.debug("Total trip duration by Seconds is printed")
    total_trip_duration_days = total_trip_duaration / (60 * 60 * 24)
    print("Total Trip Duration is \t" + str(total_trip_duration_days) + " Day")
    log.debug("Total trip duration by days is printed")
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    log.debug("Mean Travel Time is printed")
    print("Mean Trip Duration is \t" + str(mean_travel_time) + " Second")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    log.debug("Exit the method trip_duration_stats")

def user_stats(df):
    """Displays statistics on bikeshare users."""
    log.debug("Enter the method user_stats")
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if ('User Type ' in df.columns):
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print(user_types)
        log.debug("User Types printed")
    # Display counts of gender

    # check if there is gender in the columns of data frame.
    print("### Gender Information ###")
    log.debug("Check if the Gender column in the data frame or not")
    if ("Gender" in df.columns):
        print("### User Type Information ###")
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
        log.debug("Gender values are printed")
    # Display earliest, most recent, and most common year of birth
    print("### Birth Year Information ###")
    # df['Birth Year']=df['Birth Year'].astype(int)
    if('Birth Year' in df.columns):
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()
        log.debug("Earliest year is \t"+str(earliest_year))
        log.debug("recent year is\t"+str(recent_year))
        print("Earliest Year \t" + str(int(earliest_year)))
        print("Recent Year \t" + str(int(recent_year)))
        print("Common Year \t" + str(int(common_year)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    log.debug("Exit the method user_stats")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        log.debug("Calling the stats methods")
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        log.debug("Do you want to continue")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

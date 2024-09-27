import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'data/chicago.csv', 'Chicago': 'data/chicago.csv',
             'New York City': 'data/new_york_city.csv', 'New york city': 'data/new_york_city.csv',
             'new york city': 'data/new_york_city.csv', 'washington': 'data/washington.csv',
             'Washington': 'data/washington.csv'}

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    while city not in CITY_DATA.keys():
        print("\nWelcome to this program. Please choose your city:")
        print("\n1. Chicago 2. New York City 3. Washington")
        print("\nAccepted input:\nFull name of city; not case sensitive (e.g. chicago or CHICAGO).\nFull name in title case (e.g. Chicago).")
        city = input().lower()
        if city not in CITY_DATA.keys():
            print("\nInvalid input. Please choose from the available cities: Chicago, New York City, or Washington.")
            print("\nRestarting...")
    print(f"\nYou have chosen {city.title()} as your city.")

    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month, between January to June, for which you're seeking the data:")
        print("\nAccepted input:\nFull month name; not case sensitive (e.g. january or JANUARY).\nFull month name in title case (e.g. April).")
        print("\n(You may also opt to view data for all months, please type 'all' or 'All' or 'ALL' for that.)")
        month = input().lower()
        if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please choose from: January, February, March, April, May, June, or 'all'.")
            print("\nRestarting...")
    print(f"\nYou have chosen {month.title()} as your month.")

    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week of your choice for which you're seeking the data:")
        print("\nAccepted input:\nDay name; not case sensitive (e.g. monday or MONDAY).\nDay name in title case (e.g. Monday).")
        print("\n(You can also put 'all' or 'All' to view data for all days in a week.)")
        day = input().lower()
        if day not in DAY_LIST:
            print("\nInvalid input. Please choose from: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all'.")
            print("\nRestarting...")
    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*80)
    return city, month, day

def load_data(city, month, day):
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month!= 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day!= 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month = df['month'].mode()[0]
    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")
    popular_day = df['day_of_week'].mode()[0]
    print(f"\nMost Popular Day: {popular_day}")
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"\nMost Popular Start Hour: {popular_hour}")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}")
    common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most commonly used end station: {common_end_station}")
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]
    print(f"\nThe most frequent combination of trips are from {combo}.")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_type = df['User Type'].value_counts()
    print(f"The types of users by number are given below:\n\n{user_type}")
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

def display_data(df):
    BIN_RESPONSE_LIST = ['yes', 'no']
    while True:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        rdata = input().lower()
        if rdata == "yes":
            print("\nHere are the first 5 rows of data:")
            print(df.head())
            break
        elif rdata == "no":
            break
        else:
            print("\nInvalid input. Please enter 'yes' or 'no'.")
    while True:
        print("\nDo you wish to view more raw data?")
        rdata = input().lower()
        if rdata == "yes":
            counter = 5
            while rdata == "yes":
                print(f"\nRows {counter}:{counter + 5} of data:")
                print(df[counter:counter + 5])
                counter += 5
                rdata = input().lower()
            break
        elif rdata == "no":
            break
        else:
            print("\nInvalid input. Please enter 'yes' or 'no'.")
    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower()!= 'yes':
            break

if __name__ == "__main__":
    main()



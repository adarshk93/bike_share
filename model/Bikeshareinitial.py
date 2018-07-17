""""we  first create a function either by main or keeping at starting
steps need to done ask user to enter the city ,month, day of the week for  initial setup
then call a function to give the data set wrt to that"""
import pandas as pd
import numpy as np


def user_input():
    while True:
        days = None
        months = None
        city = input("Please enter the city name ('chicago', 'new york', 'washington'): ")
        filter = input("would you like to filter it by month or day or both? \n"
                       "if both - type both \n"
                       "if month- type month\n"
                       "if day- type day\n"
                       "if none - type none\n")
        if filter == 'none':
            pass
        elif filter == 'both':
            months = month()
            days = day()
        elif filter == 'month':
            months = month()
        elif filter == 'day':
            days = day()

        print("entered Details are as follows \ncity:{}\nFilter_month:{}\nFilter_day:{}\n".format(city, months, days))
        confirmation = input("Press Y for yes or N to re enter the data: \n ")
        if confirmation == 'Y':
            inp_validation(city, months, days, filter)
        elif confirmation == 'N':
            user_input()
        else:
            print("Unknown choice!!")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break;



def day():
    days = input("please enter the day name (e.g Wednesday): ")
    return days


def month():
    months = input("please enter the Month (e.g March): ")
    return months


def inp_validation(city, month, day, filter):
    cities = ['chicago', 'new york', 'washington']
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'saturday', 'sunday']
    if city in cities:
        if filter == 'both':
            if month in months and day in days:
                statsgen(city, month, day)
            else:
                help_message()
        elif filter == 'month':
            if month in months:
                statsgen(city, month, day)
            else:
                help_message()
        elif filter == 'day':
            if day in days:
                statsgen(city, month, day)
            else:
                help_message()
        elif filter == 'none':
            statsgen(city, month, day)
    else:
        help_message()
    return None


def help_message():
    return print("Sorry we don't have the matching records for these entries, Please re-enter")


def statsgen(city, month, day):
    print('Hold on Stats are on their way\n')
    print('*********************************\n')
    filename = city + '.csv'
    dataframes = pd.DataFrame(pd.read_csv(filename))
    # convert start and end time to datetime
    dataframes['Start Time'] = pd.to_datetime(dataframes['Start Time'])
    dataframes['End Time'] = pd.to_datetime(dataframes['End Time'])

    # create a derived column to capture month and day info
    dataframes['month'] = dataframes['Start Time'].dt.month
    dataframes['day'] = dataframes['Start Time'].dt.weekday_name

    # if any particular month is being selected
    # filer based on the particular month
    if month:
        dataframes = month_filter(dataframes, month)
    # if any particular day is being selected
    # filer based on the particular day
    if day:
        dataframes = days_filter(dataframes, day)

    dataframes = null_filter(dataframes)
    popular_hour = most_pop_hour(dataframes, day)
    popular_stations = most_pop_stations(dataframes)
    trip_details = trip_durations(dataframes)
    userstats = (user_info(dataframes, city))
    print('Popular times of travel: \n' \
          ' Most popular hour is: {} \n Most popular day is: {} \n\n' \
          'Popular stations and trip:\n'
          '  Most popular starting  Station is: {}\n  Most popular ending station is: {}\n  Most common trip from start to end : {}\n\n' \
          'Trip duration (mins):\n'\
          ' Total trip duration is: {}\n  Avg duration is: {}\n\n'\
          'User info:\n' \
          '  User details: {}\n  Gender details: {}\n  Oldest bike rider: {}\n  Youngest bike  rider: {}\n' \
          '  Most occuring birth year: {}\n\n '.format(popular_hour[0],
                                                 popular_hour[1],
                                                 popular_stations[0],
                                                 popular_stations[1],
                                                 popular_stations[2],
                                                 trip_details[0],
                                                 trip_details[1],
                                                 userstats[0],
                                                 userstats[1],
                                                 userstats[2],
                                                 userstats[3],
                                                 userstats[4]
                                                 ))
    print('*********************************\n')
    return None


"""" This function is used to filter the data month wise   """


def month_filter(dataframes, month_name):
    index_month = 0
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index_month = months.index(month_name) + 1
    dataframes[dataframes.month == index_month]
    return dataframes[dataframes.month == index_month]


"""" This function is used to filter the data day wise   """


def days_filter(dataframes, day):
    return dataframes[(dataframes.day == day)]


"""" This function generate following statistics
    Most popular hour , Most popular day"""


def most_pop_hour(dataframes, day):
    dataframes['hour'] = dataframes['Start Time'].dt.hour
    most_pop_hour = []
    most_pop_hour.append(dataframes['hour'].mode()[0])
    # popular day is only applicable when the filter is all
    if day is None:
        most_pop_hour.append(dataframes['day'].mode()[0])
    else:
        most_pop_hour.append('NA')
    return most_pop_hour


"""" This function generate following statistics
   Most popular starting  Station , Most popular ending station , Most common trip from start to end"""


def most_pop_stations(dataframes):
    most_pop_stations = []
    most_pop_stations.append(dataframes['Start Station'].mode()[0])
    most_pop_stations.append(dataframes['End Station'].mode()[0])
    start_end = dataframes['Start Station'] + '  :  ' + dataframes['End Station']
    most_pop_stations.append(start_end.mode()[0])
    return most_pop_stations


"""" This function generate following statistics
  Total trip duration ,Avg duration """


def trip_durations(dataframes):
    trip_durations = []
    # dataframes['diff'] = (dataframes[('End Time')] - dataframes[('Start Time')]).dt.seconds
    trip_durations.append(int(dataframes['Trip Duration'].sum() / 60))
    trip_durations.append(int(dataframes['Trip Duration'].mean() / 60))
    return trip_durations


"""" This function generate following statistics
	User detials, Gender details ,Oldest bike rider, Youngest bike  ride \
     Most occuring birth year """


def user_info(dataframes, city):
    user_info = []
    user_info.append(dataframes['User Type'].value_counts().to_dict())
    if 'Gender' and 'Birth Year' in dataframes:
        user_info.append(dataframes['Gender'].value_counts().to_dict())
        user_info.append(int(dataframes['Birth Year'].min()))
        user_info.append(int(dataframes['Birth Year'].max()))
        user_info.append(int(dataframes['Birth Year'].mode()[0]))
    # else clause is used to handle for washington data set as it does not have gender  and birth info
    else:
        user_info.append('NA')
        user_info.append('NA')
        user_info.append('NA')
        user_info.append('NA')
    return user_info


""" null_filter function is used to either drop null values or replace it with the most occuring value ()"""


def null_filter(dataframes):
    column_list = dataframes.columns.tolist()
    for i in column_list:
        if dataframes[i].isnull().sum() > 0:
            if dataframes[i].count() / 10 > dataframes[i].isnull().sum():
                dataframes.dropna(subset=[i], inplace=True)
            else:
                dataframes[i].fillna(dataframes[i].mode()[0], inplace=True)
    return dataframes


if __name__ == '__main__':
    print("Welcome to bikeshare data analysis portal\n")

    user_input()

# filename = ("Chicago.csv")
# dataframes = pd.DataFrame(pd.read_csv(filename))
# print(dataframes['Start Station'])

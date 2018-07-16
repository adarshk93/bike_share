"""" The below program is mainly implemented to support flask in picture
statsgen function is called by stat_details function which will compute all the details   """
import pandas  as  pd


def dropdown_values():
    cities = ['chicago', 'new york', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    return [cities,months,days]

def statsgen(city,month,day):
    filename = city+'.csv'
    dataframes = pd.DataFrame(pd.read_csv(filename))
	#convert start and end time to datetime
    dataframes['Start Time'] = pd.to_datetime(dataframes['Start Time'])
    dataframes['End Time'] = pd.to_datetime(dataframes['End Time'])
	
	# create a derived column to capture month and day info
    dataframes['month'] = dataframes['Start Time'].dt.month
    dataframes['day'] = dataframes['Start Time'].dt.weekday_name
	
	#if any particular month is being selected 
	#filer based on the particular month
    if (month != 'all'):
        dataframes = month_filter(dataframes,month)
	#if any particular day is being selected 
	#filer based on the particular day
    if (day != 'all'):
        dataframes = days_filter (dataframes,day)

    dataframes = null_filter(dataframes)
    popular_hour=most_pop_hour(dataframes,day)
    popular_stations=most_pop_stations(dataframes)
    trip_details = trip_durations(dataframes)
    userstats = user_info(dataframes,city)

    # Function returns the value in html format as its rendered in a html page
    return '<p style="font-weight:bold">Popular times of travel' \
           '<ol> <li> Most popular hour is: {} </li> <li> Most popular day is:   {} </li> </ol>  ' \
           '<p style="font-weight:bold"> Popular stations and trip' \
           ' <ol> <li> Most popular starting  Station is: {} </li> <li> Most popular ending station is: {} </li> <li> Most common trip from start to end : {} </li></ol> ' \
           '<p style="font-weight:bold"> Trip duration (mins)' \
           '<ol> <li> Total trip duration is: {} </li> <li> Avg duration is: {} </li> </ol> ' \
           ' <p style="font-weight:bold"> User info' \
           '<ol> <li>  User detials: {} </li> <li> Gender details: {} </li> <li> Oldest bike rider: {} </li> <li> Youngest bike  rider: {}</li> ' \
           '<li>Most occuring birth year: {} </li> </ol> ' \
        .format(popular_hour[0],
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
                )

"""" This function is used to filter the data month wise   """
def month_filter(dataframes,month_name):
    index_month =0
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    index_month = months.index(month_name) + 1
    dataframes[dataframes.month==index_month]
    return dataframes[dataframes.month==index_month]
	
"""" This function is used to filter the data day wise   """
def days_filter(dataframes,day):
    return dataframes[(dataframes.day == day)]

		
"""" This function generate following statistics
    Most popular hour , Most popular day"""
def most_pop_hour(dataframes,day):
    dataframes['hour'] = dataframes['Start Time'].dt.hour
    most_pop_hour=[]
    most_pop_hour.append(dataframes['hour'].mode()[0])
	#popular day is only applicable when the filter is all 
    if day=='all':
        most_pop_hour.append( dataframes['day'].mode()[0])
    else:
        most_pop_hour.append('NA')
    return most_pop_hour

		
"""" This function generate following statistics
   Most popular starting  Station , Most popular ending station , Most common trip from start to end"""
def  most_pop_stations(dataframes):
    most_pop_stations=[]
    most_pop_stations.append(dataframes['Start Station'].mode()[0])
    most_pop_stations.append( dataframes['End Station'].mode()[0])
    start_end = dataframes['Start Station']+'  :  '+dataframes['End Station']
    most_pop_stations.append(start_end.mode()[0])
    return most_pop_stations

"""" This function generate following statistics
  Total trip duration ,Avg duration """	
def trip_durations(dataframes):
    trip_durations = []
    #dataframes['diff'] = (dataframes[('End Time')] - dataframes[('Start Time')]).dt.seconds
    trip_durations.append(int(dataframes['Trip Duration'].sum()/60))
    trip_durations.append(int(dataframes['Trip Duration'].mean()/60))
    return trip_durations

"""" This function generate following statistics
	User detials, Gender details ,Oldest bike rider, Youngest bike  ride \
     Most occuring birth year """
def user_info(dataframes,city):
    user_info = []
    user_info.append(dataframes['User Type'].value_counts().to_dict())
    if 'Gender' and 'Birth Year' in dataframes:
        user_info.append(dataframes['Gender'].value_counts().to_dict())
        user_info.append(int(dataframes['Birth Year'].min()))
        user_info.append(int(dataframes['Birth Year'].max()))
        user_info.append(int(dataframes['Birth Year'].mode()[0]))
	# else clause is used to handle for washington data set as it does not have gender  and birth info
    else :
        user_info.append('NA')
        user_info.append('NA')
        user_info.append('NA')
        user_info.append('NA')
    return user_info

""" null_filter function is used to either drop null values or replace it with the most occuring value ()"""
def null_filter(dataframes):
    column_list = dataframes.columns.tolist()
    for i in column_list :
        if dataframes[i].isnull().sum() > 0:
            if dataframes[i].count() / 10 > dataframes[i].isnull().sum():
                dataframes.dropna(subset=[i], inplace = True)
            else:
                dataframes[i].fillna(dataframes[i].mode()[0], inplace=True)
    return dataframes






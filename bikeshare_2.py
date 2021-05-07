import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_LIST = ['all','january', 'february', 'march', 'april', 'may', 'june']
DAY_LIST = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

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
    while True:
    	try:
    		city = input('Enter the city name(chicago, new york city, washington): ')
    		if city in CITY_DATA.keys():
    			break
    		else:
    			raise ValueError('Type error...Please enter a vaild city')
    	except:
    		print('Type error...Please enter a vaild city')
    # get user input for month (all, january, february, ... , june)
    while True:
    	try:
    		month = input('Enter the month(all, january, february, ... , june): ')
    		if month in MONTH_LIST:
    			break
    		else:
    			raise ValueError('Type error...Please enter a vaild city')
    	except:
    		print('Type error...Please enter a vaild city')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
    	try:
    		day = input('Enter the day of week(all, monday, tuesday, ... sunday): ')
    		if day in DAY_LIST:
    			break
    		else:
    			raise ValueError('Type error...Please enter a vaild city')
    	except:
    		print('Type error...Please enter a vaild city')
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Start day_of_week:', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is', start_station)
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station is', end_station)

    # display most frequent combination of start station and end station trip

    popular_trip=df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most popular trip from start to end is: \n {}".format(popular_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('the total travel time:', total_travel_time)
    print('the mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('counts of user types: \n',counts_of_user_types)
    # Display counts of gender
    if 'Gender' in df.columns:
    	counts_of_gender = df['Gender'].value_counts()
    	print('counts of gender: \n',counts_of_gender)
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
    	earliest_YOB = df['Birth Year'].min()
    	most_recent_YOB = df['Birth Year'].max()
    	most_common_YOB = df['Birth Year'].mode()[0]
    	print('The earliest date of birth is ',earliest_YOB)
    	print('The most rescent date of birth is ',most_recent_YOB)
    	print('The most common birth year is ',most_recent_YOB)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_data(df):
	"""Displays trip row data on bikeshare users"""
	i = 0
	show_count = 5
	trip_data = input('Would you like to view individual trip data? Enter yes or no.\n')
	while True:
        #check if the df in the final rows
		if i > len(df.index):
			print(df.iloc[i - show_count - len(df.index): 0])
			print('no more data')
			break
		elif trip_data.lower() == 'yes':
			print(df.iloc[i:i + show_count])
			i += show_count
		elif trip_data.lower() == 'no':
			break
		else:
			print('Type error...Please enter a vaild city')
		trip_data = input('Would you want to view more data? Enter yes or no.')
		
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

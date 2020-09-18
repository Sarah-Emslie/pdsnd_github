import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month
        filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a
    # while loop to handle invalid inputs
    while True:

        city = input(
        '\nWould you like to learn about Chicago, New York City or Washington?\n'
        ).lower()
        
        if city not in cities:
            print('\nPlease choose from the following: Chicago, New York City,')
            (' or Washington.\n')
        else:
            print('\nThanks! You have chosen to learn about {}.'.format
            (city.title()))
            break

    # get user input for month (all, january, february, ... , june)
    while True:

        user_month = input(
        '\nWhich month you are interested in? (For all months, type \'all\')\n')
        month = user_month.lower()

        if month not in months:
            print('Sorry! We currently only have data for January to June!')
            print('Please ensure you\'re entering the name of the month.\n')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:

        user_day = input(
        '\nWhich day are you interested in? (For every day, type \'all\')\n')
        day = user_day.lower()

        if day not in days:
            print(
            '\nPlease check you\'re entering the name of the day or \'all\'.\n')
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month
        filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract required elements from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['time'] = df['Start Time'].dt.time

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding integer
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month as a NAME
    popular_mth = df['month'].mode()[0]
    mth_i = popular_mth
    popular_mth_name = calendar.month_name[mth_i]
    print(
    'If you chose \'all\' earlier, the most popular month of travel is {}.'
    .format(popular_mth_name))
    print('Otherwise, what follows relates to your chosen month.')

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print(
    '\nIf you chose \'all\' earlier, the most popular day of travel is {}.'
    .format(popular_day))
    print('Otherwise, what follows relates to your chosen day.')

    # display the most common start hour
    popular_hr = df['hour'].mode()[0]
    popular_hr_fin = popular_hr + 1
    print('\nThe most popular hour of travel is between {} and {}.'
    .format(popular_hr, popular_hr_fin))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('\n{} is the most commonly used start station.'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('\n{} is the most commonly used end station.'.format(popular_end))

    # display most frequent combination of start station and end station trip
    df['Trip Combination'] = (df['Start Station'] + ' to/from '
    + df['End Station'])
    popular_combo = df['Trip Combination'].mode()[0]
    print('\nThe most popular trip is {}.'.format(popular_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duratn_float = df['Trip Duration'].sum() / 60 / 60 / 24
    total_duratn = int(total_duratn_float)
    print(
    '\nThe total travel time for the chosen period is {} days.'
    .format(total_duratn))

    # display mean travel time
    mean_duratn_float = df['Trip Duration'].mean() / 60
    mean_duratn = int(mean_duratn_float)
    print('\nThe average journey time is {} minutes.'.format(mean_duratn))

    # display longest trip duration
    long_duratn_float = df['Trip Duration'].max() / 60 / 60
    long_duratn = int(long_duratn_float)
    print('\nThe longest trip duration is a whopping {} hours!'
    .format(long_duratn))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types_split = df['User Type'].value_counts().to_frame()
    print(
    'Bikeshare users for your chosen month(s) and day(s) are split as follows:')
    print(types_split)

    # Display counts of gender *Washington data is missing!
    # Use a try/except block to handle the KeyError thrown up
    try:
        gender_split = df['Gender'].value_counts().to_frame()
    except KeyError:
        print('\nSorry, we don\'t have gender data for your chosen city.')
    else:
        print('\nThe gender split of users is:\n {}'.format(gender_split))


    # Display earliest, most recent, and most common year of birth
    # *Washington data is missing! Use a try/except block to handle
    try:
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
    except KeyError:
        print('\nSorry, we don\'t have birth year data for your chosen city.')
    else:
        print('\nThe oldest user was born in {}.'.format(oldest_user))
        print('The youngest user was born in {}.'.format(youngest_user))
        print('The most common year of birth is {}.'.format(common_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Prompt the user if they want to see 5 lines of raw data, display_data
    that data if yes and continue until user says no"""

    # Set a counter to 0 and prompt the user
    counter = 0
    user_prompt = (input(
    '\nWould you like to see 5 lines of raw data? Please enter yes or no.\n')
    .lower())

    # Use a while loop to continue prompting/displaying until user says 'no'
    while True:
        if user_prompt != 'no':
            print(df.iloc[counter:counter + 5])
            counter += 5
            user_prompt = (input(
            '\nWould you like to see more raw data? Please enter yes or no.\n')
            .lower())
        else:
            break

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Please enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

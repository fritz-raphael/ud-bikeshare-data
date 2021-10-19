import os, time, pandas as pd, numpy as np, sys
from datetime import datetime

# Always show the full set of columns (instead of collapsing to window size)
pd.set_option('display.max_columns', 200)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday',
             'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Pandas-version: {}".format(pd.__version__))
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Please enter a city (Chicago, New York City, or Washington).\n")\
                    .lower().strip()
            if city not in CITY_DATA:
                print('I can\'t recognize this city. \nPlease try again.\n')
                continue
            else:
                print('You have seleted {}.\n'.format(city.title()))
            break
        except Exception as e:
            print('There was an exception: ', e, '\n')
            print('Let\'s try again. \n')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter a specific month (January to June) " \
                          "or enter 'all'.\n").lower().strip()
            if month != 'all':
                if month not in months:
                    print('This month is not in the list.\n Please try again.')
                    continue
                else:
                    print('You have selected {}.'.format(month.title()))
            else:
                print('You have selected all months.\n')
            break
        except Exception as e:
            print('There was an error:\n', e, '\n')
            print("Let's try again. ")
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("And now, please enter a day (monday to sunday) " \
                        "or enter 'all'.\n").lower().strip()
            if day != 'all':
                if day not in days_of_week:
                    print('I can\'t recognize this day.\n Please try again.')
                    continue
                else:
                    print('You have selected {}.'.format(day.title()))
            else:
                print('You have selected all days of the week.\n')
            break
        except Exception as e:
            print('There was an error:\n', e, '\n')
            print("Let's try again. ")
            continue

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

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, CITY_DATA[city])
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError as err:
        print('File not found.')
        sys.exit()

    # convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], yearfirst = True)
    df['End Time'] = pd.to_datetime(df['End Time'], yearfirst = True)

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1 # Since January is '1' in df

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days_of_week.index(day)   # Since Monday is 0
        df = df[df['day_of_week'] == day]
    return df

def show_raw_data(df):
    """Prompts the user if they want to see five lines of raw data at a time."""

    raw_data = input("Do you want to see five rows of the original data?\n"\
    "Type 'Yes' or anything else.\n").lower().strip()
    while raw_data == 'yes':
        for five_rows in range(0, df.shape[0], 5):
            if 'Gender' in df.columns:
                print(df.iloc[:, 1:8].iloc[five_rows:(five_rows+5)])
            else:
                print(df.iloc[:, 1:6].iloc[five_rows:(five_rows+5)])
            try:
                raw_data = input("\nDo you want to see five more rows?\n")\
                .lower().strip()
                if raw_data != 'yes':
                    break
                else:
                    continue
            except Exception as e:
                print(e)
                break

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate the most common month
    if month == 'all':
        month_mode = df['month'].mode()[0]

    # Calculate the most common day of the week
    if day == 'all':
        day_mode = df['day_of_week'].mode()[0]

    # Calculate the most common starting hour
    df['hour'] = df['Start Time'].dt.hour
    hour_mode = df['hour'].mode()[0]
    hour_am_pm = datetime.strptime(str(hour_mode), "%H")

    # display the most common month
    # display the most common day of week
    # display the most common start hour
    # Change timeformat due to platform
    if sys.platform != "win32":
        timeformat = "%-I %p"
    else:
        timeformat = "%#I %p"

    if month != 'all' and day != 'all':
        print("On {} of {} 2017, most bikes were rented in the hour after {}."\
              .format(day.title() + 's', month.title(),
              hour_am_pm.strftime("%#I %p")))
    elif month != 'all' and day == 'all':
        print("In {} 2017, most bikes were rented on {} "\
              "and in the hour after {}.".format(month.title(),
              (days_of_week[day_mode].title() + 's'),
              hour_am_pm.strftime(timeformat)))
    elif month == 'all' and day != 'all':
        print("On all {} from January to June 2017, " \
              "most bikes were rented in {}.\n"\
              "Most bikes were rented in the hour after {}."\
              .format(day.title() + 's', months[month_mode-1].title(),
              hour_am_pm.strftime(timeformat)))
    elif month == 'all' and day == 'all':
        print("From January to June 2017, most bikes were rented in {}.\n"\
              "The busiest days of the week were {} \n"\
              "and most bikes were rented in the hour after {}."\
              .format(months[month_mode-1].title(),
              days_of_week[day_mode].title() + 's',
              hour_am_pm.strftime(timeformat)))

    # Maybe it would be cool to round this number.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]

    # display most commonly used start station
    # display most commonly used end station
    if most_common_start_station == most_common_end_station:
        print("'{}' is the most common station both for start and end station."\
        .format(most_common_start_station))
    else:
        print("The most common start station is {} "\
              "and the most common end station is {}"\
              .format(most_common_start_station, most_common_end_station))

    # display most frequent combination of start station and end station trip
    # create a filtered table with only the most common combination
    df['station_combination'] = df['Start Station'] + "%" + df['End Station']
    most_common_combination = df['station_combination'].mode()[0]
    common_combination_table = \
        df.loc[(df['station_combination'] == most_common_combination),
        ['Start Station', 'End Station']]
    if common_combination_table['Start Station']\
        .mode()[0] == common_combination_table['End Station'].mode()[0]:
        print("The most common trip is a roundtrip that starts and ends on {}"\
              .format(common_combination_table['Start Station'].mode()[0]))
    else:
        print("The most common trip is from '{}' to '{}'."\
              .format(common_combination_table['Start Station'].mode()[0],
              common_combination_table['End Station'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    trip_count = df['Trip Duration'].count()
    trip_sum = df['Trip Duration'].sum()
    trip_sum_seconds = trip_sum.total_seconds()
    days, remainder = divmod(trip_sum_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("Total travel time: {} days, {} hours, {} minutes, and {} seconds."\
          .format(int(days), int(hours), int(minutes), int(seconds)))
    print("Number of trips:", trip_count)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean().total_seconds() / 60
    print("Average travel time per trip: {} minutes."\
          .format(round(mean_travel_time,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = pd.unique(df['User Type'])

    for user_type in user_types:
        try:
            print(df['User Type'].value_counts()[user_type], user_type + 's')
        except:
            continue
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = pd.unique(df['Gender'])

        for gender_type in gender_types:
            try:
                print(df['Gender'].value_counts()[gender_type], gender_type + 's')
            except:
                continue
    else:
        print("No data on users' gender available.")

    print()
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Earliest year of birth:", int(df['Birth Year'].min()))
        print("Most recent year of birth:", int(df['Birth Year'].max()))
        print("Most common year of birth:", int(df['Birth Year'].mode()[0]))
    else:
        print("No data on users' year of birth available.")

    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')\
                  .lower().strip()
        if restart != 'yes':
            print("Exiting program.")
            break


if __name__ == "__main__":
	main()

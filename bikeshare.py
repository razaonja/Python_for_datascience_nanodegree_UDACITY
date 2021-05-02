
# coding: utf-8

# In[1]:


import pandas as pd
import operator
import datetime
import time
import subprocess
import sys

def import_or_install(package):
    #install a module 
    #source stackoverflow.com

    subprocess.check_call([sys.executable, "-m", "pip", "install", package])  

try:
    # try to import fuzzywuzzy
    from fuzzywuzzy import fuzz
    
except ModuleNotFoundError:
    #if not installed then install and import
    import_or_install('fuzzywuzzy')
    from fuzzywuzzy import fuzz

# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[3]:


def Check_similarity(input_data,default_list):
    #This function checks the similarity ratio between the input  and  our default data list
    # source : https://pypi.org/project/fuzzywuzzy/
    input_data=input_data.lower()
    dic_ration={}
    
    #ratio calculation 
    for l_d in default_list:
        ratio=fuzz.ratio(input_data,l_d.lower())
        dic_ration[l_d]=ratio
    key_prob=max(dic_ration.items(),key=operator.itemgetter(1))[0]
    
    # Similarity Code meaning: 0-> 'Not found', 1-> 'There is similarity', 2->'exact matching'
    if dic_ration[key_prob] < 50:
        return (input_data,'NoFound',0)
    elif dic_ration[key_prob]==100:
        return (input_data,key_prob,2)
    else:
        return (input_data,key_prob,1)


# In[4]:


def check_input(filter_data):   
    if filter_data[2]==2:
        return filter_data[1]
    elif filter_data[2]==1:
        i=input('Do you mean \'{}\' ?'.format(filter_data[1].title()))
        if i.lower()in ['ys','yes','ys','ye','y']:
            return filter_data[1]
        else:
            print('Sorry, your input is not valid! Please choise again! ')
    else:
        print('Sorry, your input is not valid! Please choise again! ')
        return None   


# In[5]:


def get_month_name(monthinteger):
    # get month name from month in integer format
    month = datetime.date(1900, monthinteger, 1).strftime('%B')
    return month.lower()


# In[6]:


def get_filters():
    
    #List of default data (City, month and WeekName)
    lst_city=['chicago', 'new york city', 'washington','all']
    lst_month=['january', 'february', 'march', 'april', 'may', 'june','all']
    lst_week_name=['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] 
    
    city_value=None
    month_value=None
    week_value=None
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city_value == None:
        city_value=input('Please enter a city (chicago, new york city, washington):')
        city=Check_similarity(city_value,lst_city)
        city_value=check_input(city)
        
    # get user input for month (all, january, february, ... , june)
    while month_value==None:
        month_value=input('Which Month (all, january, ... june)?  ')
        month=Check_similarity(month_value,lst_month)
        month_value=check_input(month)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while week_value==None:
        week_value=input('Which day? (all, monday, tuesday, ... sunday)?  ')
        week=Check_similarity(week_value,lst_week_name)
        week_value=check_input(week) 
    return city_value,month_value,week_value    


# In[7]:


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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Month'] =df['Month'].apply(lambda x : get_month_name(x))
   
    df['Week_day']=df['Start Time'].dt.weekday_name
    df['Week_day']=df['Week_day'].apply(lambda x : x.lower())
    if day!='all':
        df=df[df['Week_day']==day]
    if month!='all':
        df=df[df['Month']==month]
    return df


# In[8]:


def user_stats(df,city):
    
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Numbers of user by type :')
    print(df['User Type'].value_counts())
    print('_'*10)

    
    if city!='washington':
        # Display counts of gender
        print('Numbers of user by gender :')
        print(df['Gender'].value_counts())
        print('_'*10)

        # Display earliest, most recent, and most common year of birth
        earliest=df['Birth Year'].min()
        recent=df['Birth Year'].max()
        mode=df['Birth Year'].mode()[0]
        print('The earliest year of birth: {}'.format(int(earliest)))
        print('The most common year of birth: {}'.format(int(mode)))
        print('The most recent year of birth: {}'.format(int(recent)))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


# In[9]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time:')
    total_seconds=df['Trip Duration'].sum()
    days=int(((total_seconds//60)//60)//24)
    hours=int(((total_seconds//60)//60)%24)
    minutes=int((total_seconds//60)%60)
    seconds=int(round((total_seconds%60),0))
    
    print('{} days {} hours {} minutes {} seconds , total in seconds= {}'.format(days,hours,minutes,seconds,total_seconds))
    print('_'*10)
    # display mean travel time
    print('Average Travel Time:')
    mean_seconds=df['Trip Duration'].mean()
    days=int(((mean_seconds//60)//60)//24)
    hours=int(((mean_seconds//60)//60)%24)
    minutes=int((mean_seconds//60)%60)
    seconds=int(round((mean_seconds%60),0))
    
    print('{} days {} hours {} minutes {} seconds , Average in seconds= {}'.format(days,hours,minutes,seconds,mean_seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


# In[10]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly used Start Station : {}'.format(df['Start Station'].mode()[0]))
    

    # display most commonly used end station
    print('Most Commonly used End Station : {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df_trip=(df['Start Station']+ ' -> ' +df['End Station'])
    print('Most Commonly Used Station in End and Start Station: {}'.format(df_trip.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




# In[32]:


def time_stats(df,day,month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month=='all':
        #if month is given then we don't need to display the most common month
        common_month=df['Month'].mode()[0]
        print('The Most Common Month: {}'.format(common_month.title()))

    # display the most common day of week
    if day=='all':
        #if day is given then we don't need to display the most common day
        common_day = df['Week_day'].mode()[0]
        print('The Most Common Day Of week: {}'.format(common_day.title()))

    # display the most common start hour
    common_start_hour=df['Start Time'].dt.hour.mode()[0]
    print('The Most Common Start Hour: {}'.format(common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[35]:


print('\n\n\n\n Hello and Welcom to this program!\n\n')
print('Let\'s explore some data in the US BIKESHARE Database...\n\n')

def display_data(df):
    from_i=0
    to_i=4
    while to_i<len(df):
        df=df[['Start Time', 'End Time', 'Trip Duration','Start Station', 'End Station', 'User Type']]
        print(df.loc[from_i:to_i])
        f_more_rows=input('Press \'ENTER\' for more rows!')
        if f_more_rows=='':#if user an empty input then display 5 more rows
            from_i+=5
            to_i+=5
        else:
            break
def main():
    while True:
        city, month, day = get_filters()
        df=load_data(city,month,day)
        user_stats(df,city)
        trip_duration_stats(df)
        station_stats(df)
        time_stats(df,day,month)
        f_display_data=input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        if f_display_data.lower()=='yes':
            display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        else:
            print('-'*40)
            print('-'*40)
            print('-'*40)

if __name__ == "__main__":
    main()

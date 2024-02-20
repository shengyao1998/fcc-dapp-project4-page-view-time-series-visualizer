import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
filepath = 'fcc-forum-pageviews.csv'
df = pd.read_csv(filepath)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) &
            (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df.index, df['value'], color = 'r')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
  
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = pd.DatetimeIndex(df_bar.index).year
    df_bar['month'] = pd.DatetimeIndex(df_bar.index).month
    df_bar = df_bar.groupby(['year', 'month']).mean().reset_index()
    df_bar = df_bar.pivot(index='year', columns='month', values='value')
    df_bar.columns = ['January', 
                      'February', 
                      'March', 
                      'April', 
                      'May', 
                      'June', 
                      'July', 
                      'August', 
                      'September', 
                      'October', 
                      'November', 
                      'December']

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(16, 8))
    ax = df_bar.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=['January', 
                                      'February', 
                                      'March', 
                                      'April', 
                                      'May', 
                                      'June', 
                                      'July', 
                                      'August', 
                                      'September', 
                                      'October', 
                                      'November', 
                                      'December'])
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    month_order = ['Jan',
                   'Feb',
                   'Mar',
                   'Apr',
                   'May', 
                   'Jun', 
                   'Jul', 
                   'Aug', 
                   'Sep', 
                   'Oct', 
                   'Nov', 
                   'Dec']
  
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
  
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], order=month_order)
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

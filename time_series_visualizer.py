import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

meses = [
    'January',
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
    'December'
]

mesitos = [
    'Jan',
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
    'Dec'
]

# Tips for passing unit tests:
#
# 1.  Make a copy of the cleaned data in df for test_data_cleaning.
# 2.  When using Seaborn, define fig = graph.fig and activate the
#     legend (see below).
# 3.  Pass a months list to sns via parameter hue_order or order to
#     get the legend in the correct order.  Otherwise, it will start with
#     'May' since the data starts with 'May.'

# Read the CSV data, attempt to parse the dates, and set
# the index to the date column for the original data frame.
dfo = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])
dfo.set_index('date')

# Remove the outlying 2.5% on each end for the cleaned data frame.
dfc = dfo.copy()
dfc = dfc.loc[(dfc['value'] >= dfc['value'].quantile(0.025))
              & (dfc['value'] <= dfc['value'].quantile(0.975))]

df = dfc.copy()


def draw_line_plot():
    # Draw a matplotlib line plot.
    fig = plt.figure()
    ax = plt.axes(
        xlabel='Date',
        ylabel='Page Views',
        title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019'
    )
    ax.plot_date(dfc['date'], dfc['value'], linestyle='-', marker=',')

    # Save image.
    fig.savefig('line_plot.png')

    # Return the figure for testing.
    return fig


def draw_bar_plot():
    # Massage data for monthly bar plot.
    #
    # x-axis:  Years
    # y-axis:  Average Page Views
    # legend:  months/colors
    #
    # Four groups of bars, one for each year 2016-2019.
    # One bar for each month.
    # Each bar displays the average page views per day for
    # the month.
    #
    # Data should look something like:
    #
    # year  month  avg
    # 2016  1      1.07
    # 2016  2      1.08
    #
    # Should be able to plot with a grouped bar chart with the data.

    df1 = dfc.copy()
    df1['year'] = df1['date'].dt.year
    df1['month'] = df1['date'].dt.month
    df1['month_long'] = df1['date'].dt.month_name()
    df1 = df1.groupby([df1['year'], df1['month'], df1['month_long']]).mean()
    df1 = df1.round({'value': 0})
    df1 = df1.reset_index()

    # Draw bar plot.
    #
    # Use either matplotlib directly, built-in pandas plotting, or
    # seaborn as long as the fig and axes are set for testing.

    # Use sns.catplot().
    graph = sns.catplot(
        data=df1,
        kind="bar",
        x="year",
        y="value",
        hue='month_long',
        hue_order=meses
    )
    graph.despine(left=True)
    graph.set_axis_labels('Years', 'Average Page Views')
    graph._legend.remove()

    # Define fig for return and testing.
    fig = graph.fig
    # Call legend to make the legend active for testing.
    fig.axes[0].legend()

    # Save image.
    fig.savefig('bar_plot.png')

    # Return the figure for testing.
    return fig


def draw_box_plot():
    # Goal is to draw two box and whisker plots, one showing page view
    # trends over years and the other showing page views per month.
    #
    # Two separate plots will have to be drawn on the same figure.
    #
    # The first plot will need 'years' for the x-axis and 'value' for
    # the y-axis and sns.boxplot() will construct the box and whisker
    # plot for each year from the data.
    #
    # The second plot will need 'month_short' for the x-axis and
    # 'value' for the y-axis and sns.boxplot() will construct the box
    # and whisker for each month from the data.

    df2 = dfc.copy()
    df2.reset_index(inplace=True)
    df2['year'] = df2['date'].dt.year
    df2['month'] = df2['date'].dt.month
    df2['month_long'] = df2['date'].dt.month_name
    # Must be a better way, similar to the other dt methods.
    # Mapping with integer to abbreviation dict.
    df2['month_short'] = [d.strftime('%b') for d in df2.date]

    # Create a matplotlib figure and two axes.
    # plt.subplots() returns a figure and two axes.
    fig, (ax1, ax2) = plt.subplots(figsize=(12, 6), ncols=2, sharey=False)

    # sns.boxplot() returns a matplotlib axes object.
    # We need to assign it to edit the labels.
    # ax1 = sns.boxplot(data=df2, x="year", y="value", ax=ax1)
    ax1 = sns.boxplot(
        data=df2,
        x="year",
        y="value",
        ax=ax1
    )
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax2 = sns.boxplot(
        data=df2,
        x="month_short",
        y="value",
        order=mesitos,
        ax=ax2
    )
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image.
    fig.savefig('box_plot.png')

    # Return the figure for testing.
    return fig

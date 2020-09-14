import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import db


def plot_history():

    # TODO: Eventually this should plot only the last ~2 weeks of data

    """
    Simple functions which gets all data for all products and plots using seaborn package
    :return:
    """

    # Get data from mongodb and creates dataframe
    df = pd.DataFrame.from_records(db.get_all_product_details())
    # Gets details from each product and concats to one list
    data_list = [item for sublist in df.details for item in sublist]
    # Shortens the list to 30 chars to make graph legend neater
    for i in data_list:
        i['title'] = i['title'][0:30]
    data = pd.DataFrame(data_list)
    # Set theme for plot
    sns.set_theme(style="darkgrid")
    # Create chart using seaborn
    chart = sns.relplot(x='date', y='price', hue='title', data=data, kind='line', height=5)
    # Formt x-axis lables and rotate them so they can be easily read
    chart.fig.autofmt_xdate()
    chart.set_xticklabels(fontsize=6)
    chart.ax.margins(.02)
    for label in chart.ax.get_xticklabels():
        label.set_rotation(45)
    plt.show()


if __name__ == "__main__":

    plot_history()

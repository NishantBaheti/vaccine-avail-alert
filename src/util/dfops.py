import pandas as pd
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)


def df_to_table_image(df: pd.DataFrame, file_name: str=None) -> None:
    """convert dataframe to table image and save

    Args:
        df (pd.DataFrame): dataframe containing data
        file_name (str): file name to be saved
    """
    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(1, 1)
    data = df.values
    columns = df.columns
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=data, colLabels=columns, loc='center')
    # the_table.auto_set_font_size(False)
    the_table.set_fontsize(20)
    # the_table.scale(2, 2)
    if file_name is None:
        return the_table
    else:
        plt.savefig(file_name)


def df_to_html(df: pd.DataFrame) -> str:
    """covert pandas dataframe to html

    Args:
        df (pd.DataFrame): pandas dataframe

    Returns:
        str: html string
    """

    return df.to_html()

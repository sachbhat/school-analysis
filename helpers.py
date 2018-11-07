import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_dataset(year=2018):
    """
    Load OSPI data set of assemesment performance of Washington state public schools.

    Currently supports 2016, 2017, and 2018.

    Parameters
    ----------
    year : int
        Year

    Returns
    -------
    pandas.dataframe
        Preloaded dataframe based on CSV downloaded from reportcard.ospi.k12.wa.us
    """

    url_map = {2018: 'http://reportcard.ospi.k12.wa.us/Reports/2018/2_03_AIM-WCAS-SBA%20Assessments%20School%20(with%20suppression%20-%20new%20format).txt',
        2017: 'http://reportcard.ospi.k12.wa.us/Reports/2017/2_03_AIM-EOC-MSP-SBA%20Assessments%20School%20(with%20suppression%20-%20new%20format).txt',
        2016: 'http://reportcard.ospi.k12.wa.us/Reports/2016/2_03_AIM-EOC-MSP-SBA%20Assessments%20School%20(with%20suppression%20-%20new%20format).txt'}

    if year in url_map:
        return pd.read_csv(url_map[year], sep='\t')
    else:
        return None

# Take in a integer and slice data feed by that grade. If we have no information, return None.
def filter_by_grade(df, grade=None):
    """
    Filter OSPI data by grade

    Supports 3-11

    Parameters
    ----------
    df : pandas.dataframe
        Input dataframe

    grade : int
        grade level (3-11)

    Returns
    -------
    pandas.dataframe
        Preloaded dataframe filtered by grade
    """

    grade_map = {5: '5th', 4: '4th', 3: '3rd', 8: '8th', 6: '6th', 7: '7th', 10: '10th', 11: '11th'}

    if grade in grade_map:
        return df[df['GradeLevel']==grade_map[grade]]
    else:
        return df[df['GradeLevel']==0]

# Take in 'math' or 'english' and filter out data that matches
def filter_by_subject(df, subject=None):
    """
    Filter OSPI data by subject

    Supports 2 different math tests, english

    Parameters
    ----------
    df : pandas.dataframe
        Input dataframe

    subject : string
        'math', 'math1', 'english'

    Returns
    -------
    pandas.dataframe
        Preloaded dataframe filtered by subject
    """

    subject_map = {'math': 'MATH', 'math1':'Math', 'english': 'ELA'}

    if subject in subject_map:
        return df[df['Subject']==subject_map[subject]]
    else:
        return df[df['Subject']==0]

def get_value_by_grade_subject_student_group(df, grade, subject, group, value):
    """
    Get single value of OSPI data by subject, grade, student group

    Supports 2 different math tests, english, grades 3-11, and any student group represented in underlying load_dataset

    Parameters
    ----------
    df : pandas.dataframe
        Input dataframe

    grade : int
        grade level (3-11)

    subject : string
        'math', 'math1', 'english'

    student_group : string
        demographic group (e.g. "All", "Low Income")

    value : string
        numeric value data should return

    Returns
    -------
    pandas.dataframe
        Preloaded dataframe 3 clolumns district, school, and value
    """

    df_ = filter_by_grade(df, grade)
    df_ = filter_by_subject(df_, subject)
    df_ = df_.loc[(df_["StudentGroup"]==group)]
    df_ = df_.loc[:, ['District', 'School', value]]
    return df_

# create pivot table of school x studentGroup with given values
def pivot_by_grade_subject_student_group(df, grade, subject, groups, values):
    """
    Create pivot table of school x student group with given values

    Supports 2 different math tests, english, grades 3-11, and any student group represented in underlying load_dataset

    Parameters
    ----------
    df : pandas.dataframe
        Input dataframe

    grade : int
        grade level (3-11)

    subject : string
        'math', 'math1', 'english'

    groups : array of strings
        demographic group (e.g. ["All", "Low Income"])

    values : array of string
        numeric value datas should return

    Returns
    -------
    pandas.dataframe
        Preloaded dataframe 3 clolumns district, school, and value
    """
    # filter by grade
    df = filter_by_grade(df, grade)

    # filter by subject
    df = filter_by_subject(df, subject)

    # filter by test administration
    df = df[df['testAdministration']=='SBA']

    # filter by student group
    df = df[df['StudentGroup'].isin(groups)]

    # make compound key to avoid duplicate school names
    df["DistrictSchool"] = df.apply(lambda row: "{}:{}".format(row.District, row.School), axis=1)

    #display(df.head())
    # grab the values we care about in pivoted form
    df_pivot = df.pivot(index = "DistrictSchool", columns="StudentGroup", values=values)

    #display(df_pivot.head())

    return df_pivot[:]


def build_visualization(df, x0, y0):
    """
    Quick joinplot of two variable columns.

    Parameters
    ----------
    df : pandas.dataframe
        Input dataframe

    x0 : string
        label for x-axis

    y0 : string
        label for y-axis

    Returns
    -------
    nil
    """

    plt.figure(figsize=(10,10))
    sns.set_style('darkgrid')

    ax = sns.jointplot(x=x0, y=y0, data=df, size=10, xlim=(0,100), ylim=(0,100))
    ax = ax.plot(sns.regplot, sns.distplot)

    # draw equality line
    ax.ax_joint.plot((0,100),(0,100), ':k')


def compare_groups(data, grade, subject, groups, values):
    """
    Quick visualization of scores across two different groups

    Supports 2 different math tests, english, grades 3-11, and any student group represented in underlying load_dataset

    Parameters
    ----------
    df : pandas.dataframe
        Input dataframe

    grade : int
        grade level (3-11)

    subject : string
        'math', 'math1', 'english'

    groups : string
        demographic group (e.g. "All", "Low Income")

    values : array of string (should be 2)
        numeric value datas should return

    Returns
    -------
    pandas.dataframe
        Preloaded dataframe 2 columns x, y
    """

    df = pivot_by_grade_subject_student_group(data, grade, subject, groups, values)

    # add column names
    df.columns = df.columns.levels[1]

    # clean out empty
    df = df.dropna()

    build_visualization(df, df.columns[1], df.columns[0])

    return df

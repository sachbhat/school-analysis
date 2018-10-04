import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_dataset(year=2018):
    url_map = {2018: 'http://reportcard.ospi.k12.wa.us/Reports/2018/2_03_AIM-WCAS-SBA%20Assessments%20School%20(with%20suppression%20-%20new%20format).txt',
        2017: 'http://reportcard.ospi.k12.wa.us/Reports/2017/2_03_AIM-EOC-MSP-SBA%20Assessments%20School%20(with%20suppression%20-%20new%20format).txt',
        2016: 'http://reportcard.ospi.k12.wa.us/Reports/2016/2_03_AIM-EOC-MSP-SBA%20Assessments%20School%20(with%20suppression%20-%20new%20format).txt'}

    if year in url_map:
        return pd.read_csv(url_map[year], sep='\t')
    else:
        return None

# Take in a integer and slice data feed by that grade. If we have no information, return None.
def filter_by_grade(df, grade=None):

    grade_map = {5: '5th', 4: '4th', 3: '3rd', 8: '8th', 6: '6th', 7: '7th', 10: '10th', 11: '11th'}

    if grade in grade_map:
        return df[df['GradeLevel']==grade_map[grade]]
    else:
        return df[df['GradeLevel']==0]

# Take in 'math' or 'english' and filter out data that matches
def filter_by_subject(df, subject=None):
    subject_map = {'math': 'MATH', 'math1':'Math', 'english': 'ELA'}

    if subject in subject_map:
        return df[df['Subject']==subject_map[subject]]
    else:
        return df[df['Subject']==0]

def filter_by_grade_subject_student_group(df, grade, subject, group, value):
    df_ = filter_by_grade(df, grade)
    df_ = filter_by_subject(df_, subject)
    df_ = df_.loc[(df_["StudentGroup"]==group)]
    df_ = df_.loc[:, ['District', 'School', value]]
    return df_    

# create pivot table of school x studentGroup with given values
def pivot_by_grade_subject_student_group(df, grade, subject, groups, values):

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
    plt.figure(figsize=(10,10))
    sns.set_style('darkgrid')

    ax = sns.jointplot(x=x0, y=y0, data=df, size=10, xlim=(0,100), ylim=(0,100))
    ax = ax.plot(sns.regplot, sns.distplot)

    # draw equality line
    ax.ax_joint.plot((0,100),(0,100), ':k')


def compare_groups(data, grade, subject, groups, values):

    df = pivot_by_grade_subject_student_group(data, grade, subject, groups, values)

    # add column names
    df.columns = df.columns.levels[1]

    # clean out empty
    df = df.dropna()

    build_visualization(df, df.columns[1], df.columns[0])

    return df

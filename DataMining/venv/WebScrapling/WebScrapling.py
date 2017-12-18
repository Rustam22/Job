from datetime import datetime

from lxml import html
import requests

import numpy as np
import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt
from IPython.display import display, HTML
import plotly.plotly as py

pd.options.display.max_columns = 50

thefile = open('WebScrapingContent.txt', 'w')

"""
x = np.arange(10)
print x
print x[1:]
print x[1:7]
print x[1:7:2]
print x[:]
print x[:-7]
print x[::1]
print "\n"

y = np.arange(10)
print y
y.shape = (2, 5)
print y
print y[-1, 2]
print "\n"



z = np.arange(35).reshape(5, 7)
print z
print z[1:5:2, ::3]
"""


def print_element(element):
    print("<%s %s>%s ..." % (element.tag, element.attrib, element.text_content()[:200].replace("\n", " ")))


page = requests.get('http://en.wikipedia.org/wiki/List_of_Nobel_laureates')
tree = html.fromstring(page.text)
print_element(tree)
print("\n")


tables = tree.xpath('//table')
for table in tables:
    print_element(table)
print("\n")


table = tree.xpath('//table[@class="wikitable sortable"]')[0]
print_element(table)
print("\n")


subjects = [subject[0].text_content().replace("\n", " ") for subject in table.xpath('tr')[0][1:]]
pprint(subjects)
thefile.write("1) Subjects: %s\n" % subjects)
print("\n")


years = [item[0].text for item in table.xpath('tr')[1:-1]]
print(years)
thefile.write("2) Years: %s\n\n" % years)
print("\n")


for i in range(len((table.xpath('tr')[:][1:]))):
    for index, item in enumerate(table.xpath('tr')[i][1:]):
        subject = subjects[index]
        #print "%s: " % subject
        for winner in item.xpath('span[@class="vcard"]/span/a'):
            winner_name = winner.attrib["title"]
            winner_url = winner.attrib["href"]
            #print " - %s" % winner_name
print("\n\n")


year_list = []
subject_list = []
name_list = []
url_list = []
thefile.write("3) Whole content \n")
for y_index, year in enumerate(years):
    #print year
    thefile.write("  %s) Year: %s\n" % (y_index+1, year))

    for index, item in enumerate(table.xpath('tr')[y_index + 1][1:]):
        subject = subjects[index]
        #print "%s:" % subject
        thefile.write("      a.b) Subject: %s\n" % subject)

        for winner in item.xpath('span[@class="vcard"]/span/a'):
            winner_name = winner.attrib["title"]
            winner_url = winner.attrib["href"]
            #print " - %s" % winner_name
            thefile.write("           a.c) Winner name: %s\n" % winner_name.encode('utf-8'))
            year_list.append(year)
            subject_list.append(subject)
            name_list.append(winner_name)
            url_list.append(winner_url)

    thefile.write("\n")
print("\n\n\n")



data_set = pd.DataFrame(name_list, columns=["winner_name"])
data_set["subject"] = subject_list
data_set["year"] = year_list
data_set["year"] = data_set["year"].astype(np.int32)
#data_set["url"] = url_list
data_set.head(5)
display(data_set)
print("\n\n")


years_df = data_set["year"].value_counts().sort_index()
print(years_df)




plt.figure(figsize=(15,2))
plt.plot(years_df.index, years_df.values, )
plt.grid()
plt.xlabel("Year")
plt.ylabel("Number of prizes")
plt.show()
print("Total prizes: %s\n\n" % len(data_set))



print(years_df.value_counts())
print(years_df.value_counts().index)
plt.bar(years_df.value_counts().index, years_df.value_counts())
plt.box(on="off")
plt.grid()
plt.xlabel("Number of Nobel Prizes/Year")
plt.ylabel("")
plt.show()
print("\n\n")



plt.figure(figsize=(13, 5))
for subject in subjects:
    df = data_set[data_set["subject"] == subject]["year"].value_counts().sort_index().cumsum()
    plt.plot(df.index, df, label=subject, linewidth=2, alpha=.6)

plt.grid()
plt.legend(loc="best")
plt.xlabel("Year")
plt.ylabel("Cumulative Sum of Given Nobel Prizes")
plt.xticks(np.arange(1900, 2020, 10))
plt.show()




plt.figure(figsize=(13,5))
for subject in subjects:
    df = data_set[(data_set["subject"]==subject) &
                  (data_set["year"].astype(np.int32)<1950)]["year"].value_counts().sort_index().cumsum()
    plt.plot(df.index, df, label=subject, linewidth=2, alpha=.6)

plt.grid()
plt.legend(loc="best")
plt.xlabel("Year")
plt.ylabel("Cumulative Sum of Given Nobel Prizes")
plt.xticks(np.arange(1900, 1950, 5))

gca = plt.gca()
gca.add_patch(plt.Rectangle((1914,0), 4, 60, alpha=.3, color="orange"))
gca.add_patch(plt.Rectangle((1939,0), (45-39), 60, alpha=.3, color="orange"))
plt.annotate(s="WW I", xy=(1915,55))
plt.annotate(s="WW II", xy=(1941,55))
plt.show()


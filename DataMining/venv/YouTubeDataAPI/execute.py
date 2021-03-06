from __future__ import division
from datetime import datetime
import requests
from lxml import html, etree
import json
from textblob import TextBlob

import pandas as pd
import numpy as np
from pprint import pprint

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


api_key = "AIzaSyBwQ6N1_r5r2UyT2LtQJgQbHtFjrtZl7w8"


pd.options.display.max_columns = 100
pd.options.display.max_rows = 35
pd.options.display.width = 120



#----------------Searching YouTube Using youtube.search.list---------------#
parameters = {
                "part": "snippet",
                "maxResults": 5,
                "order": "date",
                "pageToken": "",
                "publishedAfter": "2008-08-04T00:00:00Z",
                "publishedBefore": "2008-11-04T00:00:00Z",
                "q": "",
                "key": api_key,
                "type": "video",
              }

url = "https://www.googleapis.com/youtube/v3/search"
parameters['q'] = "Mark Udall"
page = requests.request(method="get", url=url, params=parameters)
j_results = json.loads(page.text)

print(page.text)
print("\n\n\n")




#----------------YouTube Video Meta Data Using youtube.video.list---------------#
parameters = {"part": "statistics",
              "id": "WSKi8HfcxEk",
              "key": api_key,
              }
url = "https://www.googleapis.com/youtube/v3/videos"

page = requests.request(method="get", url=url, params=parameters)
j_results = json.loads(page.text)
print(page.text)
print("\n\n\n")

plt.show()




#----------------Process Data Range---------------#
#            I'll check the coorelation between the results of 2008 Senate elections results and YouTube Stats.
#                         Colorado Senate - Gardner vs. Udall Cory Gardner (R) Mark Udall (D)

def _search_list(q="", publishedAfter=None, publishedBefore=None, pageToken=""):
    parameters = {"part": "id",
                  "maxResults": 50,
                  "order": "viewCount",
                  "pageToken": pageToken,
                  "q": q,
                  "type": "video",
                  "key": api_key,
                  }
    url = "https://www.googleapis.com/youtube/v3/search"

    if publishedAfter: parameters["publishedAfter"] = publishedAfter
    if publishedBefore: parameters["publishedBefore"] = publishedBefore

    page = requests.request(method="get", url=url, params=parameters)
    return json.loads(page.text)


def search_list(q="", publishedAfter=None, publishedBefore=None, max_requests=10):
    more_results = True
    pageToken = ""
    results = []

    for counter in range(max_requests):
        j_results = _search_list(q=q, publishedAfter=publishedAfter, publishedBefore=publishedBefore,
                                 pageToken=pageToken)
        items = j_results.get("items", None)
        if items:
            results += [item["id"]["videoId"] for item in j_results["items"]]
            if j_results.has_key("nextPageToken"):
                pageToken = j_results["nextPageToken"]
            else:
                return results
        else:
            return results
    return results


def _video_list(video_id_list):
    parameters = {"part": "statistics",
                  "id": ",".join(video_id_list),
                  "key": api_key,
                  "maxResults": 50
                  }
    url = "https://www.googleapis.com/youtube/v3/videos"
    page = requests.request(method="get", url=url, params=parameters)
    j_results = json.loads(page.text)
    df = pd.DataFrame([item["statistics"] for item in j_results["items"]], dtype=np.int64)
    df["video_id"] = [item["id"] for item in j_results["items"]]

    parameters["part"] = "snippet"
    page = requests.request(method="get", url=url, params=parameters)
    j_results = json.loads(page.text)
    df["publishedAt"] = [item["snippet"]["publishedAt"] for item in j_results["items"]]
    df["publishedAt"] = df["publishedAt"].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z"))
    df["date"] = df["publishedAt"].apply(lambda x: x.date())
    df["week"] = df["date"].apply(lambda x: x.isocalendar()[1])
    df["channelId"] = [item["snippet"]["channelId"] for item in j_results["items"]]
    df["title"] = [item["snippet"]["title"] for item in j_results["items"]]
    df["description"] = [item["snippet"]["description"] for item in j_results["items"]]
    df["channelTitle"] = [item["snippet"]["channelTitle"] for item in j_results["items"]]
    df["categoryId"] = [item["snippet"]["categoryId"] for item in j_results["items"]]
    return df


def video_list(video_id_list):
    values = []
    for index, item in enumerate(video_id_list[::50]):
        t_index = index * 50
        values.append(_video_list(video_id_list[t_index:t_index + 50]))
    return pd.concat(values)


#-----------------------Get Data for Two Candidates-------------------------#
def get_data(candidates, publishedAfter, publishedBefore):
    results_list = []
    for q in candidates:
        results = search_list(q=q,
                              publishedAfter=publishedAfter,
                              publishedBefore=publishedBefore,
                              max_requests=50)

        stat_data_set = video_list(results)
        stat_data_set["candidate_name"] = q
        results_list.append(stat_data_set)
    data_set = pd.concat(results_list)
    return data_set

def get_2008_data(candidates):
    return get_data(candidates, publishedAfter="2008-08-04T00:00:00Z", publishedBefore="2008-11-04T00:00:00Z")

def get_2010_data(candidates):
    return get_data(candidates, publishedAfter="2010-08-04T00:00:00Z", publishedBefore="2010-11-04T00:00:00Z")

def get_2012_data(candidates):
    return get_data(candidates, publishedAfter="2012-08-04T00:00:00Z", publishedBefore="2012-11-04T00:00:00Z")

def get_2014_data(candidates):
    return get_data(candidates, publishedAfter="2014-08-04T00:00:00Z", publishedBefore="2014-11-04T00:00:00Z")




#-----------------------Analyzing Colorado Senate Race for 2014-------------------------#
candidates = ["Cory Gardner", "Mark Udall"] # Cory Gardner (R), Mark Udall (D)*
colorado_2014_ds = get_2014_data(candidates)
tpr = pd.pivot_table(colorado_2014_ds, values=["commentCount", "favoriteCount", "dislikeCount", "likeCount", "viewCount"], aggfunc='sum', index="candidate_name")

print(tpr, "\n\n")



for candidate, color in zip(candidates, ["r", "b"]):
    cand = colorado_2014_ds[colorado_2014_ds["candidate_name"]==candidate]
    by_date = cand["week"].value_counts()
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos Published")
plt.xlabel("Week")
plt.show()



for candidate, color in zip(candidates, ["r", "b"]):
    cand = colorado_2014_ds[colorado_2014_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["viewCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos viewCount")
plt.xlabel("Week")
plt.show()


for candidate, color in zip(candidates, ["r", "b"]):
    cand = colorado_2014_ds[colorado_2014_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["likeCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos likeCount")
plt.xlabel("Week")
plt.show()


for candidate, color in zip(candidates, ["r", "b"]):
    cand = colorado_2014_ds[colorado_2014_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["dislikeCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos dislikeCount")
plt.xlabel("Week")
plt.show()







#-----------------------How Predective Was It in 2012?-------------------------#
#-----------------------Virginia Senate - Allen vs. Kaine-------------------------#
candidates = ["George Allen", "Tim Kaine"] # George Allen (R), Tim Kaine (D)Winner
va_2012_ds = get_2012_data(candidates)
pd.pivot_table(va_2012_ds, values=["commentCount", "favoriteCount", "dislikeCount", "likeCount", "viewCount"],
               aggfunc='sum', index="candidate_name")


for candidate, color in zip(candidates, ["r", "b"]):
    cand = va_2012_ds[va_2012_ds["candidate_name"]==candidate]
    by_date = cand["week"].value_counts()
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos Published")
plt.xlabel("Week")
plt.show()


for candidate, color in zip(candidates, ["r", "b"]):
    cand = va_2012_ds[va_2012_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["viewCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos viewCount")
plt.xlabel("Week")
plt.show()


for candidate, color in zip(candidates, ["r", "b"]):
    cand = va_2012_ds[va_2012_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["likeCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos likeCount")
plt.xlabel("Week")
plt.show()


for candidate, color in zip(candidates, ["r", "b"]):
    cand = va_2012_ds[va_2012_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["dislikeCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos dislikeCount")
plt.xlabel("Week")
plt.show()







#-----------------------Nevada Senate - Heller vs. Berkley-------------------------#
candidates = ["Dean Heller", "Shelley Berkley"] # Dean Heller (R)*Winnner, Shelley Berkley (D)
nv_2012_ds = get_2012_data(candidates)
print(pd.pivot_table(nv_2012_ds, values=["commentCount", "favoriteCount", "dislikeCount", "likeCount", "viewCount"], aggfunc='sum', index="candidate_name"))

for candidate, color in zip(candidates, ["r", "b"]):
    cand = nv_2012_ds[nv_2012_ds["candidate_name"]==candidate]
    by_date = cand["week"].value_counts()
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos Published")
plt.xlabel("Week")
plt.show()

for candidate, color in zip(candidates, ["r", "b"]):
    cand = nv_2012_ds[nv_2012_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["viewCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos viewCount")
plt.xlabel("Week")
plt.show()

for candidate, color in zip(candidates, ["r", "b"]):
    cand = nv_2012_ds[nv_2012_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["likeCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos likeCount")
plt.xlabel("Week")
plt.show()

for candidate, color in zip(candidates, ["r", "b"]):
    cand = nv_2012_ds[nv_2012_ds["candidate_name"]==candidate]
    by_date = pd.pivot_table(cand, index=["week"], values=["dislikeCount"], aggfunc="sum")
    by_date = by_date.sort_index()
    dates = by_date.index
    plt.plot(dates, by_date.values, "-o", label=candidate, c=color, linewidth=2)
plt.legend(loc="best")
plt.ylabel("Videos dislikeCount")
plt.xlabel("Week")
plt.show()










url = "http://www.senate.gov/general/contact_information/senators_cfm.xml"
response = requests.get(url)
tree = etree.fromstring(str(response.text))
print(tree, "\n\n")

member_full = [member.xpath("member_full")[0].text for member in tree.xpath("//member")]
senators = pd.DataFrame(member_full, columns=["member_full"])

senators["member_full"] = member_full
senators["last_name"] = [member.xpath("last_name")[0].text for member in tree.xpath("//member")]
senators["first_name"] = [member.xpath("first_name")[0].text for member in tree.xpath("//member")]
senators["party"] = [member.xpath("party")[0].text for member in tree.xpath("//member")]
senators["state"] = [member.xpath("state")[0].text for member in tree.xpath("//member")]
senators["address"] = [member.xpath("address")[0].text for member in tree.xpath("//member")]
senators["phone"] = [member.xpath("phone")[0].text for member in tree.xpath("//member")]
senators["website"] = [member.xpath("website")[0].text for member in tree.xpath("//member")]
senators["bioguide_id"] = [member.xpath("bioguide_id")[0].text for member in tree.xpath("//member")]
senators["class"] = [member.xpath("class")[0].text for member in tree.xpath("//member")]

print(senators, "\n\n")


by_party = senators["party"].value_counts()
by_party.sort(ascending=False)
print(by_party)

color_dict = {"D": "b",
              "R": "r",
              "I": "g"}


labels = ["%s: %s" % (by_party.index[index], value) for index, value in enumerate(by_party)]
colors = list(pd.Series(by_party.index).map(color_dict))

plt.figure()
plt.axis("equal")
plt.pie(by_party.values, labels=labels, colors=colors, shadow=True, explode=np.zeros(len(by_party)) + 0.04)
plt.show()


fig = plt.figure()
axes = fig.add_subplot(111)
axes.barh(range(len(by_party.index)), by_party.values, color=colors)
plt.box(on="off")
axes.axvline(x=50, color="black", alpha=0.7, linewidth=2)
axes.yaxis.set_ticks([item + 0.4 for item in range(len(by_party.index))])
axes.yaxis.set_ticklabels(by_party.index, minor=False)
plt.xlabel("$113^{th}$ Senate Seats Controlled by Party")
plt.show()



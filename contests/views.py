from datetime import datetime,timedelta
from time import time
from django.shortcuts import render, redirect
import requests


# sets the contest view
def contest_view(request):
     response = requests.get("https://codeforces.com/api/contest.list?gym=false");
     data = response.json()
     result = data['result']
     cf_contest = [d for d in result if d['phase'] == 'BEFORE']
     cf_contest.sort(key= lambda x : x['startTimeSeconds'])
     for d in cf_contest:
          d['startTimeSeconds'] = datetime(1970, 1, 1) + timedelta(milliseconds=d['startTimeSeconds']*1000)
          d['duration'] = d['durationSeconds'] /60.0/60.0
          d['link'] = "https://codeforces.com/contests/"+str(d['id'])
     #print(cf_contest)

     # atcoder part
     response = requests.get("https://kenkoooo.com/atcoder/resources/contests.json")
     result = response.json()
     currentTimeinSeconds = time() 
     print(currentTimeinSeconds)
     atcoder_contests = [d for d in result if d['start_epoch_second'] >  currentTimeinSeconds]
     print(atcoder_contests)
     #result = data['result']
     context={}
     
     context['cf_contest'] = cf_contest
     return render(request, 'contests/contests.html',context)
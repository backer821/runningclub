#!/usr/bin/python
###########################################################################################
# summarizemembers -- generate member summary
#
#       Date            Author          Reason
#       ----            ------          ------
#       09/26/15        Lou King        Create
#
#   Copyright 2015 Lou King
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###########################################################################################

# standard
import pdb
import argparse
import csv
from datetime import datetime, timedelta
from calendar import monthrange
from collections import OrderedDict
import time
import json
import types

# pypi

# other

# home grown
from running.runningaheadmembers import RunningAheadMembers
from running.ra2membersfile import ra2members
from analyzemembership import analyzemembership
from running.ra2membersfile import ra2members
from loutilities import timeu
ymd = timeu.asctime('%Y-%m-%d')
mdy = timeu.asctime('%m/%d/%Y')
md = timeu.asctime('%m-%d')
from loutilities.csvwt import wlist
from loutilities import apikey

import version

class invalidParameter(): pass

#----------------------------------------------------------------------
def membercount2json(ordyears,fname=None): 
#----------------------------------------------------------------------
    '''
    convert members added per day (ordyears) to membercount per day in json format
    
    :param ordyears: return value from analyzemembership
    :param fname: optional output file
    :rtype: json conversion from ordyears
    '''

    # convert ordyears into something which can be read with json
    membercount = OrderedDict()
    for year in ordyears:
        accumulated = 0
        thisdate = datetime(year,1,1)   # jan 1, current year
        oneday = timedelta(1)
        syear = str(year)
        membercount[syear] = []
        for dd in ordyears[year]:
            # fill in days between last thisdate and dd so all dates are covered
            while thisdate < dd:
                sdate = md.dt2asc(thisdate)
                membercount[syear].append({'date':sdate,'nummembers':accumulated})
                thisdate += oneday

            # pick up new members and save
            accumulated += ordyears[year][dd]
            sdate = md.dt2asc(dd)
            membercount[syear].append({'date':sdate,'nummembers':accumulated})
            thisdate = dd+oneday

    membercountjson = json.dumps(membercount, indent=4, separators=(',', ': '))

    if fname:
        with open(fname,'w') as outfile:
            outfile.write(membercountjson)

    return membercountjson

#----------------------------------------------------------------------
def members2file(memberfileh, mapping, outfile=None, currentmembers=True): 
#----------------------------------------------------------------------
    '''
    convert members added per day (ordyears) to membercount per day in json format
    
    :param memberfileh: membership file handle, individual records
    :param mapping: OrderedDict {'outfield1':'infield1', 'outfield2':outfunction(memberrec), ...}
    :param outfile: optional output file
    :param currentmembers: True to generate list of current members only. default True
    :rtype: lines from output file
    '''

    # pull in memberfile
    members = RunningAheadMembers(memberfileh)
    
    # iterate through members
    thesemembers = members.member_iter()
    
    # analyze mapping for outfields
    outfields = []
    for outfield in mapping:
        invalue = mapping[outfield]

        if type(invalue) not in [str,unicode] and not callable(invalue):
            raise invalidParameter, 'invalid mapping {}. mapping values must be str or function'.format(outvalue)

        outfields.append(outfield)

    # maybe check for current members (local time)
    today = time.time()-time.timezone

    # create writeable list, csv file
    memberlist = wlist()
    cmemberlist = csv.DictWriter(memberlist, outfields)
    cmemberlist.writeheader()

    for thismember in thesemembers:
        # maybe only interested in current members
        if currentmembers:
            if ymd.asc2epoch(thismember.expiration) < today: continue

        outrow = {}
        for outfield in mapping:
            infield = mapping[outfield]
            if type(infield) == str:
                outvalue = getattr(thismember, infield, None)

            else:
                # a function call is requested
                outvalue = infield(thismember)

            outrow[outfield] = outvalue
        
        cmemberlist.writerow(outrow)

    # write file if desired
    if outfile:
        with open(outfile,'wb') as out:
            out.writelines(memberlist)

    return memberlist

#----------------------------------------------------------------------
def _getdivision(member):
#----------------------------------------------------------------------
    '''
    gets division as of Jan 1 from RunningAheadMember record

    :param member: RunningAheadMember record
    :rtype: division text
    '''

    # use local time
    today = time.time()-time.timezone
    todaydt = timeu.epoch2dt(today)
    jan1 = datetime(todaydt.year, 1, 1)

    memberage = timeu.age(jan1, ymd.asc2dt(member.dob))

    # this must match grand prix configuration in membership database
    # TODO: add api to query this information from scoretility
    if memberage <= 13:
        div = '13 and under'
    elif memberage <= 29:
        div = '14-29'
    elif memberage <= 39:
        div = '30-39'
    elif memberage <= 49:
        div = '40-49'
    elif memberage <= 59:
        div = '50-59'
    elif memberage <= 69:
        div = '60-69'
    else:
        div = '70 and over'

    return div


#----------------------------------------------------------------------
def summarize(club, memberstatsfile, membersummaryfile, membershipfile=None):
#----------------------------------------------------------------------
    '''
    Summarize the membership stats and members for a given RunningAHEAD club.
    If membershipfile is not supplied, retrieve the member data from RunningAHEAD
    using the priviledged user token.

    :param club: club slug for RunningAHEAD
    :param membershipfile: filename, file handle, or list with member data (optional)
    '''

    if not membershipfile:
        ak = apikey.ApiKey('Lou King','running')
        try:
            raprivuser = ak.getkey('raprivuser')
        except apikey.unknownKey:
            raise parameterError, "'raprivuser' key needs to be configured using apikey"

        membershipfile = ra2members(club, raprivuser, exp_date='ge.1990-01-01', ind_rec=1)

    # analyze the memberships
    memberstats = analyzemembership(membershipfile)

    # generate json file with membership statistics
    membercount2json(memberstats, memberstatsfile)

    # generate members csv file with member information
    mapping = OrderedDict()
    mapping['First'] = 'fname'
    mapping['Last'] = 'lname'
    mapping['Div (age Jan 1)'] = _getdivision
    mapping['Hometown'] = lambda m: '{}, {}'.format(m.city, m.state)
    # for expiration date display convert yyyy-mm-dd to mm/dd/yyyy
    mapping['Expiration Date'] = lambda m: mdy.dt2asc(ymd.asc2dt(m.expiration))

    members2file(membershipfile, mapping, membersummaryfile)

    # for debugging
    return membershipfile


#----------------------------------------------------------------------
def main(): 
#----------------------------------------------------------------------
    '''
    summarize members
    '''
    parser = argparse.ArgumentParser(version='{0} {1}'.format('runningclub',version.__version__))
    parser.add_argument('club',help='club slug from RunningAHEAD')
    parser.add_argument('memberstatsfile',help='output file for membership stats (json)')
    parser.add_argument('membersummaryfile',help='output file for member summary (csv)')
    parser.add_argument('--membershipfile',help='optional membership file, individual records.  File headers match RunningAHEAD output',default=None)
    args = parser.parse_args()
    
    # summarize membership
    summarize(args.club, args.memberstatsfile, args.membersummaryfile, args.membershipfile)
    
# ##########################################################################################
#   __main__
# ##########################################################################################
if __name__ == "__main__":
    main()

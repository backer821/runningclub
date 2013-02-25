#!/usr/bin/python
###########################################################################################
# renderstandings - render result information within database for standings
#
#	Date		Author		Reason
#	----		------		------
#       02/14/13        Lou King        Create
#
#   Copyright 2013 Lou King
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
'''
renderstandings - render result information within database for standings
==============================================================================

'''

# standard
import pdb
import argparse

# pypi

# github

# other

# home grown
from runningclub import *
import version
import racedb


########################################################################
class BaseStandingsHandler():
########################################################################
    '''
    Base StandingsHandler class -- this is an empty class, to be used as a
    template for filehandler classes.  Each method must be replaced or enhanced.
    
    '''
    #----------------------------------------------------------------------
    def __init__(self,session):
    #----------------------------------------------------------------------
        self.session = session
    
    #----------------------------------------------------------------------
    def prepare(self,gen,seriesname,seriesid,year):
    #----------------------------------------------------------------------
        '''
        prepare output file for output, including as appropriate
        
        * open
        * print header information
        * collect format for output
        * collect print line dict for output
        
        numraces has number of races
        
        :param gen: gender M or F
        :param seriesname: name of series
        :param seriesid: series.id
        :param year: year of races
        :rtype: numraces
        '''

        pass
    
    #----------------------------------------------------------------------
    def clearline(self,gen):
    #----------------------------------------------------------------------
        '''
        prepare rendering line for output by clearing all entries

        :param gen: gender M or F
        '''

        pass
    
    #----------------------------------------------------------------------
    def setplace(self,gen,place):
    #----------------------------------------------------------------------
        '''
        put value in 'place' column for output (this should be rendered in 1st column)

        :param gen: gender M or F
        :param place: value for place column
        '''

        pass
    
    #----------------------------------------------------------------------
    def setname(self,gen,name):
    #----------------------------------------------------------------------
        '''
        put value in 'name' column for output (this should be rendered in 2nd column)

        :param gen: gender M or F
        :param name: value for name column
        '''

        pass
    
    #----------------------------------------------------------------------
    def setrace(self,gen,racenum,result):
    #----------------------------------------------------------------------
        '''
        put value in 'race{n}' column for output, for race n
        should be '' for empty race

        :param gen: gender M or F
        :param racenum: number of race
        :param result: value for race column
        '''

        pass
    
    #----------------------------------------------------------------------
    def settotal(self,gen,total):
    #----------------------------------------------------------------------
        '''
        put value in 'race{n}' column for output, for race n
        should be '' for empty race

        :param gen: gender M or F
        :param value: value for total column
        '''

        pass
    
    #----------------------------------------------------------------------
    def render(self,gen):
    #----------------------------------------------------------------------
        '''
        output current line to gender file

        :param gen: gender M or F
        '''

        pass

    #----------------------------------------------------------------------
    def skipline(self,gen):
    #----------------------------------------------------------------------
        '''
        output blank line to gender file

        :param gen: gender M or F
        '''

        pass
    
    #----------------------------------------------------------------------
    def close(self):
    #----------------------------------------------------------------------
        '''
        close files associated with this object
        '''
        
        pass
    
########################################################################
class ListStandingsHandler():
########################################################################
    '''
    Like BaseStandingsHandler class, but adds addhandler method.
    
    file handler operations are done for multiple files
    '''
    #----------------------------------------------------------------------
    def __init__(self):
    #----------------------------------------------------------------------
        self.fhlist = []
    
    #----------------------------------------------------------------------
    def addhandler(self,fh):
    #----------------------------------------------------------------------
        '''
        add derivative of BaseStandingsHandler to list of StandingsHandlers which
        will be processed
        
        :param fh: derivative of BaseStandingsHandler
        '''
        
        self.fhlist.append(fh)
        
    #----------------------------------------------------------------------
    def prepare(self,gen,seriesname,seriesid,year):
    #----------------------------------------------------------------------
        '''
        prepare output file for output, including as appropriate
        
        * open
        * print header information
        * collect format for output
        * collect print line dict for output
        
        numraces has number of races
        
        :param gen: gender M or F
        :param seriesname: name of series
        :param seriesid: series.id
        :param year: year of races
        :rtype: numraces
        '''
        
        numraces = None
        for fh in self.fhlist:
            numraces = fh.prepare(gen,seriesname,seriesid,year)
            
        # ok to use the last one
        return numraces
    
    #----------------------------------------------------------------------
    def clearline(self,gen):
    #----------------------------------------------------------------------
        '''
        prepare rendering line for output by clearing all entries

        :param gen: gender M or F
        '''

        for fh in self.fhlist:
            fh.clearline(gen)
    
    #----------------------------------------------------------------------
    def setplace(self,gen,place):
    #----------------------------------------------------------------------
        '''
        put value in 'place' column for output (this should be rendered in 1st column)

        :param gen: gender M or F
        :param place: value for place column
        '''

        for fh in self.fhlist:
            fh.setplace(gen,place)
    
    #----------------------------------------------------------------------
    def setname(self,gen,name):
    #----------------------------------------------------------------------
        '''
        put value in 'name' column for output (this should be rendered in 2nd column)

        :param gen: gender M or F
        :param name: value for name column
        '''

        for fh in self.fhlist:
            fh.setname(gen,name)
    
    #----------------------------------------------------------------------
    def setrace(self,gen,racenum,result):
    #----------------------------------------------------------------------
        '''
        put value in 'race{n}' column for output, for race n
        should be '' for empty race

        :param gen: gender M or F
        :param racenum: number of race
        :param result: value for race column
        '''

        for fh in self.fhlist:
            fh.setrace(gen,racenum,result)
    
    #----------------------------------------------------------------------
    def settotal(self,gen,total):
    #----------------------------------------------------------------------
        '''
        put value in 'race{n}' column for output, for race n
        should be '' for empty race

        :param gen: gender M or F
        :param value: value for total column
        '''

        for fh in self.fhlist:
            fh.settotal(gen,total)
    
    #----------------------------------------------------------------------
    def render(self,gen):
    #----------------------------------------------------------------------
        '''
        output current line to gender file

        :param gen: gender M or F
        '''

        for fh in self.fhlist:
            fh.render(gen)

    #----------------------------------------------------------------------
    def skipline(self,gen):
    #----------------------------------------------------------------------
        '''
        output blank line to gender file

        :param gen: gender M or F
        '''

        for fh in self.fhlist:
            fh.skipline(gen)
    
    #----------------------------------------------------------------------
    def close(self):
    #----------------------------------------------------------------------
        '''
        close files associated with this object
        '''
        
        for fh in self.fhlist:
            fh.close()
    
########################################################################
class TxtStandingsHandler(BaseStandingsHandler):
########################################################################
    '''
    StandingsHandler for .txt files
    
    :param session: database session
    '''
    #----------------------------------------------------------------------
    def __init__(self,session):
    #----------------------------------------------------------------------
        BaseStandingsHandler.__init__(self,session)
        self.TXT = {}
        self.pline = {'F':{},'M':{}}
    
    #----------------------------------------------------------------------
    def prepare(self,gen,seriesname,seriesid,year):
    #----------------------------------------------------------------------
        '''
        prepare output file for output, including as appropriate
        
        * open
        * print header information
        * collect format for output
        * collect print line dict for output
        
        numraces has number of races
        
        :param gen: gender M or F
        :param seriesname: name of series
        :param seriesid: series.id
        :param year: year of races
        :rtype: numraces
        '''
        
        # open output file
        MF = {'F':'Women','M':'Men'}
        rengen = MF[gen]
        self.TXT[gen] = open('{0}-{1}-{2}.txt'.format(year,seriesname,rengen),'w')
        
        # render list of all races which will be in the series
        self.TXT[gen].write("FSRC {0}'s {1} {2} standings\n".format(rengen,year,seriesname))
        self.TXT[gen].write('\n')                
        numraces = 0
        self.racelist = []
        for race in self.session.query(racedb.Race).join("series").filter(racedb.RaceSeries.seriesid==seriesid).order_by(racedb.Race.racenum).all():
            self.racelist.append(race.racenum)
            self.TXT[gen].write('\tRace {0}: {1}: {2}\n'.format(race.racenum,race.name,race.date))
            numraces += 1
        self.TXT[gen].write('\n')

        # set up cols format string, and render header
        NAMELEN = 40
        COLWIDTH = 5
        self.linefmt = '{{place:5s}} {{name:{0}s}} '.format(NAMELEN)
        for racenum in self.racelist:
            self.linefmt += '{{race{0}:{1}s}} '.format(racenum,COLWIDTH)
        self.linefmt += '{total:10s}\n'
        
        self.clearline(gen)
        self.setplace(gen,'')
        self.setname(gen,'')
        self.settotal(gen,'Total Pts.')
        
        for racenum in self.racelist:
            self.setrace(gen,racenum,racenum)
            
        self.render(gen)

        return numraces
    
    #----------------------------------------------------------------------
    def clearline(self,gen):
    #----------------------------------------------------------------------
        '''
        prepare rendering line for output by clearing all entries

        :param gen: gender M or F
        '''
        
        for k in self.pline[gen]:
            self.pline[gen][k] = ''
    
    #----------------------------------------------------------------------
    def setplace(self,gen,place):
    #----------------------------------------------------------------------
        '''
        put value in 'place' column for output (this should be rendered in 1st column)

        :param gen: gender M or F
        :param place: value for place column
        '''
        
        self.pline[gen]['place'] = str(place)
    
    #----------------------------------------------------------------------
    def setname(self,gen,name):
    #----------------------------------------------------------------------
        '''
        put value in 'name' column for output (this should be rendered in 2nd column)

        :param gen: gender M or F
        :param name: value for name column
        '''
        
        self.pline[gen]['name'] = str(name)
    
    #----------------------------------------------------------------------
    def setrace(self,gen,racenum,result):
    #----------------------------------------------------------------------
        '''
        put value in 'race{n}' column for output, for race n
        should be '' for empty race

        :param gen: gender M or F
        :param racenum: number of race
        :param result: value for race column
        '''
        
        self.pline[gen]['race{0}'.format(racenum)] = str(result)
    
    #----------------------------------------------------------------------
    def settotal(self,gen,total):
    #----------------------------------------------------------------------
        '''
        put value in 'race{n}' column for output, for race n
        should be '' for empty race

        :param gen: gender M or F
        :param total: value for total column
        '''
        
        self.pline[gen]['total'] = str(total)
    
    #----------------------------------------------------------------------
    def render(self,gen):
    #----------------------------------------------------------------------
        '''
        output current line to gender file

        :param gen: gender M or F
        '''

        self.TXT[gen].write(self.linefmt.format(**self.pline[gen]))
    
    #----------------------------------------------------------------------
    def skipline(self,gen):
    #----------------------------------------------------------------------
        '''
        output blank line to gender file

        :param gen: gender M or F
        '''

        self.TXT[gen].write('\n')
    
    #----------------------------------------------------------------------
    def close(self):
    #----------------------------------------------------------------------
        '''
        output blank line to gender file

        :param gen: gender M or F
        '''
        
        for gen in ['F','M']:
            self.TXT[gen].close()
    
########################################################################
class StandingsRenderer():
########################################################################
    '''
    StandingsRenderer collects standings and provides rendering methods, for a single series
    
    :param session: database session
    :param seriesname: series.name
    :param seriesid: series.id
    :param orderby: database field by which standings should be ordered (e.g., racedb.RaceResult.time)
    :param hightolow: True if ordering is high value to low value
    :param bydiv: True if standings are to be tallied by division, in addition to by gender
    :param avgtie: True if tie points are averaged, else max points is used for both
    :param multiplier: race points are multiplied by this value
    :param maxgenpoints: maximum number of points by gender for first place result.  If None, standings are tallied directly
    :param maxdivpoints: maximum number of points by division for first place result
    :param maxraces: maximum number of races run by a runner to be included in total points
    '''
    #----------------------------------------------------------------------
    def __init__(self,session,seriesname,seriesid,orderby,hightolow,bydiv,avgtie,multiplier=1,maxgenpoints=None,maxdivpoints=None,maxraces=None):
    #----------------------------------------------------------------------
        self.session = session
        self.seriesname = seriesname
        self.seriesid = seriesid
        self.orderby = orderby
        self.hightolow = hightolow
        self.bydiv = bydiv
        self.avgtie = avgtie
        self.multiplier = multiplier
        self.maxgenpoints = maxgenpoints
        self.maxdivpoints = maxdivpoints
        self.maxraces = maxraces
        
    #----------------------------------------------------------------------
    def collectstandings(self,racesprocessed,gen,raceid,byrunner,divrunner): 
    #----------------------------------------------------------------------
        '''
        collect standings for this race / series
        
        in byrunner[name][type], points{race} entries are set to '' for race not run, to 0 for race run but no points given
        
        :param racesprocessed: number of races processed so far
        :param gen: gender, M or F
        :param raceid: race.id to collect standings for
        :param byrunner: dict updated as runner standings are collected {name:{'bygender':[points1,points2,...],'bydivision':[points1,points2,...]}}
        :param divrunner: dict updated with runner names by division {div:[runner1,runner2,...],...}
        :rtype: number of standings processed for this race / series
        '''
        numresults = 0
    
        # get all the results currently in the database
        # byrunner = {name:{'bygender':[points,points,...],'bydivision':[points,points,...]}, ...}
        allresults = self.session.query(racedb.RaceResult).order_by(self.orderby).filter_by(raceid=raceid,seriesid=self.seriesid,gender=gen).all()
        if self.hightolow: allresults.sort(reverse=True)
        
        for resultndx in range(len(allresults)):
            numresults += 1
            result = allresults[resultndx]
            
            # add runner name 
            name = result.runner.name
            if name not in byrunner:
                byrunner[name] = {}
                byrunner[name]['bygender'] = []
                if self.bydiv:
                    if name not in divrunner[(result.divisionlow,result.divisionhigh)]:
                        divrunner[(result.divisionlow,result.divisionhigh)].append(name)
                    byrunner[name]['bydivision'] = []
            
            # for this runner, catch 'bygender' and 'bydivision' up to current race position
            while len(byrunner[name]['bygender']) < racesprocessed:
                byrunner[name]['bygender'].append('')
                if self.bydiv:
                    byrunner[name]['bydivision'].append('')
                    
            # accumulate points for this result
            # if result is ordered by time, genderplace and divisionplace are used
            if self.orderby == racedb.RaceResult.time:
                # if result points depend on the number of runners, update maxgenpoints
                if byrunner:
                    maxgenpoints = len(allresults)
                
                # if starting at the top (i.e., maxgenpoints is non-zero, accumulate points accordingly
                if maxgenpoints:
                    genpoints = self.multiplier*(self.maxgenpoints+1-result.genderplace)
                
                # otherwise, accumulate from the bottom (this should never happen)
                else:
                    genpoints = self.multiplier*result.genderplace
                
                byrunner[name]['bygender'].append(max(genpoints,0))
                if self.bydiv:
                    divpoints = self.multiplier*(self.maxdivpoints+1-result.divisionplace)
                    byrunner[name]['bydivision'].append(max(divpoints,0))
            
            # if result was ordered by agpercent, agpercent is used -- assume no divisions
            elif self.orderby == racedb.RaceResult.agpercent:
                # some combinations don't make sense, and have been commented out
                # TODO: verify combinations in updaterace.py
                
                ## if result points depend on the number of runners, update maxgenpoints
                #if byrunner:
                #    maxgenpoints = len(allresults)
                #
                ## if starting at the top (i.e., maxgenpoints is non-zero, accumulate points accordingly
                #if maxgenpoints:
                #    genpoints = self.multiplier*(self.maxgenpoints+1-result.genderplace)
                #
                ## otherwise, accumulate from the bottom (this should never happen)
                #else:
                genpoints = int(round(self.multiplier*result.agpercent))
                
                byrunner[name]['bygender'].append(max(genpoints,0))
                #if self.bydiv:
                #    divpoints = self.multiplier*(self.maxdivpoints+1-result.divisionplace)
                #    byrunner[name]['bydivision'].append(max(divpoints,0))
            
            elif self.orderby == racedb.RaceResult.agtime:
                # TODO: this section needs to be updated (for decathlon), currently cut/paste from orderby time
                
                # if result points depend on the number of runners, update maxgenpoints
                if byrunner:
                    maxgenpoints = len(allresults)
                
                # if starting at the top (i.e., maxgenpoints is non-zero, accumulate points accordingly
                if maxgenpoints:
                    genpoints = self.multiplier*(self.maxgenpoints+1-result.genderplace)
                
                # otherwise, accumulate from the bottom (this should never happen)
                else:
                    genpoints = self.multiplier*result.genderplace
                
                byrunner[name]['bygender'].append(max(genpoints,0))
                if self.bydiv:
                    divpoints = self.multiplier*(self.maxdivpoints+1-result.divisionplace)
                    byrunner[name]['bydivision'].append(max(divpoints,0))
            
            else:
                raise parameterError, 'results must be ordered by time, agtime or agpercent'
            
        return numresults            
    
    #----------------------------------------------------------------------
    def renderseries(self,fh): 
    #----------------------------------------------------------------------
        '''
        render standings for a single series
        
        fh object has the following methods
        * numraces = prepare(gender,seriesname,seriesid,year)
        * clearline(gender)
        * setplace(gender,place)
        * setname(gender,name)
        * setrace(gender,racenum,result)
        * settotal(gender,total)
        * render(gender)  puts standings into a file handled by fh for gender
        * skipline(gender) insert blank line
        * close()
        
        :param fh: StandingsHandler object-like
        '''

        # collect divisions, if necessary
        if self.bydiv:
            divisions = []
            for div in self.session.query(racedb.Divisions).filter_by(seriesid=self.seriesid,active=True).order_by(racedb.Divisions.divisionlow).all():
                divisions.append((div.divisionlow,div.divisionhigh))
            if len(divisions) == 0:
                raise dbConsistencyError, 'series {0} indicates divisions to be calculated, but no divisions found'.format(self.seriesname)

        # Get first race for filename year -- assume all active races are within the same year
        firstrace = self.session.query(racedb.Race).filter_by(active=True).order_by(racedb.Race.racenum).first()
        year = firstrace.year
        
        # process each gender
        for gen in ['F','M']:
            # open file, prepare header, etc
            fh.prepare(gen,self.seriesname,self.seriesid,year)
                    
            # collect data for each race, within byrunner dict
            # also track names of runners within each division
            byrunner = {}
            divrunner = None
            if self.bydiv:
                divrunner = {}
                for div in divisions:
                    divrunner[div] = []
                
            racesprocessed = 0
            for race in self.session.query(racedb.Race).join("results").all():
                self.collectstandings(racesprocessed,gen,race.id,byrunner,divrunner)
                racesprocessed += 1
                
            # render standings
            # first by division
            if self.bydiv:
                fh.clearline(gen)
                fh.setplace(gen,'Place')
                fh.setname(gen,'Age Group')
                fh.render(gen)
                
                for div in divisions:
                    fh.clearline(gen)
                    divlow,divhigh = div
                    if divlow == 0:     divtext = '{0} & Under'.format(divhigh)
                    elif divhigh == 99: divtext = '{0} & Over'.format(divlow)
                    else:               divtext = '{0} to {1}'.format(divlow,divhigh)
                    fh.setname(gen,divtext)
                    fh.render(gen)
                    
                    # calculate runner total points
                    bypoints = []
                    for name in divrunner[div]:
                        # convert each race result to int if possible
                        byrunner[name]['bydivision'] = [int(r) if type(r)==float and r==int(r) else r for r in byrunner[name]['bydivision']]
                        racetotals = byrunner[name]['bydivision'][:]    # make a copy
                        racetotals.sort(reverse=True)
                        # total numbers only, and convert to int if possible
                        racetotals = [r for r in racetotals if type(r) in [int,float]]
                        totpoints = sum(racetotals[:min(self.maxraces,len(racetotals))])
                        totpoints = int(totpoints) if totpoints == int(totpoints) else totpoints
                        bypoints.append((totpoints,name))
                    
                    # sort runners within division by total points and render
                    bypoints.sort(reverse=True)
                    thisplace = 1
                    for runner in bypoints:
                        totpoints,name = runner
                        fh.clearline(gen)
                        fh.setplace(gen,thisplace)
                        thisplace += 1
                        fh.setname(gen,name)
                        fh.settotal(gen,totpoints)
                        racenum = 1
                        for pts in byrunner[name]['bydivision']:
                            fh.setrace(gen,racenum,pts)
                            racenum += 1
                        fh.render(gen)
                        
                    # skip line between divisions
                    fh.skipline(gen)
                        
            # then overall
            fh.clearline(gen)
            fh.setplace(gen,'Place')
            fh.setname(gen,'Overall')
            fh.render(gen)
            
            # calculate runner total points
            bypoints = []
            for name in byrunner:
                # convert each race result to int if possible
                byrunner[name]['bygender'] = [int(r) if type(r)==float and r==int(r) else r for r in byrunner[name]['bygender']]
                racetotals = byrunner[name]['bygender'][:]    # make a copy
                racetotals.sort(reverse=True)
                # total numbers only, and convert to int if possible
                racetotals = [r for r in racetotals if type(r) in [int,float]]
                totpoints = sum(racetotals[:min(self.maxraces,len(racetotals))])
                totpoints = int(totpoints) if totpoints == int(totpoints) else totpoints
                bypoints.append((totpoints,name))
            
            # sort runners by total points and render
            bypoints.sort(reverse=True)
            thisplace = 1
            for runner in bypoints:
                totpoints,name = runner
                fh.clearline(gen)
                fh.setplace(gen,thisplace)
                thisplace += 1
                fh.setname(gen,name)
                fh.settotal(gen,totpoints)
                racenum = 1
                for pts in byrunner[name]['bygender']:
                    fh.setrace(gen,racenum,pts)
                    racenum += 1
                fh.render(gen)
            fh.skipline(gen)
                        
        # done with rendering
        fh.close()
            
#----------------------------------------------------------------------
def main(): 
#----------------------------------------------------------------------
    '''
    render result information
    '''
    parser = argparse.ArgumentParser(version='{0} {1}'.format('runningclub',version.__version__))
    parser.add_argument('-r','--racedb',help='filename of race database (default %(default)s)',default='sqlite:///racedb.db')
    parser.add_argument('-s','--series',help='series to render',default=None)
    args = parser.parse_args()
    
    racedb.setracedb(args.racedb)
    session = racedb.Session()
    
    # get filtered series, which have any results
    sfilter = {'active':True}
    theseseries = session.query(racedb.Series).filter_by(**sfilter).join("results").all()
    
    fh = ListStandingsHandler()
    fh.addhandler(TxtStandingsHandler(session))
    
    for series in theseseries:
        # orderby parameter is specified by the series
        orderby = getattr(racedb.RaceResult,series.orderby)
        
        # render the standings, according to series specifications
        rr = StandingsRenderer(session,series.name,series.id,orderby,series.hightolow,series.divisions,
                               series.averagetie,multiplier=series.multiplier,maxgenpoints=series.maxgenpoints,
                               maxdivpoints=series.maxdivpoints,maxraces=series.maxraces)
        rr.renderseries(fh)

    session.close()
        
# ##########################################################################################
#	__main__
# ##########################################################################################
if __name__ == "__main__":
    main()

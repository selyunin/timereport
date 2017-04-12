#!/usr/bin/python

import cmd, sys
import datetime
import calendar
import signal
import io
import os
import re
import readline
import subprocess
from lxml import etree as ET
from tempfile import mkstemp
from shutil import move, copy
from tempfile import mkstemp
from dateutil.relativedelta import relativedelta

import timereport as tr

class cdate:
    day = datetime.date.today()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = "\033[1m"

class holidays:
    @classmethod
    def get(self,year):
        return [datetime.date(year,1,1),
                datetime.date(year,5,1),
                datetime.date(year,11,1)]

class TimereportShell(cmd.Cmd):
    intro = \
    'Welcome to the timereport. Type help or ? to list commands.\n' + \
        bcolors.BOLD + bcolors.OKBLUE + 'Today: ' + bcolors.ENDC    + \
        bcolors.BOLD + bcolors.FAIL + cdate.day.strftime("%a, %d %B %Y") + \
        bcolors.ENDC
    prompt = bcolors.BOLD + bcolors.OKGREEN + '(timereport: ' + \
             bcolors.ENDC + cdate.day.strftime('%B %Y')       + \
             bcolors.BOLD + bcolors.OKGREEN + ' ) ' + bcolors.ENDC
    file = None

    # ----- basic timesheet commands -----
    def do_set_month(self, arg):
        'Specify month different from the today\'s month (arguments: month and year):  set_month [1-12] [20**]'
        args = parse(arg)
        month = int(args[0])
        year = int(args[1])
        cdate.day = datetime.date(year, month, 1)
        self.prompt = bcolors.BOLD + bcolors.OKGREEN + \
                '(timereport: ' + bcolors.ENDC + cdate.day.strftime('%B %Y')  + \
                 bcolors.BOLD + bcolors.OKGREEN + ' ) ' + bcolors.ENDC

    def do_create_month(self, arg):
        'Create empty xml document if does not exist for the month and year specified as arguments:  create_month [1-12] [20**]'
        args = parse(arg)
        month = int(args[0])
        year  = int(args[1])
        if ((month < 1) or (month > 12)):
            print 'Specify month: 1 - 12'
        elif year < 1970 or year > 2200:
            print 'You did / will not work at this time. I\'m sure'
        elif (year > 1970) and (year < 2200) and (month > 0) and (month < 13):
            tr.create_month(month, year)
            print bcolors.BOLD + bcolors.HEADER + \
                  datetime.date(year, month, 1).strftime("%Y_%B") + ".xml " + \
                  bcolors.ENDC + "Created in xml/"
        else:
            print 'Arguments not correct'

    def do_fill_day(self, arg):
        'Fill in xml entry for the date specified as an argument:  fill_day 23'
        args = parse(arg)
        print args
        if len(args) != 1:
            print 'Enter exactly one date'
            return False
        day = int(args[0])
        if day < 0 or day > calendar.monthrange(cdate.day.year, cdate.day.month)[1]:
            print 'Invalid day in the current month'
            return False
        self.prompt = bcolors.BOLD + bcolors.OKGREEN + \
                '(timereport: ' + bcolors.ENDC + cdate.day.strftime('%B %Y') + \
                ' ==> '+ tr.xstr(args[0])  + \
                bcolors.BOLD + bcolors.OKGREEN + ' ) ' + bcolors.ENDC

    def do_edit_day(self, arg):
        'Edit xml entry for the date specified as an argument:  edit_day 15'
        args = parse(arg)
        day = int(args[0])
        if day < 0 or day > calendar.monthrange(cdate.day.year, cdate.day.month)[1]:
            print 'Invalid day in the current month'
            return False
        self.prompt = bcolors.BOLD + bcolors.OKGREEN + \
                '(timereport: ' + bcolors.ENDC + cdate.day.strftime('%B %Y') + \
                ' ==> '+ tr.xstr(args[0])  + \
                bcolors.BOLD + bcolors.OKGREEN + ' ) ' + bcolors.ENDC
        #open xml file
        print cdate.day.strftime("%Y_%B") + ".xml"
        filename = cdate.day.strftime("%Y_%B") + ".xml"
        if not os.path.isfile('xml/' + filename):
            print 'No ' + filename + ' file exists.' + \
                    ' use create_month first'
            return False
        month = tr.read_month(filename)
        for date in month:
            if date.day == day:
                date.projectDescription = \
                        self.rlinput('desciption       --> ',date.projectDescription)
                date.WP = \
                        self.rlinput('WP               --> ',tr.xstr(date.WP))
                date.task = \
                        self.rlinput('task             --> ',tr.xstr(date.task))
                date.ACT = \
                        self.rlinput('ACT              --> ', date.ACT)
                date.projectHours = tr.xfloat(\
                        self.rlinput('proj. Hours      --> ', tr.xstr(date.projectHours)))
                date.otherDescription = \
                        self.rlinput('oth. description --> ', date.otherDescription)
                date.otherHours = tr.xfloat(\
                        self.rlinput('other hours      --> ', tr.xstr(date.otherHours)))
                date.absenceReason = \
                        self.rlinput('absence reason   --> ', date.absenceReason)
                date.absenceHours = tr.xfloat(\
                        self.rlinput('absence hours    --> ',tr.xstr(date.absenceHours)))
                date.productiveHours = date.projectHours + date.otherHours
                print 'Done for this day!'
        summary = self.calc_summary(month)
        tr.writeXml(month,filename,summary)
        self.prompt = bcolors.BOLD + bcolors.OKGREEN + \
                '(timereport: ' + bcolors.ENDC + cdate.day.strftime('%B %Y')  + \
                 bcolors.BOLD + bcolors.OKGREEN + ' ) ' + bcolors.ENDC

    def do_show_day(self, arg):
        'Display the xml entry for the date specified as an argument:  show_day 15'


    def do_gen_latex(self, arg):
        'Generate LaTeX table for currently set month from xml/ : gen_latex '
        filename = cdate.day.strftime("%Y_%B") + ".xml" 
        if not os.path.isfile('xml/' + filename):
            print 'No ' + filename + ' file exists.' + \
                    ' use create_month first'
            return False
        c_month = tr.read_month(filename)
        monthTable = open("monthData.tex", "w+")
        for day in c_month:
            dateString = ""
            if ( day.weekday == 'Sat' or day.weekday == 'Sun' or 
                 day.absenceReason.lower() == 'national holiday'):
                dateString = "\\rowcolor{red!20}\n" 
            dateString += day.weekday + ' & ' + tr.xstr(day.day) + \
                    ' & ' + day.projectDescription + ' & ' + \
                    tr.xstr(day.WP) + ' & ' +  tr.xstr(day.task) + ' & ' + day.ACT + ' & ' + \
                    tr.xstr(day.projectHours) + ' & ' + \
                    day.otherDescription + ' & '  + tr.xstr(day.otherHours) +\
                    ' & ' + day.absenceReason + \
                    ' & ' + tr.xstr(day.absenceHours) + ' & ' + \
                    tr.xstr(day.productiveHours) + \
                    "\\\\\\hline" + "\n"
            monthTable.write(dateString)
        summary = self.calc_summary(c_month)
        summary_str = "\\hline\n\\multicolumn{2}{|c|}{\\bf Summary:} " +\
                "& \\multicolumn{4}{|c|}{} & {\\bf " +\
                tr.xstr(summary.projectSummary) + \
                "} & & {\\bf " + \
                tr.xstr(summary.otherSummary)  + \
                "}  & & {\\bf " + \
                tr.xstr(summary.absenceSummary) +\
                "} & {\\bf " + \
                tr.xstr(summary.productiveSummary) + \
                "} \\\\\\hline\n"
        monthTable.write(summary_str)
        monthTable.close()
        
        monthName = cdate.day.strftime("%Y_%B" + ".tex")
        copy('timereport.tex', monthName)
        self.replace(monthName, 'MonthName', cdate.day.strftime("%B %Y"))
        signature_date = cdate.day
        year = cdate.day.year
        month = cdate.day.month
        day = 1
        if cdate.day.month != 12:
            signature_date = datetime.date(year, month+1, day)
        else:
            signature_date = datetime.date(year+1, 1, day)

        while( signature_date in holidays.get(signature_date.year) or 
            signature_date.isoweekday() == 6 or 
            signature_date.isoweekday() == 7):
            signature_date = datetime.date(signature_date.year,
                                           signature_date.month,
                                           signature_date.day + 1)
        self.replace(monthName, 'SignatureDate', signature_date.strftime('%d %B %Y'))
        bashCommand = 'pdflatex ' + monthName
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

    def replace(self, file_path, pattern, subst):
        #Create temp file
        fh, abs_path = mkstemp()
        with open(abs_path,'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    new_file.write(line.replace(pattern, subst))
        os.close(fh)
        #Remove original file
        os.remove(file_path)
        #Move new file
        move(abs_path, file_path)

    def calc_summary(self, month):
        summary = tr.Summary()
        #compute summary
        for day in month:
            summary.projectSummary += day.projectHours
            summary.otherSummary += day.otherHours
            summary.absenceSummary += day.absenceHours

        summary.productiveSummary = summary.projectSummary + \
                                    summary.otherSummary #- \
                                    #summary.absenceSummary
        return summary

    def rlinput(self, prompt, prefill=''):
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return raw_input(prompt)
        finally:
            readline.set_startup_hook()   


    def do_stats(self, arg):
        'Show stats for the whole month:  stats'
        #left(*parse(arg))

    def do_stats(self, arg):
        'Show stats for the whole month:  stats'
        #left(*parse(arg))

    def do_quit(self, arg):
        'Quit timereport:  quit'
        print 'Exit...'
        self.close()
        return True
    def do_exit(self, arg):
        'Exit timereport:  exit'
        print 'Exit...'
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return map(int, arg.split())

def signal_handler(signal, frame):
        sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    TimereportShell().cmdloop()

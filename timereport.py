#!/usr/bin/python

import datetime
import calendar
import io
import os
import re
from lxml import etree as ET
from tempfile import mkstemp
from shutil import move

month = 11
date = 1
year = 2014

monthStart = datetime.date(year, month, date)
currentDate = monthStart

xmlFilename = monthStart.strftime("%B_%Y") + ".xml"

#array of month dates
month = []
while currentDate.month == monthStart.month:
    month.append(currentDate)
    currentDate += datetime.timedelta(days=1)

class Day:
    def __init__(self, weekday, date, projectDescription, WP, task, ACT, 
            projectHours, otherDescription, otherHours, absenceReason, absenceHours, productiveHours):
        self.weekday = weekday
        m = re.match('^(\d\d)-(\d\d)-(\d\d\d\d)$', date)
        self.day = xint(m.group(1))
        self.month = xint(m.group(2))
        self. year = xint(m.group(3))
        self.date = datetime.date(self.year, self.month, self.day)
        self.projectDescription = projectDescription
        self.WP = xint(WP)
        self.task = xint(task)
        self.ACT = ACT
        self.projectHours = xfloat(projectHours)
        self.otherDescription = otherDescription
        self.otherHours = xfloat(otherHours)
        self.absenceReason = absenceReason
        self.absenceHours = xfloat(absenceHours)
        self.productiveHours = xfloat(productiveHours)

def create_month(month, year):
    monthStart = datetime.date(year, month, 1)
    currentDate = monthStart
    xmlFilename = monthStart.strftime("%Y_%B") + ".xml"
    month = []
    while currentDate.month == monthStart.month:
        month.append(currentDate)
        currentDate += datetime.timedelta(days=1)
    if not os.path.isfile('xml/' + xmlFilename):
        root = ET.Element("timesheet")
        root.set("month", monthStart.strftime("%B"))
        for date in month:
            day = ET.SubElement(root, "day")
            #weekdate and date
            weekday = ET.SubElement(day, "weekday")
            weekday.text = date.strftime("%a")
            thisdate = ET.SubElement(day,"date")
            thisdate.text = date.strftime("%d-%m-%Y")
            #project activities
            projectActivities = ET.SubElement(day, "projectActivities")
            description = ET.SubElement(projectActivities,"description")
            description.text = ""
            WP = ET.SubElement(projectActivities, "WP")
            WP.text = ""
            Task = ET.SubElement(projectActivities, "Task")
            Task.text = ""
            ACT = ET.SubElement(projectActivities, "ACT")
            ACT.text = ""
            Hours = ET.SubElement(projectActivities, "hours")
            Hours.text = ""
            #other activities
            otherActivities = ET.SubElement(day, "otherActivities")
            descriptionOther = ET.SubElement(otherActivities,"description")
            descriptionOther.text = ""
            hoursOther = ET.SubElement(otherActivities,"hours")
            hoursOther.text = ""
            #absence
            absence = ET.SubElement(day, "absence")
            descriptionAbsence = ET.SubElement(absence,"reason")
            descriptionAbsence.text = ""
            hoursAbsence = ET.SubElement(absence,"hours")
            hoursAbsence.text = ""
            #productiveHours
            productiveHours = ET.SubElement(day, "productiveHours")
            productiveHours.text = ""
        #summary Hours for month
        summary = ET.SubElement(root, "summary")
        projectSummary = ET.SubElement(summary, "projectSummary")
        projectSummary.text = ""
        otherSummary = ET.SubElement(summary, "otherSummary")
        otherSummary.text = ""
        absenceSummary = ET.SubElement(summary, "absenceSummary")
        absenceSummary.text = ""
        # wrap it in an ElementTree instance, and save as XML
        tree = ET.ElementTree(root)
        tree.write('xml/' + xmlFilename, pretty_print=True)
    else:
        print 'such month already exists in \'xml\' '

def create_another_month(month, year):
    print 'Executing month'

class Summary:
    def __init__(self):
        self.projectSummary = 0
        self.otherSummary = 0
        self.absenceSummary = 0 
        self.productiveSummary = 0

#create xml document if does not exist
if not os.path.isfile('xml/' + xmlFilename):
    root = ET.Element("timesheet")
    root.set("month", monthStart.strftime("%B"))
    for date in month:
        day = ET.SubElement(root, "day")
        #weekdate and date
        weekday = ET.SubElement(day, "weekday")
        weekday.text = date.strftime("%a")
        thisdate = ET.SubElement(day,"date")
        thisdate.text = date.strftime("%d-%m-%Y")
        #project activities
        projectActivities = ET.SubElement(day, "projectActivities")
        description = ET.SubElement(projectActivities,"description")
        description.text = ""
        WP = ET.SubElement(projectActivities, "WP")
        WP.text = ""
        Task = ET.SubElement(projectActivities, "Task")
        Task.text = ""
        ACT = ET.SubElement(projectActivities, "ACT")
        ACT.text = ""
        Hours = ET.SubElement(projectActivities, "hours")
        Hours.text = ""
        #other activities
        otherActivities = ET.SubElement(day, "otherActivities")
        descriptionOther = ET.SubElement(otherActivities,"description")
        descriptionOther.text = ""
        hoursOther = ET.SubElement(otherActivities,"hours")
        hoursOther.text = ""
        #absence
        absence = ET.SubElement(day, "absence")
        descriptionAbsence = ET.SubElement(absence,"reason")
        descriptionAbsence.text = ""
        hoursAbsence = ET.SubElement(absence,"hours")
        hoursAbsence.text = ""
        #productiveHours
        productiveHours = ET.SubElement(day, "productiveHours")
        productiveHours.text = ""
    #summary Hours for month
    summary = ET.SubElement(root, "summary")
    projectSummary = ET.SubElement(summary, "projectSummary")
    projectSummary.text = ""
    otherSummary = ET.SubElement(summary, "otherSummary")
    otherSummary.text = ""
    absenceSummary = ET.SubElement(summary, "absenceSummary")
    absenceSummary.text = ""
    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    tree.write('xml/' + xmlFilename, pretty_print=True)

def xstr(s):
    if s is None or s == 0:
        return ''
    else:
        return str(s)

def xint(s):
    if s is "":
        return 0
    else:
        return int(s)

def xfloat(s):
    if s is "":
        return 0
    else:
        return float(s)

def read_month(month_name):
    monthDataXml = open('xml/' + month_name, "r")
    tree = ET.parse(monthDataXml) 
    month = []
    for day in tree.xpath('//day'):
        weekday = xstr(day.xpath('child::weekday')[0].text)
        date = xstr(day.xpath('child::date')[0].text)
        projectDescription = xstr(day.xpath('child::projectActivities/description')[0].text)
        WP = xstr(day.xpath('child::projectActivities/WP')[0].text)
        task = xstr(day.xpath('child::projectActivities/Task')[0].text)
        ACT = xstr(day.xpath('child::projectActivities/ACT')[0].text)
        projectHours = xstr(day.xpath('child::projectActivities/hours')[0].text)
        otherDescription = xstr(day.xpath('child::otherActivities/description')[0].text)
        otherHours = xstr(day.xpath('child::otherActivities/hours')[0].text)
        absenceReason = xstr(day.xpath('child::absence/reason')[0].text)
        absenceHours = xstr(day.xpath('child::absence/hours')[0].text)
        productiveHours = xstr(day.xpath('child::productiveHours')[0].text)
        #create a Day object
        thisDay = Day(weekday, date, projectDescription, WP, task, ACT, projectHours,
                otherDescription, otherHours, absenceReason, absenceHours, productiveHours)
        month.append(thisDay)
        monthDataXml.close()
    return month


#parse the xml document and create Latex Table in monthData.tex
monthTable = open("monthData.tex", "w+")
monthDataXml = open('xml/' + xmlFilename, "r")
tree = ET.parse(monthDataXml) 
month = []
for day in tree.xpath('//day'):
    weekday = xstr(day.xpath('child::weekday')[0].text)
    date = xstr(day.xpath('child::date')[0].text)
    projectDescription = xstr(day.xpath('child::projectActivities/description')[0].text)
    WP = xstr(day.xpath('child::projectActivities/WP')[0].text)
    task = xstr(day.xpath('child::projectActivities/Task')[0].text)
    ACT = xstr(day.xpath('child::projectActivities/ACT')[0].text)
    projectHours = xstr(day.xpath('child::projectActivities/hours')[0].text)
    otherDescription = xstr(day.xpath('child::otherActivities/description')[0].text)
    otherHours = xstr(day.xpath('child::otherActivities/hours')[0].text)
    absenceReason = xstr(day.xpath('child::absence/reason')[0].text)
    absenceHours = xstr(day.xpath('child::absence/hours')[0].text)
    productiveHours = xstr(day.xpath('child::productiveHours')[0].text)
    #create a Day object
    thisDay = Day(weekday, date, projectDescription, WP, task, ACT, projectHours,
            otherDescription, otherHours, absenceReason, absenceHours, productiveHours)
    month.append(thisDay)
    dateString = ""
    if ( weekday == 'Sat' or weekday == 'Sun'):
        dateString = "\\rowcolor{red!20}\n" 
    dateString += weekday + ' & ' + date + ' & ' + projectDescription + ' & ' + WP + ' & ' + \
            task + ' & ' + ACT + ' & ' + projectHours + ' & ' + otherDescription + ' & '   + \
            otherHours + ' & ' + absenceReason + ' & ' + absenceHours + ' & ' + productiveHours + \
            "\\\\\\hline" + "\n"
    monthTable.write(dateString)

monthTable.close()
monthDataXml.close()

# first: parse an xml month file to an array of day objects. and a singleton summary object.
# modify day objects, recalculate summary, upon completion write everything back to xml file.
summary = Summary()
#compute summary
for day in month:
    summary.projectSummary += day.projectHours
    summary.otherSummary += day.otherHours
    summary.absenceSummary += day.absenceHours

summary.productiveSummary = summary.projectSummary + summary.otherSummary - summary.absenceSummary

#convert array of Day objects to xml and write this xml
def writeXml(month, filename,summary):
    root = ET.Element("timesheet")
    root.set("month", month[0].date.strftime("%B"))
    for day in month:
        dayXml = ET.SubElement(root, "day")
        #weekdate and date
        weekday = ET.SubElement(dayXml, "weekday")
        weekday.text = xstr(day.weekday)
        thisdate = ET.SubElement(dayXml,"date")
        thisdate.text = day.date.strftime("%d-%m-%Y")
        #project activities
        projectActivities = ET.SubElement(dayXml, "projectActivities")
        description = ET.SubElement(projectActivities,"description")
        description.text = xstr(day.projectDescription)
        WP = ET.SubElement(projectActivities, "WP")
        WP.text = xstr(day.WP)
        Task = ET.SubElement(projectActivities, "Task")
        Task.text = xstr(day.task)
        ACT = ET.SubElement(projectActivities, "ACT")
        ACT.text = xstr(day.ACT)
        Hours = ET.SubElement(projectActivities, "hours")
        Hours.text = xstr(day.projectHours)
        #other activities
        otherActivities = ET.SubElement(dayXml, "otherActivities")
        otherDescription = ET.SubElement(otherActivities,"description")
        otherDescription.text = xstr(day.otherDescription)
        otherHours = ET.SubElement(otherActivities,"hours")
        otherHours.text = xstr(day.otherHours)
        #absence
        absence = ET.SubElement(dayXml, "absence")
        absenceReason = ET.SubElement(absence,"reason")
        absenceReason.text = xstr(day.absenceReason)
        absenceHours = ET.SubElement(absence,"hours")
        absenceHours.text = xstr(day.absenceHours)
        #productiveHours
        productiveHours = ET.SubElement(dayXml, "productiveHours")
        productiveHours.text = xstr(day.productiveHours)
    #summary Hours for month
    summaryXml = ET.SubElement(root, "summary")
    projectSummary = ET.SubElement(summaryXml, "projectSummary")
    projectSummary.text = xstr(summary.projectSummary)
    otherSummary = ET.SubElement(summaryXml, "otherSummary")
    otherSummary.text = xstr(summary.otherSummary)
    absenceSummary = ET.SubElement(summaryXml, "absenceSummary")
    absenceSummary.text = xstr(summary.absenceSummary)
    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    tree.write('xml/' + filename, pretty_print=True)

writeXml(month, xmlFilename, summary)

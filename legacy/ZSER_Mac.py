"""Let's import some useful functions first"""
import os
from psychopy import core, visual, monitors, gui, data, event
import numpy as np
import random, math
import pickle

# get the current working directory
workpath = os.getcwd()

"""Some important notes in the beginning"""
# The whole script - i.e. the the definition of the coordinates - works
# when the PRL is in the top right or top left based on the screen center.
# If that isn't the case some calculations for the flanker have to be redone.
# Here: PRL is up-right; oppPRL is up-left
# if vice versa => re-lable beginning from "#define the conditions"

"""Window before the start of the experiment"""
# initialize start window
try:  # try to get a previous parameters file
    with open('lastParams.pickle', 'rb') as opener:
        expInfo = pickle.load(opener)
except:  # if not there then use a default set
    expInfo = {'1. participant': '000', '2. x-coordinate PRL': 0, '3. y-coordinate PRL': 0, '4. x-coordinate oppPRL': 0,
               '5. y-coordinate oppPRL': 0, '6. distance from screen': 50}
#
#
#
"""Initialize parameter window"""
##
# present a dialogue to change parameters
dlg = gui.DlgFromDict(expInfo, title='Crowding ZSER Control', fixed=['date'])
if dlg.OK:
    print(dlg)
    print(expInfo)
else:
    core.quit()  # the user hits cancel so exit
# save new data in pickle
picklePath = workpath + '/LastParams.pickle'
with open(picklePath, 'wb') as handle:
    pickle.dump(expInfo, handle)
    handle.close()
#
#
#
"""Define all the specifications for the subject here"""
##
# code of the subject
subj = int(expInfo['1. participant'])
##
# Monitor Specifications - muessen zusaetzlich unter Tools -> Monitor Center geaendert werden!
winx = 1440
winy = 900
##
# distance from the screen (in cm)
scrdis = float(expInfo['6. distance from screen'])
##
# Hier muss die Bildschirmbreite (!!), nicht -diagonale eingegegeben werden - kann schon vorab erfragt und festgelegt werden - vormals: screen diagonale (in cm)
scrdia = 28.5
##
# location of the screen center
x_sc = 0.0
y_sc = 0.0
##
# location of the PRL => x- and y-coordinate (in visual degree from the screen center)
x_p = float(expInfo['2. x-coordinate PRL'])  # x-coordinate PRL
y_p = float(expInfo['3. y-coordinate PRL'])  # y-coordinate PRL
##
# location of the oppPRL => x- and y-coordinate (in visual degree from the screen center)
x_o = float(expInfo['4. x-coordinate oppPRL'])  # x-coordinate
y_o = float(expInfo['5. y-coordinate oppPRL'])  # y-coordinate
##
# size of the target and both flanker
stisi = [0.75, 0.75]  # ['deg','deg'] both numbers must be the same (^= quadratic stimulus file)
##
# size of the *linear* staircase steps
stesi = 0.1
##
# starting value of the staircase functions
# DON'T FORGET to change the value inside "val_comp.csv"
staval = 2.5
##
# number of trials
trialn = 200  # minimum number of trials per staircase (not including control trials)
##
# minimum number of reversals
revnum = 15
##
# which fixation should be used (1 = cross fixation; 2 = dot fixation; 'any other number' = no fixation)
fixuse = 1
##
# presentation time of the stimuli (in seconds)
prestime = 10
#
#
"""Stuff that shouldn't be changed"""
##
# Import Images
land_up = workpath + '/landolt_up.png'
land_do = workpath + '/landolt_do.png'
land_le = workpath + '/landolt_le.png'
land_ri = workpath + '/landolt_ri.png'
land_fu = workpath + '/landolt_fu.png'
# Import comparison file for the feedback-screen
comp_file = workpath + '/val_comp.txt'
##
# landolt opening counter
# PRL with radial flanker
pr_up = 0
pr_ri = 0
pr_do = 0
pr_le = 0
# PRL with tangential flanker
pt_up = 0
pt_ri = 0
pt_do = 0
pt_le = 0
# oppPRL with radial flanker
or_up = 0
or_ri = 0
or_do = 0
or_le = 0
# oppPRL with tangential flanker
ot_up = 0
ot_ri = 0
ot_do = 0
ot_le = 0
# PRL with no flanker
pe_up = 0
pe_ri = 0
pe_do = 0
pe_le = 0
# oppPRL with no flanker
oe_up = 0
oe_ri = 0
oe_do = 0
oe_le = 0

# rotation counter
rotation_check = 0
fixation_pr = str('-')

# allocator that checks if target and flanker overlap
overlap_ch = 0  # 0 = no overlap; 1 = in this increment an overlap would happen
#
#
#
"""Preparing the data acquisition"""
##
currentDate = data.getDateStr()  # gets the current data as a string
fileName = "ZSER_Crowding_VP" + str(expInfo['1. participant']) + "_" + currentDate  # making a filename
dataFile = open(fileName + '.csv', 'w')  # text file with comma seperated values
dataFL_1 = "VP-Code: " + str(expInfo['1. participant'])
dataFL_2 = "x-PRL: " + str(expInfo['2. x-coordinate PRL'])
dataFL_3 = "y-PRL: " + str(expInfo['3. y-coordinate PRL'])
dataFL_4 = "x-oppPRL: " + str(expInfo['4. x-coordinate oppPRL'])
dataFL_5 = "y-oppPRL: " + str(expInfo['5. y-coordinate oppPRL'])
dataFL_6 = "distance from screen: " + str(expInfo['6. distance from screen'])
dataFile.write('%s,%s,%s,%s,%s,%s\n' % (dataFL_1, dataFL_2, dataFL_3, dataFL_4, dataFL_5, dataFL_6))
dataFile.write('condition,landolt_opening,increment,response,reaction_time,fixation_detection\n')
#
#
#
"""Creating the window and the stimuli"""
##
# Setting up the monitor
mon = monitors.Monitor(name='testmonitor', width=scrdia, distance=scrdis)
##
# Creating the window
win = visual.Window(size=(winx, winy),
                    fullscr=True, screen=0,
                    color=[133, 133, 133], colorSpace='rgb255',
                    monitor=mon,
                    winType='pyglet', allowGUI=False, allowStencil=False,
                    blendMode='avg', useFBO=True,
                    units='deg')
# target stimulus created
target = visual.ImageStim(win,
                          image=land_do,
                          pos=[0, 0],
                          size=stisi)
# flanker 1 created
flanker1 = visual.ImageStim(win,
                            image=land_fu,
                            pos=[0.0, 0.0],
                            size=stisi)
# flanker 2 created
flanker2 = visual.ImageStim(win,
                            image=land_fu,
                            pos=[0.0, 0.0],
                            size=stisi)

# create the correct fixation
if fixuse == 1:  # fixationcross
    fixcross = visual.ShapeStim(win,
                                vertices='cross')
    fixcross.setColor([0, 0, 0], 'rgb255')
    fixcross.setPos([0.0, 0.0])
    fixcross.setSize([1.0, 1.0])
elif fixuse == 2:  # fixation dots
    # generating all 4 fixation dots
    fixball1 = visual.Circle(win)
    fixball1.setColor([255, 0, 0], 'rgb255')
    fixball1.setSize([0.5, 0.5])
    fixball2 = visual.Circle(win)
    fixball2.setColor([255, 0, 0], 'rgb255')
    fixball2.setSize([0.5, 0.5])
    fixball3 = visual.Circle(win)
    fixball3.setColor([255, 0, 0], 'rgb255')
    fixball3.setSize([0.5, 0.5])
    fixball4 = visual.Circle(win)
    fixball4.setColor([255, 0, 0], 'rgb255')
    fixball4.setSize([0.5, 0.5])
    # getting the position for the fixation dots
    degfromcenter = 2
    fixball1.setPos([x_sc, y_sc + degfromcenter])
    fixball2.setPos([x_sc + degfromcenter, y_sc])
    fixball3.setPos([x_sc, y_sc - degfromcenter])
    fixball4.setPos([x_sc - degfromcenter, y_sc])

# remove autodraw
target.setAutoDraw(False)
flanker1.setAutoDraw(False)
flanker2.setAutoDraw(False)
if fixuse == 1:
    fixcross.setAutoDraw(False)
elif fixuse == 2:
    fixball1.setAutoDraw(False)
    fixball2.setAutoDraw(False)
    fixball3.setAutoDraw(False)
    fixball4.setAutoDraw(False)

"""Get the timing stuff"""
clock = core.Clock()

"""Welcome screen"""

# initialize and draw the welcome text on the screen
starttext = visual.TextStim(win,
                            text="Im Folgenden werden Ihnen sogenannte Landolt-C-Reize gezeigt. \n Dabei handelt es sich um Ringe, die eine Öffnung in eine bestimmte Richtung haben. Ihre Aufgabe ist es, die Öffnung der Ringe zu entdecken und entsprechend mit den Pfeiltasten zu antworten. \n Drücken Sie also die Pfeiltaste 'oben', wenn die Öffnung oben ist, die Pfeiltaste 'links', wenn die Öffnung links ist usw. \n Fixieren Sie bitte während des gesamten Experiments stets das Fixationskreuz im Zentrum des Bildschirms! \n Drücken Sie die Leertaste um fortzufahren!")
starttext.draw()
win.flip()
# pressing spacebar will continue to the control trial text window
startResp = None
while startResp == None:
    spaceKey = event.waitKeys()
    for thisKey in spaceKey:
        if thisKey == 'space':
            startResp = 1
        elif thisKey in ['escape']:
            core.quit()
    event.clearEvents()

# initialize and draw the window, that show the control trial instructions
ctrltext = visual.TextStim(win,
                           text="Weiterhin wird in einigen Durchgängen das Fixationskreuz sich ein kleines Stück um seine eigene Achse drehen. \n Wenn Sie eine solche Drehung erkennen, drücken Sie bitte die Leertaste, anstelle auf die Öffnung zu reagieren. Drücken Sie dabei nur die Leertaste, wenn das Kreuz gedreht ist und nicht, wenn es sich wieder zurückdreht. \n Drücken Sie nun die Leertaste, um mit dem Versuch zu beginnen!")
ctrltext.draw()
win.flip()
# pressing the spacebar will start the experiment
ctrlResp = None
while ctrlResp == None:
    spaceKey = event.waitKeys()
    for thisKey in spaceKey:
        if thisKey == 'space':
            ctrlResp = 1
        elif thisKey in ['escape']:
            core.quit()
    event.clearEvents()

"""Getting the staircase and the conditions"""

eastrn = int(trialn * 0.2)  # number of trials in easy task = ohne Flanker
fixtrn = int(trialn * 0.8)  # number of trials in Fixationsaufgabe

# condition Parameters
conditions = [
    {'label': 'prltan', 'startVal': staval, 'stepType': 'lin', 'stepSizes': stesi, 'nUp': 1, 'nDown': 2,
     'nTrials': trialn, 'nReversals': revnum},
    {'label': 'prlrad', 'startVal': staval, 'stepType': 'lin', 'stepSizes': stesi, 'nUp': 1, 'nDown': 2,
     'nTrials': trialn, 'nReversals': revnum},
    {'label': 'opptan', 'startVal': staval, 'stepType': 'lin', 'stepSizes': stesi, 'nUp': 1, 'nDown': 2,
     'nTrials': trialn, 'nReversals': revnum},
    {'label': 'opprad', 'startVal': staval, 'stepType': 'lin', 'stepSizes': stesi, 'nUp': 1, 'nDown': 2,
     'nTrials': trialn, 'nReversals': revnum},
    {'label': 'peastr', 'startVal': staval, 'stepType': 'lin', 'stepSizes': stesi, 'nUp': 1, 'nDown': 2,
     'nTrials': eastrn},
    {'label': 'oeastr', 'startVal': staval, 'stepType': 'lin', 'stepSizes': stesi, 'nUp': 1, 'nDown': 2,
     'nTrials': eastrn},
    {'label': 'fixation', 'startVal': staval, 'stepType': 'lin', 'stepSizes': stesi, 'nUp': 1, 'nDown': 2,
     'nTrials': fixtrn}]

# creates the multiple staircases parallel to each other
stairs = data.MultiStairHandler(conditions=conditions, method='random')

# calculates the minimum number of trials to finish (for calculating when to break)
min_sumtrials = 4 * trialn + 2 * eastrn
# makes min_sumtrials divisable by 4 (for making the break calculations possible)
while (min_sumtrials % 4) != 0:
    min_sumtrials = min_sumtrials + 1

# break counter
brk_count = 0

"""This makes fixation before the first trial starts"""
if fixuse == 1:
    fixcross.draw()
if fixuse == 2:
    fixball1.draw()
    fixball2.draw()
    fixball3.draw()
    fixball4.draw()
win.flip()
core.wait(0.5)
win.flip()

"""The actual experiment with trials and everything"""

for thisIncrement, thisCondition in stairs:

    # condition to be met for making a a little break inbetween the trials (including an instruction text and a feedback bar)
    # break 1/4
    if brk_count == (min_sumtrials / 4):
        # 1/4 text
        starttext = visual.TextStim(win,
                                    text="Sie haben nun ungefähr ein Viertel der Übung geschafft. Sie können sich daher eine kleine Pause nehmen.\n Drücken Sie die Leertaste, um wieder mit der Aufgabe fortzufahren!",
                                    pos=[0, 3])
        # 1/4 progress bar
        prog_bar01 = visual.Rect(win, fillColor=[0.4, 0.3, 0.6], lineColor=[0, 0, 0], width=16, height=1.5, pos=[0, -3])
        prog_bar02 = visual.Rect(win, fillColor=[0.1, 0.35, 0.2], lineColor=[0, 0, 0], width=4, height=1.5,
                                 pos=[-6, -3])
        marker_0perc = visual.TextStim(win, text="0%", pos=[-8, -4.5])
        marker_25perc = visual.TextStim(win, text="25%", pos=[-4, -4.5])
        marker_50perc = visual.TextStim(win, text="50%", pos=[0, -4.5])
        marker_75perc = visual.TextStim(win, text="75%", pos=[4, -4.5])
        marker_100perc = visual.TextStim(win, text="100% geschafft!", pos=[10.5, -4.5])
        # 1/4 put on screen
        starttext.draw()
        prog_bar01.draw()
        prog_bar02.draw()
        marker_0perc.draw()
        marker_25perc.draw()
        marker_50perc.draw()
        marker_75perc.draw()
        marker_100perc.draw()
        win.flip()
        # keys required to continue
        startResp = None
        while startResp == None:
            spaceKey = event.waitKeys()
            for thisKey in spaceKey:
                if thisKey == 'space':
                    startResp = 10
                elif thisKey in ['escape']:
                    core.quit()
            event.clearEvents()
        # making the fixation before the next targets are presented
        if fixuse == 1:
            fixcross.draw()
        if fixuse == 2:
            fixball1.draw()
            fixball2.draw()
            fixball3.draw()
            fixball4.draw()
        win.flip()
        core.wait(0.5)
    # break 1/2
    elif brk_count == (min_sumtrials / 2):
        # 1/2 text
        starttext = visual.TextStim(win,
                                    text="Sie haben nun ungefähr die Hälfte der Übung geschafft. Sie können sich daher eine kleine Pause nehmen.\n Drücken Sie die Leertaste, um wieder mit der Aufgabe fortzufahren!",
                                    pos=[0, 3])
        # 1/2 progress bar
        prog_bar01 = visual.Rect(win, fillColor=[0.4, 0.3, 0.6], lineColor=[0, 0, 0], width=16, height=1.5, pos=[0, -3])
        prog_bar02 = visual.Rect(win, fillColor=[0.1, 0.35, 0.2], lineColor=[0, 0, 0], width=8, height=1.5,
                                 pos=[-4, -3])
        marker_0perc = visual.TextStim(win, text="0%", pos=[-8, -4.5])
        marker_25perc = visual.TextStim(win, text="25%", pos=[-4, -4.5])
        marker_50perc = visual.TextStim(win, text="50%", pos=[0, -4.5])
        marker_75perc = visual.TextStim(win, text="75%", pos=[4, -4.5])
        marker_100perc = visual.TextStim(win, text="100% geschafft!", pos=[10.5, -4.5])
        # 1/2 put on screen
        starttext.draw()
        prog_bar01.draw()
        prog_bar02.draw()
        marker_0perc.draw()
        marker_25perc.draw()
        marker_50perc.draw()
        marker_75perc.draw()
        marker_100perc.draw()
        win.flip()
        # keys required to continue
        startResp = None
        while startResp == None:
            spaceKey = event.waitKeys()
            for thisKey in spaceKey:
                if thisKey == 'space':
                    startResp = 10
                elif thisKey in ['escape']:
                    core.quit()
            event.clearEvents()
        # making the fixation before the next targets are presented
        if fixuse == 1:
            fixcross.draw()
        if fixuse == 2:
            fixball1.draw()
            fixball2.draw()
            fixball3.draw()
            fixball4.draw()
        win.flip()
        core.wait(0.5)
    # break 3/4
    elif brk_count == (min_sumtrials * 0.75):
        # 3/4 text
        starttext = visual.TextStim(win,
                                    text="Sie haben nun ungefähr drei Viertel der Übung geschafft. Sie können sich daher eine kleine Pause nehmen.\n Drücken Sie die Leertaste, um wieder mit der Aufgabe fortzufahren!",
                                    pos=[0, 3])
        # 3/4 progress bar
        prog_bar01 = visual.Rect(win, fillColor=[0.4, 0.3, 0.6], lineColor=[0, 0, 0], width=16, height=1.5, pos=[0, -3])
        prog_bar02 = visual.Rect(win, fillColor=[0.1, 0.35, 0.2], lineColor=[0, 0, 0], width=12, height=1.5,
                                 pos=[-2, -3])
        marker_0perc = visual.TextStim(win, text="0%", pos=[-8, -4.5])
        marker_25perc = visual.TextStim(win, text="25%", pos=[-4, -4.5])
        marker_50perc = visual.TextStim(win, text="50%", pos=[0, -4.5])
        marker_75perc = visual.TextStim(win, text="75%", pos=[4, -4.5])
        marker_100perc = visual.TextStim(win, text="100% geschafft!", pos=[10.5, -4.5])
        # 3/4 put on screen
        starttext.draw()
        prog_bar01.draw()
        prog_bar02.draw()
        marker_0perc.draw()
        marker_25perc.draw()
        marker_50perc.draw()
        marker_75perc.draw()
        marker_100perc.draw()
        win.flip()
        # keys required to continue
        startResp = None
        while startResp == None:
            spaceKey = event.waitKeys()
            for thisKey in spaceKey:
                if thisKey == 'space':
                    startResp = 10
                elif thisKey in ['escape']:
                    core.quit()
            event.clearEvents()
        # making the fixation before the next targets are presented
        if fixuse == 1:
            fixcross.draw()
        if fixuse == 2:
            fixball1.draw()
            fixball2.draw()
            fixball3.draw()
            fixball4.draw()
        win.flip()
        core.wait(0.5)

    # if the number of trials for the reversals needed exeed the predefined maximum number of trials
    # ==> reset all the flanker counter
    if brk_count == min_sumtrials:
        pr_up = 0
        pr_ri = 0
        pr_do = 0
        pr_le = 0
        pt_up = 0
        pt_ri = 0
        pt_do = 0
        pt_le = 0
        or_up = 0
        or_ri = 0
        or_do = 0
        or_le = 0
        ot_up = 0
        ot_ri = 0
        ot_do = 0
        ot_le = 0
        pe_up = 0
        pe_ri = 0
        pe_do = 0
        pe_le = 0
        oe_up = 0
        oe_ri = 0
        oe_do = 0
        oe_le = 0

    brk_count = brk_count + 1

    # stuff to define the target
    randlan = random.random()
    maxlan = trialn / 4
    maxeas = eastrn / 4

    # no flanker condition (== easy trials)
    if thisCondition['label'] == 'fixation':
        if random.random() <= 0.5:
            fixcross.setOri(6.5)
        else:
            fixcross.setOri(353.5)
        rotation_check = 1
        # get randomly a target in the PRL or oppPRL
        if random.random() <= 0.5:
            x_t = x_sc + x_p
            y_t = y_sc + y_p
        else:
            x_t = x_sc + x_o
            y_t = y_sc + y_o
        target.setPos([x_t, y_t])
        # get a random landolt opening
        if (randlan <= 0.25 and pe_up < maxeas) or (pe_ri == maxeas and pe_do == maxeas and pe_le == maxeas):
            target.setImage(land_up)
            pe_up = pe_up + 1
        elif (randlan <= 0.5 and pe_ri < maxeas) or (pe_do == maxeas and pe_le == maxeas):
            target.setImage(land_ri)
            pe_ri = pe_ri + 1
        elif (randlan <= 0.75 and pe_do < maxeas) or (pe_le == maxeas):
            target.setImage(land_do)
            pe_do = pe_do + 1
        else:
            target.setImage(land_le)
            pe_le = pe_le + 1
    elif thisCondition['label'] == 'peastr':
        x_t = x_sc + x_p
        y_t = y_sc + y_p
        target.setPos([x_t, y_t])
        # get a random landolt opening
        if (randlan <= 0.25 and pe_up < maxeas) or (pe_ri == maxeas and pe_do == maxeas and pe_le == maxeas):
            target.setImage(land_up)
            pe_up = pe_up + 1
        elif (randlan <= 0.5 and pe_ri < maxeas) or (pe_do == maxeas and pe_le == maxeas):
            target.setImage(land_ri)
            pe_ri = pe_ri + 1
        elif (randlan <= 0.75 and pe_do < maxeas) or (pe_le == maxeas):
            target.setImage(land_do)
            pe_do = pe_do + 1
        else:
            target.setImage(land_le)
            pe_le = pe_le + 1
    elif thisCondition['label'] == 'oeastr':
        x_t = x_sc + x_o
        y_t = y_sc + y_o
        target.setPos([x_t, y_t])
        # get a random landolt opening
        if (randlan <= 0.25 and oe_up < maxeas) or (oe_ri == maxeas and oe_do == maxeas and oe_le == maxeas):
            target.setImage(land_up)
            oe_up = oe_up + 1
        elif (randlan <= 0.5 and oe_ri < maxeas) or (oe_do == maxeas and oe_le == maxeas):
            target.setImage(land_ri)
            oe_ri = oe_ri + 1
        elif (randlan <= 0.75 and oe_do < maxeas) or (oe_le == maxeas):
            target.setImage(land_do)
            oe_do = oe_do + 1
        else:
            target.setImage(land_le)
            oe_le = oe_le + 1
    # define the flanker trials conditions
    elif thisCondition['label'] == 'prlrad':
        # define the target position in the PRL
        x_t = x_sc + x_p
        y_t = y_sc + y_p
        target.setPos([x_t, y_t])
        ##
        # gets the current distance
        pt_check = np.sin(np.arctan(x_p / y_p)) * thisIncrement
        # tests if target and flanker overlap and if that's the case handle appropiately
        if pt_check <= stisi[0]:
            # position of the tangential flanker1
            x_fl1 = x_t - np.sin(np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            y_fl1 = y_t - np.cos(np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            # position of the tangential flanker2
            x_fl2 = x_t + np.sin(np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            y_fl2 = y_t + np.cos(np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            # draw both flankers
            flanker1.setPos([x_fl1, y_fl1])
            flanker2.setPos([x_fl2, y_fl2])
            # remember the overlap
            overlap_ch = 1
        ##
        # non-overlapping case
        else:
            # position of the tangential flanker1
            x_fl1 = x_t - np.sin(np.arctan(x_p / y_p)) * thisIncrement
            y_fl1 = y_t - np.cos(np.arctan(x_p / y_p)) * thisIncrement
            # position of the tangential flanker2
            x_fl2 = x_t + np.sin(np.arctan(x_p / y_p)) * thisIncrement
            y_fl2 = y_t + np.cos(np.arctan(x_p / y_p)) * thisIncrement
            # draw both flankers
            flanker1.setPos([x_fl1, y_fl1])
            flanker2.setPos([x_fl2, y_fl2])
        ##
        # get a random landolt opening
        if (randlan <= 0.25 and pt_up < maxlan) or (pt_ri == maxlan and pt_do == maxlan and pt_le == maxlan):
            target.setImage(land_up)
            pt_up = pt_up + 1
        elif (randlan <= 0.5 and pt_ri < maxlan) or (pt_do == maxlan and pt_le == maxlan):
            target.setImage(land_ri)
            pt_ri = pt_ri + 1
        elif (randlan <= 0.75 and pt_do < maxlan) or (pt_le == maxlan):
            target.setImage(land_do)
            pt_do = pt_do + 1
        else:
            target.setImage(land_le)
            pt_le = pt_le + 1
    elif thisCondition['label'] == 'prltan':
        # define the target position in the PRL
        x_t = x_sc + x_p
        y_t = y_sc + y_p
        target.setPos([x_t, y_t])
        ##
        # gets the current distance
        pt_check = np.sin(np.arctan(x_p / y_p)) * thisIncrement
        # tests if target and flanker overlap and if that's the case handle appropiately
        if pt_check <= stisi[0]:
            # position of the tangential flanker1
            x_fl1 = x_t - np.sin(np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            y_fl1 = y_t + np.cos(np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            # position of the tangential flanker2
            x_fl2 = x_t + np.sin(np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            y_fl2 = y_t - np.cos(np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            # draw both flankers
            flanker1.setPos([x_fl1, y_fl1])
            flanker2.setPos([x_fl2, y_fl2])
            # remember the overlap
            overlap_ch = 1
        ##
        # non-overlapping case
        else:
            # position of the radial flanker1
            x_fl1 = x_t - np.sin(np.arctan(y_p / x_p)) * thisIncrement
            y_fl1 = y_t + np.cos(np.arctan(y_p / x_p)) * thisIncrement
            flanker1.setPos([x_fl1, y_fl1])
            # position of the radial flanker2
            x_fl2 = x_t + np.sin(np.arctan(y_p / x_p)) * thisIncrement
            y_fl2 = y_t - np.cos(np.arctan(y_p / x_p)) * thisIncrement
            flanker2.setPos([x_fl2, y_fl2])
        # get a random landolt opening
        if (randlan <= 0.25 and pr_up < maxlan) or (pr_ri == maxlan and pr_do == maxlan and pr_le == maxlan):
            target.setImage(land_up)
            pr_up = pr_up + 1
        elif (randlan <= 0.5 and pr_ri < maxlan) or (pr_do == maxlan and pr_le == maxlan):
            target.setImage(land_ri)
            pr_ri = pr_ri + 1
        elif (randlan <= 0.75 and pr_do < maxlan) or (pr_le == maxlan):
            target.setImage(land_do)
            pr_do = pr_do + 1
        else:
            target.setImage(land_le)
            pr_le = pr_le + 1
    elif thisCondition['label'] == 'opprad':
        # define the target position in the oppPRL
        x_t = x_sc + x_o
        y_t = y_sc + y_o
        target.setPos([x_t, y_t])
        ##
        # gets the current distance
        pt_check = np.sin(np.arctan(x_p / y_p)) * thisIncrement
        # tests if target and flanker overlap and if that's the case handle appropiately
        if pt_check <= stisi[0]:
            # position of the tangential flanker1
            x_fl1 = x_t - np.sin(math.pi / 2 - np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            y_fl1 = y_t + np.cos(math.pi / 2 - np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            # position of the tangential flanker2
            x_fl2 = x_t + np.sin(math.pi / 2 - np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            y_fl2 = y_t - np.cos(math.pi / 2 - np.arctan(y_p / x_p)) * (thisIncrement - 0.1)
            # draw both flankers
            flanker1.setPos([x_fl1, y_fl1])
            flanker2.setPos([x_fl2, y_fl2])
            # remember the overlap
            overlap_ch = 1
        ##
        # non-overlapping case
        else:
            # position of the tangential flanker1
            x_fl1 = x_t - np.sin(math.pi / 2 - np.arctan(y_p / x_p)) * thisIncrement
            y_fl1 = y_t + np.cos(math.pi / 2 - np.arctan(y_p / x_p)) * thisIncrement
            flanker1.setPos([x_fl1, y_fl1])
            # position of the tangential flanker2
            x_fl2 = x_t + np.sin(math.pi / 2 - np.arctan(y_p / x_p)) * thisIncrement
            y_fl2 = y_t - np.cos(math.pi / 2 - np.arctan(y_p / x_p)) * thisIncrement
            flanker2.setPos([x_fl2, y_fl2])
        # get a random landolt opening
        if (randlan <= 0.25 and ot_up < maxlan) or (ot_ri == maxlan and ot_do == maxlan and ot_le == maxlan):
            target.setImage(land_up)
            ot_up = ot_up + 1
        elif (randlan <= 0.5 and ot_ri < maxlan) or (ot_do == maxlan and ot_le == maxlan):
            target.setImage(land_ri)
            ot_ri = ot_ri + 1
        elif (randlan <= 0.75 and ot_do < maxlan) or (ot_le == maxlan):
            target.setImage(land_do)
            ot_do = ot_do + 1
        else:
            target.setImage(land_le)
            ot_le = ot_le + 1
    elif thisCondition['label'] == 'opptan':
        # define the target position in the oppPRL
        x_t = x_sc + x_o
        y_t = y_sc + y_o
        target.setPos([x_t, y_t])
        ##
        # gets the current distance
        pt_check = np.sin(np.arctan(x_p / y_p)) * thisIncrement
        # tests if target and flanker overlap and if that's the case handle appropiately
        if pt_check <= stisi[0]:
            # position of the tangential flanker1
            x_fl1 = x_t - np.sin(math.pi / 2 - np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            y_fl1 = y_t - np.cos(math.pi / 2 - np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            # position of the tangential flanker2
            x_fl2 = x_t + np.sin(math.pi / 2 - np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            y_fl2 = y_t + np.cos(math.pi / 2 - np.arctan(x_p / y_p)) * (thisIncrement - 0.1)
            # draw both flankers
            flanker1.setPos([x_fl1, y_fl1])
            flanker2.setPos([x_fl2, y_fl2])
            # remember the overlap
            overlap_ch = 1
        ##
        # non-overlapping case
        else:
            # position of the radial flanker1
            x_fl1 = x_t - np.sin(math.pi / 2 - np.arctan(x_p / y_p)) * thisIncrement
            y_fl1 = y_t - np.cos(math.pi / 2 - np.arctan(x_p / y_p)) * thisIncrement
            flanker1.setPos([x_fl1, y_fl1])
            # position of the radial flanker2
            x_fl2 = x_t + np.sin(math.pi / 2 - np.arctan(x_p / y_p)) * thisIncrement
            y_fl2 = y_t + np.cos(math.pi / 2 - np.arctan(x_p / y_p)) * thisIncrement
            flanker2.setPos([x_fl2, y_fl2])
        # get a random landolt opening
        if (randlan <= 0.25 and or_up < maxlan) or (or_ri == maxlan and or_do == maxlan and or_le == maxlan):
            target.setImage(land_up)
            or_up = or_up + 1
        elif (randlan <= 0.5 and or_ri < maxlan) or (or_do == maxlan and or_le == maxlan):
            target.setImage(land_ri)
            or_ri = or_ri + 1
        elif (randlan <= 0.75 and or_do < maxlan) or (or_le == maxlan):
            target.setImage(land_do)
            or_do = or_do + 1
        else:
            target.setImage(land_le)
            or_le = or_le + 1

    target.draw()
    if thisCondition['label'] == 'prltan' or thisCondition['label'] == 'prlrad' or thisCondition['label'] == 'opptan' or \
            thisCondition['label'] == 'opprad':
        flanker1.draw()
        flanker2.draw()
    # gets the right fixation
    if fixuse == 1:
        fixcross.draw()
    elif fixuse == 2:
        fixball1.draw()
        fixball2.draw()
        fixball3.draw()
        fixball4.draw()

    # shows the stimuli
    win.flip()
    core.wait(prestime)
    rt_start = core.Clock()
    # let's remove the shit
    if fixuse == 1:
        fixcross.draw()
    elif fixuse == 2:
        fixball1.draw()
        fixball2.draw()
        fixball3.draw()
        fixball4.draw()

    win.flip()

    # get the right response
    thisResp = None
    while thisResp == None:
        allKeys = event.waitKeys(keyList=['escape', 'up', 'down', 'left', 'right', 'space'])
        for thisKey in allKeys:
            if thisKey == 'space':
                fixation_pr = 'space'
            else:
                fixation_pr = '-'
            if overlap_ch == 1:
                if target.image == land_do:
                    if thisKey == 'down':
                        thisResp = 1  # correct
                    elif thisKey == 'up' or 'left' or 'right':
                        thisResp = -1
                    rt_end = core.Clock()
                elif target.image == land_up:
                    if thisKey == 'up':
                        thisResp = 1
                    elif thisKey == 'down' or 'left' or 'right':
                        thisResp = -1
                    rt_end = core.Clock()
                elif target.image == land_le:
                    if thisKey == 'left':
                        thisResp = 1
                    elif thisKey == 'up' or 'down' or 'right':
                        thisResp = -1
                    rt_end = core.Clock()
                elif target.image == land_ri:
                    if thisKey == 'right':
                        thisResp = 1
                    elif thisKey == 'up' or 'down' or 'left':
                        thisResp = -1
                    rt_end = core.Clock()
            else:
                if target.image == land_do:
                    if thisKey == 'down':
                        thisResp = 1  # correct
                    elif thisKey == 'up' or 'left' or 'right':
                        thisResp = -1
                    rt_end = core.Clock()
                elif target.image == land_up:
                    if thisKey == 'up':
                        thisResp = 1
                    elif thisKey == 'down' or 'left' or 'right':
                        thisResp = -1
                    rt_end = core.Clock()
                elif target.image == land_le:
                    if thisKey == 'left':
                        thisResp = 1
                    elif thisKey == 'up' or 'down' or 'right':
                        thisResp = -1
                    rt_end = core.Clock()
                elif target.image == land_ri:
                    if thisKey == 'right':
                        thisResp = 1
                    elif thisKey == 'up' or 'down' or 'left':
                        thisResp = -1
                    rt_end = core.Clock()
        if thisKey in ['escape']:
            core.quit()  # abort experiment

    # add the data to the staircase so it can calculate the next level
    stairs.addData(thisResp)

    # getting the data for the data file
    condition_data = str(thisCondition["label"])

    if target.image == land_do:
        landolt_opening = str("land_down")
    elif target.image == land_ri:
        landolt_opening = str("land_right")
    elif target.image == land_le:
        landolt_opening = str("land_left")
    elif target.image == land_up:
        landolt_opening = str("land_up")

    reaction_time = rt_start.getTime() - rt_end.getTime()

    # write the current step in a data file
    dataFile.write('%s,%s,%.2f,%i,%.3f,%s\n' % (
    condition_data, landolt_opening, thisIncrement, thisResp, reaction_time, fixation_pr))

    # values for the feedback

    if thisCondition['label'] == 'prltan':
        prltan_fb = thisIncrement
    elif thisCondition['label'] == 'prlrad':
        prlrad_fb = thisIncrement
    elif thisCondition['label'] == 'opptan':
        opptan_fb = thisIncrement
    elif thisCondition['label'] == 'opprad':
        opprad_fb = thisIncrement

    core.wait(0.1)

    if rotation_check == 1:
        fixcross.setOri(0)
        rotation_check = 0

    fixcross.draw()

    win.flip()

    # wait 500ms after keypress till the next stimulus trial starts
    core.wait(0.5)

stairs.saveAsExcel('responses_' + currentDate)
dataFile.close()

"""End screen"""

# scaling of the bar
bsc = 1.5

# initialize and draw the end text on the screen
endtext = visual.TextStim(win, pos=[0, 5],
                          text="Sie haben die heutige Übungseinheit absolviert. Drücken sie die Leertaste, um die Einheit zu beenden")
endtext.draw()
# initialize and draw the feedback bar(s)
bar01 = visual.Rect(win, fillColor=[1, 0, 0], lineColor=[1, 0, 0], width=bsc, height=bsc, pos=[4.5 * bsc, -2])
bar02 = visual.Rect(win, fillColor=[1, 0.20, 0], lineColor=[1, 0.20, 0], width=bsc, height=bsc, pos=[3.5 * bsc, -2])
bar03 = visual.Rect(win, fillColor=[1, 0.41, 0], lineColor=[1, 0.41, 0], width=bsc, height=bsc, pos=[2.5 * bsc, -2])
bar04 = visual.Rect(win, fillColor=[1, 0.62, 0], lineColor=[1, 0.62, 0], width=bsc, height=bsc, pos=[1.5 * bsc, -2])
bar05 = visual.Rect(win, fillColor=[1, 0.83, 0], lineColor=[1, 0.83, 0], width=bsc, height=bsc, pos=[0.5 * bsc, -2])
bar06 = visual.Rect(win, fillColor=[0.97, 1, 0], lineColor=[0.97, 1, 0], width=bsc, height=bsc, pos=[-0.5 * bsc, -2])
bar07 = visual.Rect(win, fillColor=[0.76, 1, 0], lineColor=[0.76, 1, 0], width=bsc, height=bsc, pos=[-1.5 * bsc, -2])
bar08 = visual.Rect(win, fillColor=[0.55, 1, 0], lineColor=[0.55, 1, 0], width=bsc, height=bsc, pos=[-2.5 * bsc, -2])
bar09 = visual.Rect(win, fillColor=[0.34, 1, 0], lineColor=[0.34, 1, 0], width=bsc, height=bsc, pos=[-3.5 * bsc, -2])
bar10 = visual.Rect(win, fillColor=[0, 1, 0], lineColor=[0, 1, 0], width=bsc, height=bsc, pos=[-4.5 * bsc, -2])
bar01.draw()
bar02.draw()
bar03.draw()
bar04.draw()
bar05.draw()
bar06.draw()
bar07.draw()
bar08.draw()
bar09.draw()
bar10.draw()
# initialize and draw the feedback scaling
scale_sta = visual.TextStim(win, pos=[-4.5 * bsc, -bsc - 2], text="0 deg")
scale_end = visual.TextStim(win, pos=[4.5 * bsc, -bsc - 2], text="10 deg")
scale_sta.draw()
scale_end.draw()

# initialize and draw the feedback circle
circ_fb = visual.Circle(win, fillColor=None, lineColor=[0, 0, 0], radius=(bsc / 2))
val_fb = (prltan_fb + prlrad_fb + opptan_fb + opprad_fb) / 4
pos_fb = val_fb - (4 * bsc)
circ_fb.setPos([pos_fb, -2])
circ_fb.draw()
# get the comparison value for the feedback text and write the new value inside the .csv-file
with open(comp_file, "r+") as f:
    val_comp = f.read()
    f.seek(0)  # look for position 0
    f.write(str(val_fb))  # write the current feedback value into the file
    f.truncate()  # delete everything after that
val_comp = float(val_comp)
# initialize and draw the feedback text
txtfb = "Ihr Abstand zwischen dem Zielreiz und den beiden äußeren Kreisen hat sich\n von %.2f auf %.2f Grad Sehwinkel geändert" % (
val_comp, val_fb)
text_fb = visual.TextStim(win, pos=[0, -bsc - 6], text=txtfb)
text_fb.draw()

win.flip()

# pressing spacebar will end the experiment
startResp = None
while startResp == None:
    spaceKey = event.waitKeys()
    for thisKey in spaceKey:
        if thisKey in ['space', 'escape']:
            core.quit()

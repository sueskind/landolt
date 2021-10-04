import datetime as dt
import os
import random
from os.path import join

import numpy as np
from psychopy import core, monitors, visual, event, data, gui, sound

import settings
import texts
from constants import Labels, landolt_openings
from paths import landolt_files, RESULTS_DIR, RESULT_DATA_FILE_FMT, RESULT_RESPONSES_FILE_FMT, RESULT_META_FILE_FMT, \
    FEEDBACK_FILE_FMT, SOUNDS_CORRECT_DIR, SOUNDS_WRONG_DIR
from settings import opp_position, prl_position


def random_left_right_rotation(degrees):
    rotation_dir = round(random.random()) * 2 - 1
    return (360 + rotation_dir * degrees) % 360


def stimuli_positions(increment, label):
    if label not in [Labels.PRL_RAD, Labels.PRL_TAN, Labels.OPP_RAD, Labels.OPP_TAN]:
        raise ValueError(f"Illegal label '{label}'")

    if label in [Labels.PRL_RAD, Labels.PRL_TAN]:
        target = prl_position
    else:
        target = opp_position

    vector = target / np.linalg.norm(target) * increment
    if label in [Labels.PRL_TAN, Labels.OPP_TAN]:
        rot = np.array([[0, -1], [1, 0]])
        vector = np.dot(rot, vector)

    return target, target + vector, target - vector


def await_key(keys):
    if isinstance(keys, str):
        keys = [keys]
    pressed = event.waitKeys(keyList=["escape"] + keys)
    if "escape" in pressed:
        core.quit()
    return pressed[0]


def show_text(window, text, resume_key=None):
    visual.TextStim(window, text=text, height=settings.text_size).draw()
    window.flip()
    if resume_key is not None:
        await_key(resume_key)


def show_break_screen(window, progress):
    visual.TextStim(window, text=texts.break_texts[progress], pos=(0, 3), height=settings.text_size).draw()

    for x, text in ((-8, "0%"), (-4, "25%"), (0, "50%"), (4, "75%"), (10.5, "100% geschafft!")):
        visual.TextStim(window, text=text, pos=(x, -4.5), height=settings.text_size).draw()

    visual.Rect(window, fillColor=(0.4, 0.3, 0.6), lineColor=(0, 0, 0), width=16, height=1.5, pos=(0, -3)).draw()
    bars = {0.25: (4, -6),
            0.5: (8, -4),
            0.75: (12, -2)}
    width, pos_x = bars[progress]
    visual.Rect(window, fillColor=(0.1, 0.35, 0.2), lineColor=(0, 0, 0), width=width, height=1.5,
                pos=(pos_x, -3)).draw()

    window.flip()
    await_key("space")


def show_feedback_screen(window, old_feedback_value, new_feedback_value):
    visual.TextStim(window, pos=[0, 5], text=texts.end_text, height=settings.text_size).draw()

    size = 1.5
    bars_spec = (([1, 0, 0], [1, 0, 0], [4.5 * size, -2]),
                 ([1, 0.20, 0], [1, 0.20, 0], [3.5 * size, -2]),
                 ([1, 0.41, 0], [1, 0.41, 0], [2.5 * size, -2]),
                 ([1, 0.62, 0], [1, 0.62, 0], [1.5 * size, -2]),
                 ([1, 0.83, 0], [1, 0.83, 0], [0.5 * size, -2]),
                 ([0.97, 1, 0], [0.97, 1, 0], [-0.5 * size, -2]),
                 ([0.76, 1, 0], [0.76, 1, 0], [-1.5 * size, -2]),
                 ([0.55, 1, 0], [0.55, 1, 0], [-2.5 * size, -2]),
                 ([0.34, 1, 0], [0.34, 1, 0], [-3.5 * size, -2]),
                 ([0, 1, 0], [0, 1, 0], [-4.5 * size, -2]))

    for fill_color, line_color, pos in bars_spec:
        visual.Rect(window, fillColor=fill_color, lineColor=line_color, width=size, height=size, pos=pos).draw()

    visual.TextStim(window, pos=[-4.5 * size, -size - 2], text="0 deg", height=settings.text_size).draw()
    visual.TextStim(window, pos=[4.5 * size, -size - 2], text="10 deg", height=settings.text_size).draw()

    position = new_feedback_value - (4 * size)
    visual.Circle(window, fillColor=None, lineColor=[0, 0, 0], radius=(size / 2), pos=[position, -2]).draw()

    if old_feedback_value is not None:
        visual.TextStim(window, pos=(0, -(size + 6)),
                        text=texts.feedback_text_fmt.format(old_feedback_value, new_feedback_value),
                        height=settings.text_size).draw()

    window.flip()
    await_key("space")


def create_stairs():
    labels_trials_reversals = ((Labels.PRL_TAN, settings.trials, settings.reversals),
                               (Labels.PRL_RAD, settings.trials, settings.reversals),
                               (Labels.OPP_TAN, settings.trials, settings.reversals),
                               (Labels.OPP_RAD, settings.trials, settings.reversals),
                               (Labels.PRL_NOFL, settings.trials_easy, None),
                               (Labels.OPP_NOFL, settings.trials_easy, None),
                               (Labels.FIXATION, settings.trials_fixation, None))
    conditions = [{"label": label,
                   "startVal": settings.stairs_start,
                   "minVal": max(settings.stimuli_size),
                   "stepType": "lin",
                   "stepSizes": settings.stairs_step_size,
                   "nUp": 1,
                   "nDown": 2,
                   "nTrials": num_trials,
                   "nReversals": reversals}
                  for label, num_trials, reversals in labels_trials_reversals]

    return data.MultiStairHandler(conditions=conditions, nTrials=0)


def load_old_store_new_feedback_value(feedback_file, datestring, new_feedback_value):
    with open(feedback_file, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip() != ""]
    try:
        old_feedback_value = float(lines[-1].split(",")[1])
    except IndexError:
        old_feedback_value = None

    with open(feedback_file, "a") as f:
        f.write(f"{datestring},{new_feedback_value}\n")

    return old_feedback_value


def main():
    monitor = monitors.Monitor(settings.monitor)

    dialog_info = {"Participant": "000",
                   "X-coordinate PRL": settings.prl_position[0],
                   "Y-coordinate PRL": settings.prl_position[1],
                   "X-coordinate oppPRL": settings.opp_position[0],
                   "Y-coordinate oppPRL": settings.opp_position[1],
                   "Distance from screen": monitor.getDistance()}
    fixed = ["X-coordinate PRL", "Y-coordinate PRL", "X-coordinate oppPRL", "Y-coordinate oppPRL",
             "Distance from screen"]
    dialog = gui.DlgFromDict(dialog_info, title="ZSER Crowding Control", fixed=fixed, sortKeys=False)
    if not dialog.OK:
        core.quit()

    window = visual.Window(size=monitor.getSizePix(), fullscr=True, color=settings.background_color,
                           colorSpace="rgb255",
                           monitor=monitor, winType="pyglet", allowGUI=False, useFBO=True, units="deg")

    participant = str(dialog_info["Participant"])
    datestring = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    participant_dir = join(RESULTS_DIR, participant)
    session_dir = join(participant_dir, datestring)
    feedback_file = join(participant_dir, FEEDBACK_FILE_FMT.format(participant))

    os.makedirs(session_dir, exist_ok=True)
    open(feedback_file, "a").close()

    filename = RESULT_DATA_FILE_FMT.format(participant, datestring)
    data_file = open(join(session_dir, filename), "w")
    data_file.write("condition,landolt_opening,increment,response,reaction_time,fixation_detection\n")

    filename = RESULT_META_FILE_FMT.format(participant, datestring)
    with open(join(session_dir, filename), "w") as f:
        for k, v in vars(settings).items():
            if not k.startswith("__"):
                f.write(f"{k},{v}\n")

        f.write(f"screen_distance,{monitor.getDistance()}\n")
        f.write(f"screen_size,{monitor.getSizePix()}\n")
        f.write(f"screen_width,{monitor.getWidth()}\n")

    sounds = {1: [sound.Sound(join(SOUNDS_CORRECT_DIR, f)) for f in os.listdir(SOUNDS_CORRECT_DIR)],  # correct
              0: [sound.Sound(join(SOUNDS_WRONG_DIR, f)) for f in os.listdir(SOUNDS_WRONG_DIR)]}  # wrong

    for text in texts.intro_texts:
        show_text(window, text, resume_key="space")

    show_text(window, texts.soundcheck_text)

    key_pressed = await_key(["N", "P", "space"])
    while key_pressed != "space":
        if key_pressed == "N":
            random.choice(sounds[0]).play()
        if key_pressed == "P":
            random.choice(sounds[0]).play()
        key_pressed = await_key(["N", "P", "space"])

    target = visual.ImageStim(window, size=settings.stimuli_size, units="deg")
    flanker1 = visual.ImageStim(window, size=settings.stimuli_size, image=landolt_files["full"], units="deg")
    flanker2 = visual.ImageStim(window, size=settings.stimuli_size, image=landolt_files["full"], units="deg")
    fixcross = visual.ShapeStim(window, vertices="cross", size=settings.fixcross_size, units="deg")
    fixcross.setColor((0, 0, 0), colorSpace="rgb255")

    clock = core.Clock()
    stairs = create_stairs()

    fixcross.draw()
    window.flip()
    core.wait(2)

    trials_total = 4 * settings.trials + 2 * settings.trials_easy + settings.trials_fixation
    last_increments = {label: 0 for label in (Labels.PRL_TAN, Labels.PRL_RAD, Labels.OPP_TAN, Labels.OPP_RAD)}

    # main loop start
    for i, (increment, condition) in enumerate(stairs):

        if i == trials_total // 4:
            show_break_screen(window, 0.25)
        elif i == trials_total // 2:
            show_break_screen(window, 0.5)
        elif i == trials_total * 3 // 4:
            show_break_screen(window, 0.75)

        opening = random.choice(landolt_openings)
        target.setImage(landolt_files[opening])

        label = condition["label"]
        if label == Labels.FIXATION:
            target.setPos(random.choice((prl_position, opp_position)))
            fixcross.setOri(random_left_right_rotation(settings.fixcross_rotation))

        elif label == Labels.PRL_NOFL:
            target.setPos(prl_position)

        elif label == Labels.OPP_NOFL:
            target.setPos(opp_position)

        else:
            target_pos, flanker1_pos, flanker2_pos = stimuli_positions(increment, label)
            target.setPos(target_pos)
            flanker1.setPos(flanker1_pos)
            flanker2.setPos(flanker2_pos)
            flanker1.draw()
            flanker2.draw()

        fixcross.draw()
        target.draw()

        # show all stimuli
        window.flip()
        reaction_time_start = clock.getTime()
        core.wait(settings.stimuli_time)

        # only show fixcross again
        fixcross.draw()
        window.flip()

        # wait for response
        key_pressed = await_key(["up", "down", "right", "left", "space"])
        reaction_time = clock.getTime() - reaction_time_start

        fixation_detection = "-"
        if label == Labels.FIXATION:
            if key_pressed == "space":
                fixation_detection = key_pressed
            response = int(key_pressed == "space")
        else:
            response = int(key_pressed == opening)
        stairs.addResponse(response)

        random.choice(sounds[response]).play()

        last_increments[label] = increment

        data_file.write(f"{condition},{opening},{increment},{response},{reaction_time},{fixation_detection}\n")

        core.wait(settings.wait_after_feedback)
        fixcross.setOri(0)
        fixcross.draw()
        window.flip()
        core.wait(0.5)

    data_file.close()
    filename = RESULT_RESPONSES_FILE_FMT.format(participant, datestring)
    stairs.saveAsExcel(join(session_dir, filename))

    new_feedback_value = np.mean(list(last_increments.values()))
    old_feedback_value = load_old_store_new_feedback_value(feedback_file, datestring, new_feedback_value)
    show_feedback_screen(window, old_feedback_value, new_feedback_value)


if __name__ == '__main__':
    main()

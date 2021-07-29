import os
from os.path import join, abspath, dirname

PROJECT_ROOT = abspath(dirname(__file__))
ASSETS_DIR = join(PROJECT_ROOT, "assets")

SOUNDS_DIR = join(ASSETS_DIR, "sounds")
SOUNDS_CORRECT_DIR = join(SOUNDS_DIR, "correct")
SOUNDS_WRONG_DIR = join(SOUNDS_DIR, "wrong")

IMAGES_DIR = join(ASSETS_DIR, "images")
landolt_files = {direction: join(IMAGES_DIR, f"landolt_{direction}.png")
                 for direction in ("up", "down", "left", "right", "full")}

RESULTS_DIR = join(PROJECT_ROOT, "results")
RESULT_DATA_FILE_FMT = "VP_{}_{}_results.csv"  # participant, datetime
RESULT_META_FILE_FMT = "VP_{}_{}_meta.csv"  # participant, datetime
RESULT_RESPONSES_FILE_FMT = "VP_{}_{}_responses"  # participant, datetime
FEEDBACK_FILE_FMT = "VP_{}_feedback.csv"  # participant

# create dirs if not exist
os.makedirs(RESULTS_DIR, exist_ok=True)

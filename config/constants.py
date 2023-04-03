import datetime
import os
import time

# configuration

# realtime config
realtime_delay_second = 3

# whisper
language = "english"
# tiny | base | small | medium
model_type = "small"
if language == "english" or language == "en":
    model_name = model_type + ".en"

# common
pwd = os.getcwd()

# dir
dir_audio_realtime = os.path.join(pwd, r"output\wav\realtime")
dir_audio_live = os.path.join(pwd, r"output\wav\live")
dir_audio_record = os.path.join(pwd, r"output\wav\record")
dir_srt = os.path.join(pwd, r"output\srt")
dir_txt = os.path.join(pwd, r"output\txt")

# path
path_text_list = os.path.join(pwd, r"output\txt\file_list.txt")
path_text_history = os.path.join(pwd, r"output\txt\history.txt")

path_audio_realtime = os.path.join(pwd, r"output\wav\realtime.wav")
path_audio_live = os.path.join(pwd, r"output\wav\live.wav")

path_icon = os.path.join(pwd, r"image\logo.svg")

# type
type_final_realtime = "realtime-"
type_final_live = "live-"
type_record = "record-"
type_realtime = "realtime"
type_live = "live"

# prompt
prompt_realtime = "[ Real time ... ]"
prompt_live = "[ Live ... ]"
prompt_continue = "[ Continue ... ]"
prompt_transcribing = "[ Transcribing ... ]"
prompt_recording = "[ Recording ... ]"
prompt_finished = "[ Finished. ]"
prompt_loading = "[ Model loading ... ]"
prompt_fail_task = "[ Failed: another task is running ... ]"
prompt_fail_begin = "[ Failed: can't begin again ... ]"

# action
action_begin = "begin"
action_realtime = "realtime"
action_live = "live"
action_stop = "stop"
action_record = "record"
action_submit = "submit"

# status
status_ready = "ready"
status_realtime = "realtime"
status_live = "live"
status_transcribe = "transcribe"
status_record = "record"


def get_audio_path(audio_type):
    file_id = datetime.datetime.now().strftime('%Y-%m-%d+%H_%M_%S')
    file_path = ""
    if audio_type == type_realtime:
        file_path = path_audio_realtime
    if audio_type == type_live:
        file_path = path_audio_live
    if audio_type == type_record:
        file_path = os.path.join(dir_audio_record, audio_type + file_id + ".wav")
    if audio_type == type_final_live:
        file_path = os.path.join(dir_audio_live, audio_type + file_id + ".wav")
    if audio_type == type_final_realtime:
        file_path = os.path.join(dir_audio_realtime, audio_type + file_id + ".wav")
    return file_path


def realtime_delay():
    time.sleep(realtime_delay_second)


def create_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def init_dir():
    create_dir(dir_audio_realtime)
    create_dir(dir_audio_live)
    create_dir(dir_audio_record)
    create_dir(dir_srt)
    create_dir(dir_txt)

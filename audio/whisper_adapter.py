import os
import threading
from collections.abc import Iterator

import torch
import whisper
from whisper import utils

from config import constants


class WhisperAdapter:
    def __init__(self):
        self._running = True

    _instance_lock = threading.Lock()

    def load_model(self):
        if not hasattr(self, "_model"):
            with self._instance_lock:
                if not hasattr(self, "_model"):
                    self._model = whisper.load_model(constants.model_name)

    def transcribe(self, file_path: str, need_srt: bool):
        decode_options = dict(task="transcribe", language=constants.language, fp16=torch.cuda.is_available())
        recognize_result = whisper.transcribe(model=self._model, audio=file_path, verbose=False,
                                              condition_on_previous_text=False, no_speech_threshold=0.5,
                                              compression_ratio_threshold=2.2,
                                              **decode_options)
        result = get_text(file_path, recognize_result["segments"], need_srt)
        return result


def get_text(file_path: str, transcript: Iterator[dict], need_srt: bool):
    _, file_full_name = os.path.split(file_path)
    file_id, _ = os.path.splitext(file_full_name)
    txt = ""
    if need_srt:
        path_srt = os.path.join(constants.dir_srt, file_id + ".srt")
        with open(path_srt, "w", encoding="utf-8") as file_object:
            for i, segment in enumerate(transcript, start=1):
                print(
                    f"{utils.format_timestamp(segment['start'], always_include_hours=True, decimal_marker=',')} --> "
                    f"{utils.format_timestamp(segment['end'], always_include_hours=True, decimal_marker=',')}\n"
                    f"{segment['text'].strip().replace('-->', '->')}\n",
                    file=file_object,
                    flush=True,
                )
                txt += segment['text'].strip() + "\n"
    else:
        for i, segment in enumerate(transcript, start=1):
            txt += segment['text'].strip() + "\n"
    update_history(file_id, txt)
    return txt.strip()


def update_history(file_id, txt):
    with open(constants.path_text_history, "a", encoding="utf-8") as file_object:
        file_object.write("\n")
        file_object.write(file_id)
        file_object.write("\n")
        file_object.write(txt)


whisper_obj = WhisperAdapter()

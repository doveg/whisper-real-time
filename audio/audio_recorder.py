import _thread
import wave

import pyaudio

from config import constants


class Recorder:
    def __init__(self, chunk=1024, channels=1, rate=64000):
        self.chunk = chunk
        self.channels = channels
        self.rate = rate
        self.format = pyaudio.paInt16
        self.au = pyaudio.PyAudio()
        self._running = False
        self._frames = []
        self._temp = []
        self._status = constants.status_ready

    def is_running(self):
        return self._running

    def start(self):
        if not self._running:
            _thread.start_new_thread(self.__recording, ())

    def __recording(self):
        self._running = True
        self._frames = []
        self._temp = []
        stream = self.au.open(format=self.format,
                              channels=self.channels,
                              rate=self.rate,
                              input=True,
                              frames_per_buffer=self.chunk)
        while self._running:
            data = stream.read(self.chunk)
            self._frames.append(data)
            self._temp.append(data)

        stream.stop_stream()
        stream.close()

    def stop(self, action_type):
        self._running = False
        self.be_ready(action_type)

    def save_audio(self, filename, audio_type):
        if audio_type == constants.type_realtime or audio_type == constants.type_live:
            self.save(filename, self._temp)
            self._temp = []
        else:
            self.save(filename, self._frames)

    def save(self, filename, data):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.au.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(data))
        wf.close()

    def clear_temp(self):
        self._temp = []

    def check_status(self, action):
        if action == constants.action_begin:
            return self._status == constants.status_ready or self._status == constants.status_realtime
        if action == constants.action_realtime:
            return self._status == constants.status_realtime
        if action == constants.action_live:
            return self._status == constants.status_ready or self._status == constants.status_live
        if action == constants.action_stop:
            return self._status == constants.status_live
        if action == constants.action_record:
            return self._status == constants.status_ready
        if action == constants.action_submit:
            return self._status == constants.status_record

    def is_start(self, action):
        if action == constants.action_live:
            result = self._status == constants.status_ready
            self._status = constants.status_live
            return result
        if action == constants.action_begin:
            if self._status == constants.status_ready:
                self._status = constants.status_realtime
                return True
            else:
                return False

    # def end_transcribe(self, action):
    #     if self._status == constants.status_transcribe and action == constants.action_live:
    #         self._status = constants.status_live

    def be_ready(self, action_type):
        if self._status == constants.status_realtime and action_type == constants.action_realtime:
            self._status = constants.status_ready
        if self._status == constants.status_live and action_type == constants.action_live:
            self._status = constants.status_ready
        if self._status == constants.status_record and action_type == constants.action_record:
            self._status = constants.status_ready


def audio_play_thread(audio_path):
    if audio_path is None:
        print("No item is selected")
        return
    _thread.start_new_thread(play_audio, (audio_path,))


def play_audio(audio_path):
    print("Audio playing")
    au = pyaudio.PyAudio()
    chunk = 1024
    wf = wave.open(audio_path, 'rb')
    stream = au.open(format=au.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                     rate=wf.getframerate(), output=True)
    # file_stats = os.stat(audio_path)
    # progress = tqdm(total=math.ceil(file_stats.st_size / (chunk*2)))
    while True:
        # progress.update(1)
        data = wf.readframes(chunk)
        if data == b'':
            break
        stream.write(data)
    stream.stop_stream()
    stream.close()
    au.terminate()
    print("Audio play finished")


recorder_obj = Recorder()

# -*- coding: utf-8 -*-
from aip import AipSpeech
import wave
from pyaudio import PyAudio,paInt16
import re
import time
from aip import AipNlp

APP_ID1 = '11136502'
API_KEY1 = 'dPeG4ubYHR0mhwjANj5xcn1YZjahStUF'
SECRET_KEY1 = 'BpFVkeP4PMkf2XVHnoaP8yNIe2kujrP7'

APP_ID2 = '11455220'
API_KEY2 = 'MqhL6rfGZS9o4483iAs3hkuf'
SECRET_KEY2 = 'qTsMNBHqGp8xHA3FufmTtGHVAKIvboKl'

client_au = AipSpeech(APP_ID1,API_KEY1,SECRET_KEY1)
client_word = AipNlp(APP_ID2,API_KEY2,SECRET_KEY2)

def get_file(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()

framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=5
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*4:  #控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print '.' 
    save_wave_file('01.pcm',my_buf)
    stream.close()

chunk=2014
def play():
    wf=wave.open(r"01.pcm",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()

if __name__ == '__main__':
  #  my_record()
    print 'Over!'
  #  play()
    t1 = time.time()
    a = str(client_au.asr(get_file('01.pcm'), 'pcm', 16000, {'dev_pid': 1536 }))
 
   # a = str(client_au.asr(get_file('/home/pi/baiduAI/sample/asrDemo2/pcm/0.pcm'), 'pcm', 16000, {'dev_pid': 1536 }))
    print time.time() - t1
    g = re.search(r"[\\].+?[$\']",a)
    if g:
        print g.group()
        p = g.group().decode('unicode_escape').strip("'")
        print p
	q = p.encode('utf-8')
	for i in range(len(client_word.lexer(q)['items'])):       
		print client_word.lexer(q)['items'][i]['item']
    else: 
        print 'something wrong'


#print(client.asr(get_file('/home/dyfdaf/baiduAI/sample/asrDemo2/pcm/0.pcm'),'pcm',16000,{'dev_pid':1536,}))
#print(client.asr(get_file('/home/dyfdaf/zn.wav'),'wav',16000,{'dev_pid':1536,}))

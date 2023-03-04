from sklearn.mixture import GaussianMixture
from playsound import playsound as ps
import python_speech_features as mfcc
from googletrans import Translator
from scipy.io.wavfile import read
from sklearn import preprocessing
import speech_recognition as sr
from gtts import gTTS
import numpy as np
import whisper
import pyaudio
import pickle
import wave
import time
import os


with open("pwd.txt", 'r') as pwd:
    folder_location = pwd.read()

with open(f'{folder_location}database/language.txt', 'r') as data:
    language = data.read()
model = whisper.load_model("base")

curspeaker = ""


def listen():
    global curspeaker
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        gaudio = r.listen(source)
        print("Recognizing...")
    try:
        dt = r.recognize_google(gaudio)
        print(dt)

    except sr.UnknownValueError:
        dt = ""

    except sr.RequestError:
        dt = ""
        print("Request results from Google Speech Recognition service error")
    if dt != "":
        curspeaker = find_user("./recording.wav")
        print(curspeaker)
        if curspeaker != "Crystal":
            result = model.transcribe("./recording.wav")
            recognized_text = result["text"]
            print(f"{curspeaker} said", recognized_text)
            with open(f"{folder_location}database/recognition.txt", 'w') as recognition:
                recognition.write(recognized_text)
            return curspeaker
    return ""


def calculate_delta(array):
   
    rows,cols = array.shape
    print(rows)
    print(cols)
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
              first =0
            else:
              first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas


def extract_features(audio,rate):
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01,20,nfft = 1200, appendEnergy = True)    
    mfcc_feature = preprocessing.scale(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature,delta)) 
    return combined


def record_audio_train():
    Name =(input("Please Enter Your Name:"))
    for count in range(5):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = 10
        device_index = 2
        audio = pyaudio.PyAudio()
        print("----------------------record device list---------------------")
        info = audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
                if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        print("-------------------------------------------------------------")
        index = int(input("Enter the device ID you would like to record with: "))        
        print("recording via index "+str(index))
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index = index,
                        frames_per_buffer=CHUNK)
        print ("recording started")
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        print ("recording stopped")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        OUTPUT_FILENAME=Name+"-sample"+str(count)+".wav"
        WAVE_OUTPUT_FILENAME=os.path.join("training_set",OUTPUT_FILENAME)
        WAVE_OUTPUT_FILENAME=folder_location+"voices/" +WAVE_OUTPUT_FILENAME
        print(WAVE_OUTPUT_FILENAME)
        trainedfilelist = open("training_set_addition.txt", 'a')
        trainedfilelist.write(OUTPUT_FILENAME+"\n")
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()

def record_audio_test():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 40
    audio = pyaudio.PyAudio()
    print("----------------------record device list---------------------")
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
    print("-------------------------------------------------------------")
    index = int(input())        
    print("recording via index "+str(index))
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = index,
                    frames_per_buffer=CHUNK)
    print ("recording started")
    Recordframes = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print ("recording stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    OUTPUT_FILENAME="sample.wav"
    WAVE_OUTPUT_FILENAME=os.path.join("testing_set",OUTPUT_FILENAME)
    WAVE_OUTPUT_FILENAME = folder_location+"voices/"+WAVE_OUTPUT_FILENAME
    # trainedfilelist = open("testing_set_addition.txt", 'a')
    # trainedfilelist.write(OUTPUT_FILENAME+"\n")
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()

def train_model():
    source = folder_location+"voices/"+"training_set/"   
    dest = folder_location+"voices/"+"trained_models/"
    train_file = folder_location+"voices/"+"training_set_addition.txt"        
    file_paths = open(train_file,'r')
    print(file_paths)
    count = 1
    features = np.asarray(())
    for path in file_paths:    
        path = path.strip()   
        print(path)

        sr,audio = read(source + path)
        print(sr)
        vector = extract_features(audio,sr)
        
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        if count == 5:    
            gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)
            
            # dumping the trained gaussian model
            picklefile = path.split("-")[0]+".gmm"
            pickle.dump(gmm,open(dest + picklefile,'wb'))
            print('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)   
            features = np.asarray(())
            count = 0
        count = count + 1


def find_user(path):
    modelpath = folder_location+"voices/"+"trained_models/"
     
    gmm_files = [os.path.join(modelpath,fname) for fname in
                  os.listdir(modelpath) if fname.endswith('.gmm')]
     
    #Load the Gaussian gender Models
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                  in gmm_files]
     
    # Read the test directory and get the list of test audio files 
    path = path.strip()
    sr,audio = read(path)
    vector   = extract_features(audio,sr)
        
    log_likelihood = np.zeros(len(models)) 
    
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        
    winner = np.argmax(log_likelihood)
    return speakers[winner]


def speak(text):
    text = reverse_translate(text)
    tts = gTTS(text, lang=language)
    print(text)
    tts.save(f'{folder_location}audio.mp3')
    ps(f'{folder_location}audio.mp3')
    time.sleep(4)
    with open(f"{folder_location}database/recognition.txt", 'w') as recognition:
        recognition.write('')


def translate(text):
    translator = Translator()
    translate_text = translator.translate(text, src=language, dest='en').text
    return translate_text


def reverse_translate(text):
    translator = Translator()
    translate_text = translator.translate(text, src='en', dest=language).text
    return translate_text

import speech_recognition as sr
import os
from playsound import playsound
import webbrowser
import random


speech = sr.Recognizer()

greeting_dict = {'hello': 'hello', 'hi': 'hi'}
open_launch_dict = {'open': 'open', 'launch': 'launch'}
google_searches_dict = {'what': 'what', 'which': 'which', 'when': 'when', 'where': 'where', 'search': 'search',
                        'who': 'who', 'whom': 'whom', 'whose': 'whose', 'why': 'why', 'whether': 'whether', 'youtube': 'youtube'}
social_media_dict = {'facebook': 'https://www.facebook.com/', 'instagram': 'https://www.instagram.com/',
                     'twitter': 'https://twitter.com/explore', ' whatsapp': 'https://www.whatsapp.com/'}

mp3_thankyou_list =['MP3\welcome.mp3']
mp3_listening_problem_list = ['MP3\pardon.mp3', 'MP3\sorry.mp3']
mp3_struggling_list = ['MP3\samaj.mp3', 'MP3\struggle.mp3']
mp3_google_search = ['MP3\here.mp3', 'MP3\search.mp3']
mp3_greeting_list = ['MP3\hope.mp3', 'MP3\how.mp3']
mp3_open_launch_list = ['MP3\open.mp3', 'MP3\launch.mp3']
mp3_bye = ['MP3\goodb.mp3', 'MP3\ciao.mp3',]

error_occurrence = 0

def is_valid_google_search(phrase):
    if (google_searches_dict.get(phrase.split(' ')[0]) == phrase.split(' ')[0]):
        return True


def play_sound(mp3_list):
    mp3 = random.choice(mp3_list)
    playsound(mp3)


def read_voice_cmd():
    voice_text = ''
    print('Listening...')

    global error_occurrence

    try:
        with sr.Microphone() as source:
            audio = speech.listen(source=source, timeout=10, phrase_time_limit=5)
        voice_text = speech.recognize_google(audio)
    except sr.UnknownValueError:

        if error_occurrence==0:
            play_sound(mp3_listening_problem_list)
            error_occurrence+=1
        elif error_occurrence==1:
            play_sound(mp3_struggling_list)
            error_occurrence+=1

    except sr.RequestError as e:
        print('Network error')
    except sr.WaitTimeoutError:

        if error_occurrence == 0:
            play_sound(mp3_listening_problem_list)
            error_occurrence += 1
        elif error_occurrence == 1:
            play_sound(mp3_struggling_list)
            error_occurrence += 1

    return voice_text


def is_valid_note(greet_dict, voice_note):
    for key, value in greet_dict.items():
        # 'Hello edith'
        try:

            if value == voice_note.split(' ')[0]:
                return True
                break
            elif key == voice_note.split(' ')[1]:
                return True
                break
        except IndexError:
            pass

    return False


if __name__ == '__main__':

    playsound('MP3\hello2.mp3')

    while True:

        voice_note = read_voice_cmd().lower()
        print('cmd : {}'.format(voice_note))

        if is_valid_note(greeting_dict, voice_note):
            print('In greeting...')
            play_sound(mp3_greeting_list)
            continue
        elif is_valid_note(open_launch_dict, voice_note):
            print('In open...')
            play_sound(mp3_open_launch_list)
            if (is_valid_note(social_media_dict, voice_note)):
                # Launch Facebook
                key = voice_note.split(' ')[1]
                webbrowser.open(social_media_dict.get(key))
            else:
                os.system('explorer C:\\{}'.format(voice_note.replace('open ', '').replace('launch ', '')))
                print('explorer C:\\{}'.format(voice_note.replace('open ', '').replace('launch ', '')))


                os.system('explorer D:\\{}'.format(voice_note.replace('open', '').replace('launch', '')))
                print('explorer D:\\{}'.format(voice_note.replace('open', '').replace('launch', '')))
            continue
        elif is_valid_google_search(voice_note):
            print('searching..')
            play_sound(mp3_google_search)
            webbrowser.open('https://www.google.co.in/search?q={}'.format(voice_note))
            continue
        elif 'thanks' in voice_note:
            print('Thanks boss...')
            play_sound(mp3_thankyou_list)
            continue

        elif 'bye' in voice_note:
            print('Good bye...')
            play_sound(mp3_bye)
            exit()

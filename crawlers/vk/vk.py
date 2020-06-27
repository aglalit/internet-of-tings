import os
import sys
import json
import locale

import utils
import vkapi
import config

locale.setlocale(locale.LC_ALL, "")
PATH = os.environ['PATH']

def autorizations():
    try:
        login = os.environ['VK_LOGIN']
        password = os.environ['VK_PASSWORD']

        isProxyOauth = utils.get_proxy_host(False, False)
        isProxyAPI = utils.get_proxy_host(False)

        r = vkapi.autorization(login, password)

        if (r == "Error: 2fa isn't supported"):
            print('sms')
            code = input('Enter the code from SMS: ')

            r = vkapi.autorization(login, password, isProxyOauth, str(code))

        resp = json.loads(json.dumps(r))

        if (resp.get('access_token') != None):

            access_token = resp['access_token']

            getRefreshToken = vkapi.refreshToken(access_token, isProxyAPI)
            refresh_token = getRefreshToken["response"]["token"]

            DATA = {'access_token': access_token, 'token': refresh_token}
            utils.save_json("DATA", DATA)

        else:
            print('Login failed :(')

    except vkapi.VKException as ex:
        print(str(ex))

    except Exception as e:
        print('Login failed')
        print(str(e))


def LoadsListMusic():
    try:
        with open('DATA', encoding='utf-8') as data_json:
            data_token = json.loads(data_json.read())

        access_token = data_token["access_token"]
        refresh_token = data_token["token"]

        isProxyAPI = utils.get_proxy_host(False)

        data = vkapi.get_audio(refresh_token, isProxyAPI)

        if (config.SaveToFile):
            utils.save_json('response.json', data)

        count_track = data['response']['count']
        i = 0

        for count in data['response']['items']:

            line = count['artist'] + ' — ' + count['title']
            print(line)
            # test.setText(0, str(i + 1))
            # test.setText(1, count['artist'])
            # test.setText(2, count['title'])
            # test.setText(3, utils.time_duration(count['duration']))
            # test.setText(4, utils.unix_time_stamp_convert(count['date']))

            # if ('is_hq' in count and 'is_explicit' in count):
            #     test.setText(5, "HQ (E)")
            #
            # elif 'is_hq' in count:
            #     test.setText(5, "HQ")
            #
            # elif 'is_explicit' in count:
            #     test.setText(5, "E")
            #
            # if (count['url'] == ""):
            #     test.setText(6, "Недоступно")

            i += 1

        # self.label.setText("Всего аудиозаписей: " + str(count_track) + " Выбрано: " + str(0) + " Загружено: " + str(0))
        is_loaded = True

    except vkapi.VKException as ex:
        print(str(ex))

    except Exception as e:
        print(str(e))

def run():
        try:
            if (config.SaveToFile):
                if (utils.file_exists('response.json')):
                    with open('response.json', encoding='utf-8') as data_json:
                        data = json.loads(data_json.read())
                else:
                    raise Exception("File \"response.json\" not found")

            for item in data['response']['items']:

                artist = item['artist']
                title = item['title']
                song_name = artist + " - " + title

                filename = PATH + "/downloads/" + utils.remove_symbols(song_name) + ".mp3"
                url = item['url']

                if (item['url'] == ""):

                    if (item['content_restricted']):
                            if item['content_restricted'] == 1:
                               print("Аудиозапись: " + song_name + " недоступна по решению правообладателя")
                            elif item['content_restricted'] == 2:
                                print("Аудиозапись: " + song_name + " недоступна в вашем регионе по решению правообладателя")
                            elif item['content_restricted'] == 5:
                                print("Доступ к аудиозаписи: " + song_name + " скоро будет открыт")
                    else:
                        print("Аудиозапись: " + song_name + " недоступна в вашем регионе")

                else:
                    utils.downloads_files_in_wget(url, filename)

        except Exception as e:
            print(str(e))

run()
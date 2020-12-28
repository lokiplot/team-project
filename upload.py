import vk
import datetime
import time
import random
import math
import requests
import json

our_group_id = 200698416
token = "65e6efa565e6efa565e6efa54f6593fb1f665e665e6efa53a5c6937a4636b3416a8bd92"
group_token = "17e681fbe171945431a04f1abc752d41ff888698288abf74124de4e782c67f36e76484601991870f56b7a"
analyse_group_id = 'memkn'
new_token = "812c2975fc2ac0785252d97e8b5011f45e873a00dfb98b15299aec060ff7b890d06c4822feab0626e198c"
session1 = vk.AuthSession(access_token=new_token)
vk_api = vk.API(session1, v=5.92)
album_id = 278041850
month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
version = '5.95'


def upload_picture(picture_path):
    r = vk_api.photos.getUploadServer(group_id=our_group_id, album_id=album_id)
    url = r['upload_url']
    file = {'file1': open(picture_path, 'rb')}
    ur = requests.post(url, files=file).json()
    result = requests.get('https://api.vk.com/method/photos.save',
                          params={
                              'access_token': new_token,
                              'album_id': ur['aid'],
                              'group_id': ur['gid'],
                              'server': ur['server'],
                              'photos_list': ur['photos_list'],
                              'hash': ur['hash'],
                              'v': version,
                          }).json()
    return result


upload_picture("21.png")

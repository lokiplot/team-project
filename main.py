import vk
import datetime
import time
import random
import math


class Group:
    """
    we don't really need this now but i suppose it would be useful in the nearest future
    """

    def __init__(self, group_id, freq):
        self.group_id = group_id
        self.begin = datetime.datetime.now()
        self.frequency = freq

    def count_online_proportion(self):
        """
        gets the number of members online, ant the total number of members, not counting those,
        whose info is not is not available
        :param self: the object of the class Group. We need the group id
        :return: two integers - the number of members with available online-information and the number of members online
        """
        amount = 0
        online = 0
        your_group_info = vk_api.groups.getById(group_id=self.group_id, fields='members_count')
        number_of_members = your_group_info[0]['members_count']
        one_more_number_of_members = number_of_members
        already_count = 0
        while already_count < number_of_members:
            group_members_ids = vk_api.groups.getMembers(group_id=self.group_id, offset=already_count, fields='online')
            for x in group_members_ids['items']:
                if 'online' in x:
                    online += x['online']
                else:
                    one_more_number_of_members -= 1
            already_count += 1000
        if one_more_number_of_members == 0:
            return -1, -1
        else:
            return one_more_number_of_members, online


our_group_id = "memkn_funclub"
token = "65e6efa565e6efa565e6efa54f6593fb1f665e665e6efa53a5c6937a4636b3416a8bd92"
group_token = "17e681fbe171945431a04f1abc752d41ff888698288abf74124de4e782c67f36e76484601991870f56b7a"
analyse_group_id = 'memkn'
session1 = vk.AuthSession(access_token=token)
vk_api = vk.API(session1, v=5.92)
album_id = "278041850"
month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def upload_picture(picture_path):
    r = requests.get('https://api.vk.com/method/photos.getUploadServer',
                     params={
                         'access_token': token,
                         'album_id': album_id,
                         'group_id': our_group_id,
                     }).json()
    url = r['response']['upload_url']
    file = {'file1': open(picture_path, 'rb')}
    ur = requests.post(url, files=file).json()
    result = requests.get('https://api.vk.com/method/photos.save',
                          params={
                              'access_token': token,
                              'album_id': ur['aid'],
                              'group_id': ur['gid'],
                              'server': ur['server'],
                              'photos_list': ur['photos_list'],
                              'hash': ur['hash']
                          }).json()
    print(result)

def get_user_last_seen(profile_id):
    """
    shows when user was online
    :param profile_id:
    :return time:
    """
    value = vk_api.users.get(user_ids=profile_id, fields='last_seen')
    if 'last_seen' not in value[0]:
        return None
    online_time = datetime.datetime.fromtimestamp(value[0]['last_seen']['time'])
    return online_time


def get_group_followers(group_page_id, done):
    """
    gets the list of the group members, not more than 1000
    :param group_page_id:
    :param done: shows the indent
    :return list of members' ids:
    """
    value = vk_api.groups.getMembers(group_id=group_page_id, offset=done)
    followers_id = []
    for user in value['items']:
        followers_id.append(user)
    return followers_id


'''
# probably we will not need this one, but who knows...

def get_user_followers(id):
    """
    shows when user was online
    :param id:
    :return time:
    """
    value = vk_api.users.getFollowers(user_id=id)
    followers_id = []
    for user in value['items']:
        followers_id.append(user)
    return followers_id
'''


def approximate_time(real_time):
    """
    gets time user was last seen and adds two minutes
    :param real_time: time user was last seen online
    :return: real_time plus 2 min
    """

    hours = real_time.hour
    days = real_time.day
    months = real_time.month
    years = real_time.year
    # обработка редких случаев
    if years % 4 == 0 and years % 100 != 0 or years % 400 == 0:
        month_length[1] += 1
    if real_time.minute >= 58:
        hours = real_time.hour + 1
    if hours == 24:
        hours = 0
        days += 1
    if days > month_length[months - 1]:
        days = 1
        months += 1
    if months > 12:
        months = 1
        years += 1

    approximate_online_time = real_time.replace(minute=(real_time.minute + 2) % 60,
                                                hour=hours, day=days, month=months, year=years)
    return approximate_online_time


def is_online(online_time):
    # just checks if the user is online or not, returns 0 or 1

    now_time = datetime.datetime.now()
    now_time = now_time.replace(microsecond=0)
    if online_time >= now_time:
        return 1
    else:
        return 0


'''
# it is so long and long-working shit that i don't want to re-write it. I suppose, we have something better

def count_online(id):
    amount = 0
    online = 0
    your_group = vk_api.groups.getById(group_id=id, fields='members_count')
    number_of_them = your_group[0]['members_count']
    if number_of_them <= 10000:
        done = 0
        while done < number_of_them:
            group_members_ids = get_group_followers(id, done)
            for x in group_members_ids:
                last = get_user_last_seen(str(x))
                if last is not None:
                    amount += 1
                    delta_last = delta_time(last)
                    online += is_online(delta_last)
            done += 1000
        if amount == 0:
            return -1
        else:
            return amount, online
    else:
        piece = number_of_them // 100
        for i in range(piece):
            group_members_ids = get_group_followers(id, 100 * i)
            x = random.randint(0, 100)
            last = get_user_last_seen(str(group_members_ids[x]))
            if last is not None:
                amount += 1
                delta_last = approximate_time(last)
                online += is_online(delta_last)
        number_of_them -= piece * 100
        group_members_ids = get_group_followers(id, piece * 100)
        x = random.randint(0, number_of_them - 1)
        last = get_user_last_seen(str(group_members_ids[x]))
        if last is not None:
            amount += 1
            delta_last = approximate_time(last)
            online += is_online(delta_last)
        return amount, online
'''

analyse_group_id = input()
frequency = input()
if frequency == "as frequently as possible":
    frequency_number = 0
elif frequency.isdigit():
    frequency_number = int(frequency)
else:
    print("Error")
    exit()
n = int(input())

group = Group(analyse_group_id, frequency_number)

t0 = time.time()
all_members, online_members = group.count_online_proportion()
percent = online_members / all_members * 100
percent = math.ceil(percent)

# print("In this group i have got information about " + str(all_members) + " users")

# print("Online percent in " + analyse_group_id + " is " + str(percent) + "%")
t0 = time.time() - t0
if t0 >= group.frequency * 60:
    print("Sorry, I can't work so fastly, so I will count statistics as fastly as i can")
    for i in range(n):
        current_time = datetime.datetime.now()

        all_members, online_members = group.count_online_proportion()
        percent = online_members / all_members * 100
        percent = math.ceil(percent)

        print("Time: " + str(current_time) + ". Online percent in " + analyse_group_id + " is " + str(percent) + "%")
        print("____________________________________________________________________________________________________")
else:
    for i in range(n):
        current_time = datetime.datetime.now()
        t0 = time.time()

        all_members, online_members = group.count_online_proportion()
        percent = online_members / all_members * 100
        percent = math.ceil(percent)

        print("Time: " + str(current_time) + ". Online percent in " + analyse_group_id + " is " + str(percent) + "%")
        print("____________________________________________________________________________________________________")
        t0 = time.time() - t0
        time.sleep(group.frequency * 60 - t0)
exit()
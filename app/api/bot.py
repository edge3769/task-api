from app import db
from telegram import Bot
from geopy import distance
from flask.globals import request
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from app.api import bp
from flask import request
from app.user_model import User

bot = Bot('1854496672:AAEB8tdvXSsqG57eb5LyOkNbaIIAvXMQmLo')

commands = [
    {
        'desc': 'Send a location attachment to set a location'
    },
    {
        'name': 'add',
        'desc': """specify a list of comma separated tags to add to your tags
                e.g: /add dog cat 
                will add dog and cat from your tags"""
    },
    {
        'name': 'delete',
        'desc': """specify a list of comma separated tags to delete
                e.g: /delete dog cat 
                will delete dog and cat from your tags"""
    },
    {
        'name': 'users',
        'desc': 'show top users matching your tags'
    },
    {
        'name': 'location',
        'desc': 'show users closest to your set location'
    },
    {
        'name': 'delLocation',
        'desc': "delete your location from the bot. User's won't be able to find you by location"
    },
    {
        'name': 'off',
        'desc': "stop appearing in other user's x369_bot searches"
    },
    {
        'name': 'on',
        'desc': "appear in other user's x369_bot searches. This is the default"
    },
    {
        'name': 'tags',
        'desc': 'list all your tags'
    },
    {
        'name': 'help',
        'desc': 'get a list of all commands'
    }
]

def location_sort(target, query):
    target = (target['latitude'], target['longitude'])
    for user in query:
        if user.location:
            if 'latitude' in user.location and 'longitude' in user.location:
                location = (user.location['latitude'], user.location['longitude'])
                user.distance = distance.distance(target, location).km
        else:
            query = query.filter(User.id != user.id)
    db.session.commit()
    query = query.order_by(User.distance.asc())

def delLocation(user):
    user.location = None
    db.session.commit()
    bot.sendMessage(
        user.id,
        'location deleted'
    )

def location(user, location):
    user.location = {
        'longitude': location['longitude'],
        'latitude': location['latitude']
    }
    db.session.commit()

def invalidCommand(message):
    bot.sendMessage(
        message['from']['id'],
        'Invalid command'
    )
    return

def on(message):
    user = User.query.get(message['from']['id'])
    if not user:
        start(message)
    user.visible = True
    db.session.commit()

def off(message):
    user = User.query.get(message['from']['id'])
    if not user:
        start(message)
    user.visible = False
    db.session.commit()

def start(message):
    user = message['from']
    id = user['id']
    if not 'username' in user:
        bot.sendMessage(
            id,
            'please set a username in your Telegram account settings before continuing'
        )
        return
    username = user['username']
    user = User.query.get(id)
    if not user:
        user = User(username, id)
        bot.sendMessage(
            user.id,
            "you've been added"
        )
        return
    else:
        bot.sendMessage(
            user.id,
            "already added"
        )
        return

def tags(message):
    tagString = ''
    user = User.query.get(message['from']['id'])
    if not user:
        start(message)
    if user.tags:
        for tag in user.tags:
            tagString += f'{tag}\n'
    else:
        bot.sendMessage(
            user.id,
            'add tags with /add'
        )
        return
    if tagString == '':
        bot.sendMessage(
            user.id,
            'No result'
        )
        return
    bot.sendMessage(
        user.id,
        tagString
    )
    return

def delete(message):
    user = User.query.get(message['from']['id'])
    if not user:
        start(message)
    _tags = message['text'].split('/delete')
    print(message['text'])
    if len(_tags) > 1:
        _tags = _tags[1]
    else:
        return
    _tags = _tags.split(',')
    tags = []
    for tag in _tags:
        tag = tag.strip()
        if tag not in tags:
            tags.append(tag)
    if user.tags:
        user_tags = user.tags[:]
    else:
        bot.sendMessage(
            user.id,
            'add tags with /add'
        )
        return
    for tag in tags:
        if not isinstance(tag, str):
            tags.remove(tag)
        try:
            user_tags.remove(tag)
        except:
            pass
    user.tags = user_tags
    db.session.commit()

def users(message):
    user = User.query.get(message['from']['id'])
    if not user:
        start(message)
    total = 0
    query = User.query.filter(User.visible==True)
    query = User.query.filter(User.id != user.id)
    if user.tags:
        print(
            "user's tags: ", user.tags
        )
        for query_user in query:
            if query_user.tags:
                print(
                    'query_user:',
                    'username: ', query_user.username,
                    'tags: ', query_user.tags
                )
                query_user.score = 0
                for tag in user.tags:
                    print(
                        'tag: ', tag
                    )
                    try:
                        result = process.extractOne(tag, query_user.tags, scorer=fuzz.ratio)
                        print('user result', result)
                        if result:
                            score = result[1]   
                            if score:
                                query_user.score += score
                                total += 1
                    except Exception as e:
                        print('users exception', e)
                        pass
                if not query_user.score or not total or query_user.score < 1 or total < 1:
                    print(
                        'users error: not query_user.score or total',
                        'query_user.score: ',query_user.score, 
                        'total: ', total
                    )
                    continue
                print(
                    'end1:',
                    'query_user.score: ', query_user.score,
                    'total: ', total
                    )
                total*=100
                query_user.score = query_user.score/total * 100
                print(
                    'end2:',
                    'query_user.score: ', query_user.score,
                    'total: ', total
                    )                
            else:
                query = query.filter(User.id != query_user.id)
    else:
        bot.sendMessage(
            user.id,
            'add tags with /add'
        )
        return
    db.session.commit()
    if '/location' in message['text']:
        print('location', user.location)
        if user.location:
            location_sort(user.location, query)
        else:
            bot.sendMessage(
                user.id,
                'Send a location attachment to set a location'
            )
            return
    else:
        query = query.order_by(User.score.desc())
    query.limit(10)
    user_list = ''
    for query_user in query:
        if query_user.username:
            user_string = '@' + query_user.username + ' ' + str(query_user.score) + '%' + '\n'
            user_list += user_string
    if user_list == '':
        bot.sendMessage(
            user.id,
            'No result'
        )
        return
    bot.sendMessage(
        user.id,
        user_list
    )
    return

def help(message):
    command_list = ''
    for command in commands:
        command_string = ''
        if 'name' and 'desc' in command:
            command_string = '/' + command['name'] + ':\n' + command['desc'] +'\n\n'
        elif 'name' in command:
            command_string += '/' + command['name'] + '\n\n'
        elif 'desc' in command:
            command_string += command['desc'] + '\n\n'
        else:
            pass
        command_list += command_string
    if command_list == '':
        return
    bot.sendMessage(
        message['from']['id'],
        command_list
    )
    return

def add(message):
    user = User.query.get(message['from']['id'])
    if not user:
        start(message)
    _tags = message['text'].split('/add')
    print(message['text'])
    if len(_tags) > 1:
        _tags = _tags[1]
    else:
        return
    _tags = _tags.split(',')
    print(_tags)
    tags = []
    for tag in _tags:
        tag = tag.strip()
        if tag not in tags:
            tags.append(tag)
    if user.tags:
        user_tags = user.tags[:]
    else:
        user_tags = []
    for tag in tags:
        if not tag in user_tags:
            user_tags.append(tag)
    for tag in user_tags:
        if not isinstance(tag, str):
            user_tags.remove(tag)
    user.tags = user_tags
    db.session.commit()

@bp.route('/bot', methods=['POST'])
def update():
    data = request.get_json()
    print('data: ', data)
    if not data or not 'message' in data:
        return '', 200
    message = data['message']
    user = User.query.get(message['from']['id'])
    if user:
        print(user.dict())
    if 'location' in message:
        location(user, message['location'])
    if 'text' in message:
        text = message['text']
        if '/off' in text:
            off(message)
        elif '/on' in text:
            on(message)
        elif '/start' in text:
            start(message)
        elif '/help' in text:
            help(message)
        elif '/delLocation' in text:
            delLocation(user)
        elif '/add' in text:
            add(message)
        elif '/location' in text:
            users(message)
        elif '/users' in text:
            users(message)
        elif '/delete' in text:
            delete(message)
        elif '/tags' in text:
            tags(message)
        else:
            invalidCommand(message)
    return '', 202
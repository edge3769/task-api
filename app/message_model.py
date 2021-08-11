# import datetime
# from app import db
# from fuzzywuzzy import process, fuzz

# submessages = db.Table(
#     db.Column('parent', db.Integer, db.ForeignKey('message.id')),
#     db.Column('child', db.Integer, db.ForeignKey('message.id')))

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Unicode)
#     done = db.Column(db.Boolean, default=False)
#     time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
#     replies = db.relationship('Message',
#                     secondary=submessages,
#                     primary_join=id==submessages.c.parent,
#                     secondary_join=id==submessages.c.child,
#                     backref=db.backref('message', lazy='dynamic'),
#                     lazy='dynamic')

#     def parent(self, message, depth):
#         if not self.message:
#             return False
#         else:
#             return self.message.id == message.id or message.parent()
#         #TODO depth

#     def dict(self):
#         return {
#             'id': self.id,
#             'body': self.body,
#             'done': self.done,
#             'time': self.time
#         }

#     @staticmethod
#     def get(id, search, sort, order, message, depth):
#         query = Message.query
#         if sort:
#                 if sort == 'alpha':
#                     if order == 'asc':
#                         return Message.query.order_by(Message.body.asc())
#                     elif order =='dsc':
#                         return Message.query.order_by(Message.body.desc())
#                 elif sort == 'time':
#                     if order == 'asc':
#                         return Message.query.order_by(Message.time.asc())
#                     elif order =='dsc':
#                         return Message.query.order_by(Message.time.desc())
#         if search:
#             for message in Message.query:
#                 message.score = fuzz.ratio(message.body, search)
#         db.session.commit()
#         if message:
#             if depth == 1:
#                 query = query.filter(Message.message.id == message.id)
#             else:
#                 query = query.filter(Message.parent(message) == True)
#         if order == 'asc':
#             return Message.query.order_by(Message.score.asc())
#         elif order =='dsc':
#             return Message.query.order_by(Message.score.desc())

#     @staticmethod
#     def fuz(search, sort, fields, id, hidden, tags):
#         query = Message.query
#         for message in query:
#             message.score = 0
#             for tag in tags:
#                 try:
#                     message.score += process.extractOne(tag, message.tags)[1]
#                 except:
#                     pass
#         db.session.commit()
#         query.order_by(Message.score.desc())
#         return query

#     def toggle(self):
#         self.done = not self.done
#         db.session.commit()

#     def edit(self, name, message):
#         self.body = name
#         self.message = message
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         for message in self.messages:
#             message.delete()
#         db.session.commit()

#     def __init__(self, name, message=None):
#         self.body = name
#         self.message = message
#         db.session.add(self)
#         db.session.commit()

#     def is_child(self, message):
#         self.messages.filter(
#             submessages.c.child == message.id).count() > 0

#     def add(self, message):
#         if not self.is_child(message):
#             self.messages.append(message)
#             db.session.commit()

#     def remove(self, message):
#         if self.is_child(message):
#             self.messages.remove(message)
#             db.session.commit()

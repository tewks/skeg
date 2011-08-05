import json
from core import Composite, Hash, List

class Blog(Composite):
    properties = {'meta' : Hash, 'posts' : List}

    def add_post(self, title, body):
	self.posts.append(json.dumps({'title' : title, 'body' : body}))

    def posts_json(self, start=0, length=20):
        return '[%s]' % ','.join(post for post in self.posts[start:start+length])   
        	

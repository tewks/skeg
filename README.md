# skeg: run steady

# Examples

    l = List('test-l')
    l.append('hello, world')
    l[0] # 'hello, world'
    

    d = Dict('test-d')
    d['hello'] = 'world'
    d['hello']    # 'world'   

    class Blog(Composite):
        properties = {'meta' : Hash, 'posts' : List}

        def add_post(self, title, body):
            self.posts.append(json.dumps({'title' : title, 'body' : body}))

        def posts_json(self, start=0, length=20):
            return '[%s]' % ','.join(post for post in self.posts[start:start+length])


    >>> blog = Blog('bu.mp')
    >>> blog.add_post('First post', 'Hello, world')
    >>> blog.add_post('Second post', 'Hello, world')
    >>> blog.add_post('Third post', 'Hello, world')
    >>> blog.posts[:2]
    ['{"body": "Hello, world", "title": "First post"}', '{"body": "Hello, world", "title": "Second post"}']

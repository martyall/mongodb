# this follows this module of the week tutorial on http://pymotw.com/2/json/
# here is a brief description of the JSON format: he json module provides an
# API similar to pickle for converting in-memory Python objects to a serialized
# representation known as JavaScript Object Notation (JSON).
# Unlike pickle, JSON has the benefit of having
# implementations in many languages (especially
# JavaScript), making it suitable for inter-application
# communication. JSON is probably most widely used for
# communicating between the web server and client in an
# AJAX application, but is not limited to that problem domain.

import json

import tempfile


data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print 'Data:', repr(data)

# json.dumps serializes an object to a json formatted string, i.e.
# and encoded strin

data_string = json.dumps(data)
print 'JSON:', data_string

print 'Encoded', data_string

# loads deserializes a json object to a python object
decoded = json.loads(data_string)
print 'Decoded', decoded

print 'Origininal:', type(data[0]['b'])
print 'decoded:', type(decoded[0]['b'])

# notice here that strings -> unicode and tuple -> list
# inside the JSON object

# dumping to json format does not automatically sort the keys in any way
# but we may specify that we want that...
unsorted = json.dumps(data)
print 'JSON:', json.dumps(data)
print 'SORT:', json.dumps(data, sort_keys=True)


first = json.dumps(data, sort_keys=True)
second = json.dumps(data, sort_keys=True)


print 'unsorted match:', unsorted == first
print 'sorted match:', first == second

# we see here that json dumps gives an unsorted list

# now go back and forth
print json.loads(json.dumps(data))
print data
# what we see here is that going to jason then back to python object
# gives the same order (didnt specify to sort) but all tuples
# became lists and all strings got converted to unicode.

# remeber json data type is highly nested, so for readibility we specify indent

print 'Normal:', json.dumps(data, sort_keys=True)
print 'indented:', json.dumps(data, sort_keys=True, indent=2)

# ENCODING DICTIONARIES: json expects string keys, so it will throw an error
# for non string keys unless we tell it to just forget about these.

new_dict = data[0]
new_dict[(3,)] = 'd'
data = [new_dict]

print "first attempt"
try:
    print json.dumps(data)
except (TypeError, ValueError) as err:
    print 'Error:', err

print
print 'Second attempt'
print json.dumps(data, skipkeys=True)

# now we try a little action with our own types:


class MyObj(object):

    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return '<MyObj(%s)>' % self.s

# maybe the simplest way to do this is to try to convert MyObj instances to
# some known type, like a giant dict

obj = MyObj('instance value goes here')

print 'first attempt'
try:
    print json.dumps(obj)
except TypeError, err:
    print "error:", err

    
def convert_to_built_in_type(obj):
    print 'default(', repr(obj), ')'
    # converts an object to dict of representations
    d = {'__class__': obj.__class__.__name__,
         '__module__': obj.__module__,
         }
    d.update(obj.__dict__)
    return d

print 'with default'
# deault must be a function returning a serialized object
print json.dumps(obj, default=convert_to_built_in_type)

# now how do we reconstruct the object from the json datatype?
# just as dumbs takes "default", loads takes "object_hook"

print "\n\n\n now we do some json -> python \n\n"

def dict_to_object(d):
    if "__class__" in d:
        class_name = d.pop("__class__")
        module_name = d.pop("__module__")
        module = __import__(module_name)
        print "module:", module
        class_ = getattr(module, class_name)
        print "class", class_
        print "\n"
        args = dict((key.encode('ascii'), value) for key, value
                    in d.items())
        print "instance args", args
        inst = class_(**args)
    else:
        inst = d
    return inst

encoded_object = json.dumps(MyObj("HEY"), default=convert_to_built_in_type)

myobj_instance = json.loads(encoded_object, object_hook=dict_to_object)
print myobj_instance

# looking at above, module, class provide which object/constructor then pass
# object dictionary to be constructed.

print "\n"

# there is a json class encoder, JSONEncoder, a class in the json module. we
# can build doff this in order to do what we did above, but in a cleaner way


encoder = json.JSONEncoder()
data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
for part in encoder.iterencode(data):
    print "Part:", part

# hence the encode method is something like ''.join(enoder.iterable())

s = ''.join(encoder.iterencode(data))
print s
print json.loads(s)


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        print 'default(', repr(obj), ')'
        d = {'__class__': obj.__class__.__name__,
             '__module__': obj.__module__}
        d.update(obj.__dict__)
        return d

obj = MyObj("internal data")
print obj
print MyEncoder().encode(obj)


class MyDecoder(json.JSONDecoder):

    '''
    should take in a json type and return something of the
    form MyObj
    '''

    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict((key.encode('ascii'), value) for key,
                        value in d.items())
            print 'args:', args
            inst = class_(**args)
        else:
            inst = d
        return inst

    
myobj_instance = MyDecoder().decode(encoded_object)
print myobj_instance

f = tempfile.NamedTemporaryFile(mode='w+')
f.write('[{"a": "A", "c": 3.0, "b": [2, 4]}]')
f.flush()
f.seek(0)

print json.load(f)

# raw_decode allows as to parse data in a stram, by decoding
# what it can and then giving an index in to the first place
# in the file which wasn't passted to the decoder

decoder = json.JSONDecoder()

print encoded_object

def get_decoded_and_remainder(input_data):
    obj, end = decoder.raw_decode(input_data)
    remaining = input_data[end:]
    return (obj, end, remaining)

encoded_object = '[{"a": "A", "c": 3.0, "b": [2, 4]}]'
extra_text = 'This text is not JSON.'

print 'JSON first:'

new = ' '.join([encoded_object, extra_text])
obj, end, remaining = get_decoded_and_remainder(new)

print 'Object              :', obj
print 'End of parsed input :', end
print 'Remaining text      :', repr(remaining)

print
print 'JSON embedded:'

new2 = ' '.join([extra_text, encoded_object, extra_text])
try:
    obj, end, remaining = get_decoded_and_remainder(new2)
except ValueError, err:
    print 'ERROR:', err


    

# Scribe
Python Library for generating docs conforming to common data model .

scribe is a tool to process data collected and conform it to common data model
to facilitate data indexing into elasticsearch. Currently scribe only supports
data collected through stockpile but it's very easy to integrate other data
sources.

It is suggested to use a venv to install and run scribe.

	python3 -m venv /path/to/new/virtual/environment
    source /path/to/new/virtual/environment/bin/activate
    git clone https://github.com/redhat-performance/scribe
    pip install -e scribe/

Note: we're creating a python3 venv here as scribe is written in python3 and
      is currently incompatible with python2

## Usage

You can easily interact with the utilities through the provided command line
options or import the libraries provided by this package to use in your own
scripts.

### Provided Commands

Currently the only functionality provided through command line is scribe. It
takes 2 inputs and can be run as follows.

	(scribe_venv) [agopi@localhost virtenv3]$ scribe -t stockpile -ip /tmp/stockpile.json


### Using scribe as a python library

If you're just looking for a way to use `scribe` to generate documents and
consume them, take a look at `run_scribe.py` (excerpt below):

	from transcribe.render import transcribe
    for scribe_object in transcribe('/tmp/stockpile.json','stockpile'):
        print(scribe_object)


## Contributing

Please submit a github PR

## Contributing(making changes)

Scribe package is basically made of two modules:

1. scribes
2. scribe_modules

These 2 modules serve different purpose, scribes are for reading the input data
and pre-processing them into a structure that can be used to create
scribe_modules

The pre-processed dictionary structure can look like this:
```json
  {
  "scribe_module_1": [
      {
          "host": "localhost",
          "value": "sample_value_1"
      },
      {
          "host": "host1",
          "value": "sample_value_2"
      },
      {
          "host": "host2",
          "value": "sample_value_3"
      }
  ],
  "scribe_module_2": [
      {
          "host": "host2",
          "value": {
              "field1": "sample_filed1_value_3",
              "field2": "sample_field2_value_3"
          }
      },
      {
          "host": "host1",
          "value": [
              {
                  "field1": "sample_filed1_value_1",
                  "field2": "sample_field2_value_1"
              },
              {
                  "field1": "sample_filed1_value_2",
                  "field2": "sample_field2_value_2"
              }
          ]
      }
  ]
  }
```

Basically the dictionary needs to have first level keys that you've written
'scribe\_modules', match the name of the file in scribe\_modules/ . The children of
each of the module in dictionary should have the 2 keys - 'host' and 'value'.
the value for the key 'value' can be either a dictionary or a list of dictionary

Please note that the value for the key 'value' will be the one passed to the
scribe_modules while creating the object.

So let's take the simple example of scribe\_module\_2 for host2, just one object
would be created and the value passed would be

```json
  {
  "field1": "sample_filed1_value_3",
  "field2": "sample_field2_value_3"
  }
```

And like wise for host1, there will be 2 objects created.

for object 1, following value would be passed:

```json
  {
  "field1": "sample_filed1_value_1",
  "field2": "sample_field2_value_1"
  }
```

for object 2, following value would be passed:

```json
  {
  "field1": "sample_filed1_value_2",
  "field2": "sample_field2_value_2"
  }
```

While for scribe\_module\_1 for host1, the value that will be passed would be:
"sample\_value\_2"

### Adding new scribes

Steps to extend scribe to work with a new input-type 'example1' would involve:

1. Creating 'example1.py' in the 'transcribe/scribes/' directory. The sample
code would look like:


```python

from . import ScribeBaseClass


class Example1(ScribeBaseClass):

    def example1_build_initial_dict(self):
        output_dict = {}
        Example1_data = load_file(self._path)
        # .... some sort of data manipulation
        # .... to build the output_dict
        return output_dict

    def __init__(self, path=None, source_type=None):
        ScribeBaseClass.__init__(self, source_type=source_type, path=path)
        self._dict = self.example1_build_initial_dict()

    def emit_scribe_dict(self):
        return self._dict

```


Note the following:

a) from . import ScribeBaseClass needs to be present as we are inheriting
from the ScribeBaseClass

b) class Example1(ScribeBaseClass) is where inheritance occurs, ensure that
'(ScribeBaseClass)' is present when you write the class definition

c) The first letter in classname must be uppercase that's how factory method is
defined.

d) The \_\_init\_\_ function first calls the parent's \_\_init\_\_ function and passes
the default arguments which are path and source_type, however more can be added.
and they won't be needed to passed on to parent class's \_\_init\_\_ function.

e) emit\_scribe\_dict is an abstractmethod and thus it needs to be defined in any
other class that is written. However the method itself can be changed
but it should return the dictionary object as described above.

2. Add the module to choices list in scribe.py at L14, currently it looks like
   choices=['stockpile'], because at the time of creating this documentation
   only stockpile data could be transcribed using scribe.


### Adding new scribe_modules

Steps to extend scribe_modules to work with a new module 'scribe_module_1'
would involve:

1. Adding a new class 'scribe_module_1.py' to directory
'transcribe/scribe_modules'. It'd probably look something like this:
```python

  from . import ScribeModuleBaseClass


  class Scribe_module_1(ScribeModuleBaseClass):

      # This is the abstract method we have to override
      def parse(self):
          # input data is passed through self._input_dict
          # here is where data manipulation occurs to fit our requirements
          output_dict = {"value": self._input_dict}
          # output data should be passed under the "value" key of a dictionary
          yield output_dict

```

Note the following important things:

a) from . import ScribeModuleBaseClass needs to be present as we are inheriting
from the ScribeModuleBaseClass

b) class Example1(ScribeModuleBaseClass) is where inheritance occurs,
ensure that '(ScribeModuleBaseClass)' is present when you write the class.

c) The first letter in classname must be uppercase that's how factory method is
defined.

d) setting the new entities should be done inside the __parse___ method only,
but the user has flexibility of calling another method from either same class
or from lib/util.py to do transformation.

2. Add schema for the new class 'example1.yml' to the directory
'transcribe/schema'. Scribe currently uses cerberus to validate the iterable
produced by the scribe_modules subclass. Please look at
http://docs.python-cerberus.org/en/stable/validation-rules.html for more
information on how to write the schema for your class's output.

Note: The name of the yml file should match that of the scribe_modules class
that you create it for. Thus, for 'example1' class the file should be named
'example1.yml'

3. When adding a new scribe module for Stockpile please be sure to include
an example resulting json with the same name. This will be run in our
CI test suite. An easy way to obtain this json is by running the following
from your stockpile directory:
```ansible-playbook -i hosts stockpile.yml --tags=[my_module_tags],dump-facts```
Then copy the resulting json file to ci/[my_module_name].json

## Data Model and ES templates

Directory 'transcribe/schema' will essentially contain the data model.
Work needs to be done so that these yml files can be used to create templates
for elasticsearch. It's on the line of the ViaQ's elasticsearch templates work.

Please refer https://github.com/ViaQ/elasticsearch-templates for more info
on how templates can be created.

Do note that, currently ViaQ/elasticsearch-templates doesn't support creating
templates from the schema files present in 'transcribe/schema'

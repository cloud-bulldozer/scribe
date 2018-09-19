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

If you're just looking for a way to use scribe to generate documents and
consume them to build your JSON, which would be scribe's use case. You can do
something like the following.
The smallest sample would look like:

	from transcribe.render import transcribe
    for scribe_object in transcribe('/tmp/stockpile.json','stockpile'):
        print(scribe_object)


## Contributing(create patchsets)

Please visit http://gerrithub.io/ and Sign In with your github account.
Make sure to import your ssh keys.

Now, clone the github repository

        $ git clone https://github.com/redhat-performance/scribe.git

Make sure, you've git-review installed, following should work.

        $ sudo pip install git-review

To set up your cloned repository to work with Gerrit

        $ git review -s

It's suggested to create a branch to do your work,
name it something related to the change you'd like to introduce.

        $ git branch my_special_enhancement
        $ git checkout !$

Make your changes and then commit them using the instructions
below.

        $ git add /path/to/files/changed
        $ git commit -m "your commit title"

Use a descriptive commit title followed by an empty space.
You should type a small justification of what you are
changing and why.

Now you're ready to submit your changes for review:

        $ git review


If you want to make another patchset from the same commit you can
use the amend feature after further modification and saving. Make sure to be on
same branch, and if don't have the branch please follow next set of instructions

	$ git add /path/to/files/changed
        $ git commit --amend
        $ git review

If you want to submit a new patchset from a different location
(perhaps on a different machine or computer for example) you can
clone the repo again (if it doesn't already exist) and then
use git review against your unique Change-ID:

        $ git review -d Change-Id

Change-Id is the change id number as seen in Gerrit and will be
generated after your first successful submission. So, in case of
https://review.gerrithub.io/#/c/redhat-performance/scribe/+/425014/

You can either do git review -d 425014 as it's the number
or you can do git review -d If0b7b4f30615e46f009759b32a3fc533e811ebdc
where If0b7b4f30615e46f009759b32a3fc533e811ebdc is the change-id present

Make the changes on the branch that was setup by using the git review -d
(the name of the branch is along the lines of
review/username/branch_name/patchsetnumber).

Add the files to git and commit your changes using,

        $ git commit --amend

You can edit your commit message as well in the prompt shown upon
executing above command.

Finally, push the patch for review using,

        $ git review

### Adding Depends-On to commit message

A lot of times, especially when adding a new module.. Changes made to scribe,
will not ensure the CI to work propery until the respective changes to stockpile
are merged. In this case, to ensure CI doesn't work with master branch of
stockpile but rather the patchset you submitted to stockpile, You can use the
depends-on functionality.

To add Depends-On functionality, please copy the Change-Id of the patchset you
submitted to stockpile, and add it to the commit message at the end like this.

Note: Please add it after Change-Id in commit message.

The commit message should look like:

	Your commit message

	Change-Id: I9bc121f076b8625da88705c9d96bd00117f94c22

	Depends-On: {Change-Id of the review submitted to stockpile}

Say for example, you're working on adding a module to process satellite data,
the CI won't be able to test it because stockpile doesn't have a satellite
collection yet. However, because you've a commit thats still yet to be merged
like https://review.gerrithub.io/#/c/redhat-performance/stockpile/+/425015/

You can still ensure and verify stockpile-scribe workflow by adding Depends-On
to your commit message in scribe, so commit message will look like:

	Adding satellite Module to work with stockpile.

	Change-Id: some_random_change_id_generated_after_git_review

	Depends-On: I66329511b38a558ce61efb7edb4c3be18625b252

Note that the change ID in Depends-On is the same one in
https://review.gerrithub.io/#/c/redhat-performance/stockpile/+/425015/

For another example look at:
https://review.gerrithub.io/#/c/redhat-performance/scribe/+/425969/

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

      def __init__(self, input_dict=None, module_name=None, host_name=None,
                   input_type=None, scribe_uuid=None):
          ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                         input_dict=input_dict,
                                         host_name=host_name,
                                         input_type=input_type,
                                         scribe_uuid=scribe_uuid)
          if input_dict:
              new_dict = {}
              # ... this is where transformation occurs
              # ... can call other member functions of class
              # ... can set the entities of the class object like
              self.entity_1 = input_dict

      # This isn't needed here, as it's how the __iter__ function is defined
      # in the parent class and it's not an abstractmethod, so only if you'd
      # like to change how __iter__ method should work for your class, you
      # should add the following next lines.
      # Not recommended, unless you know what you're doing
      def __iter__(self):
            # ... your definition of how to make it iterable


```

Note the following important things:

a) from . import ScribeModuleBaseClass needs to be present as we are inheriting
from the ScribeModuleBaseClass

b) class Example1(ScribeModuleBaseClass) is where inheritance occurs,
ensure that '(ScribeModuleBaseClass)' is present when you write the class.

c) The first letter in classname must be uppercase that's how factory method is
defined.

d) The \_\_init\_\_ function first calls the parent's \_\_init\_\_ function and passes
the default arguments which are module_name, input_dict, host_name, input_type
and scribe_uuid. Please note that no more arguments can be passed.

e) setting the new entities should be done inside the \_\_init\_\_ function only,
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

## Data Model and ES templates

Directory 'transcribe/schema' will essentially contain the data model.
Work needs to be done so that these yml files can be used to create templates
for elasticsearch. It's on the line of the ViaQ's elasticsearch templates work.

Please refer https://github.com/ViaQ/elasticsearch-templates for more info
on how templates can be created.

Do note that, currently ViaQ/elasticsearch-templates doesn't support creating
templates from the schema files present in 'transcribe/schema'

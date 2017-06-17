# TODO

## Description

This documents describes the checkpoints for this project. *They are not set
in stone*, they can always be changed or replenished due to new developments
during implementation or other circumstances.

Changes in planning can be followed by inspecting this document's history on
GitHub.

The following paragraph lists the features necessary to complete the
respective versions of the project.

Take a look at [at the project's Kanban board](https://tree.taiga.io/project/kaleidophon-debattenkultur/kanban)
to see which tasks are currently worked on.

## Versions

### v0.1

* Init project structure
* Add appropriate models

### v0.2

* Add parser for the parliament's proceedings
* Wrap the content up within the different models in a structured manner

### v0.3
* Port to Python 3.6
* Change project structure
* Add semantic versioning
* Refactor some code

### v0.4

* Create a MongoDB in the project folder
* Create some code that specifically writes data into MongoDB

### v0.5

* Write daemon that updates the database on a regular basis
* A warning should be written into the log if daemon doesn't add new entries
to the database for a while

### v0.6

* Think of good class hierarchy for data analysis modules
* Implement superclass

### v0.7

* Add data analysis for word frequencies per speaker / faction
* Add data analysis for interruptions by faction
* Find elegant ways to add those to the database

### v0.8

* Add Flask App
* Add logging
* Add exception handling

### v0.9

* Think of a good website structure
* Add templates and views for app

### v0.10

* Add frontend using Bootstrap
* Visualize data

### v0.11

* Add unittests
* Compose project using docker

### v0.12
* Write meaningful README
* Add documentation

### v1.0

* Deploy the app online
* Test the features manually
* Send it to other people to test it

## Future features

This paragraph lists features that haven't been assigned to specific version
of the project yet.

* World domination
* ...

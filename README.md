# Natural Language Processing Classifier

The Natural Language Processing Classifier is a minimal implementation of a service to convert natural language inputs into semantic categories.  For example, a conversational system may wish to determine which broad semantic category an input may belong to ("I would like to open a new account, please" -> `NEW_ACCOUNT`). 

The Natural Langauge Processing Classifier does _not_ represent the state of the art in natural language classification: rather it represents a starting point for a simple conversational system.

## Starting the service

To run the service, choose one of the following options (without/with Docker):

### As a regular service

To run the Natural Language Processing Classifier as a python service, first set the `NLPC_FILE_SYSTEM_DATA_DIR` environment variable to a directory on your file system.  This will hold the raw training data and models.  Then, from the base directory, run

`python3 start.py`

This will start the web service.

### As a docker container

First, if you have not already done so, install Docker (https://www.docker.com/).  Then, from the base directory, run

`docker build -t nlpc .`

This will create a new docker image called `nlpc`.  To run the service:

`docker run -p 8081:5000 nlpc`

This will start the web service.

## Using the service

To view the swagger API documentation, navigate your web browser to http://localhost:8081/apidocs.

### Training the service

To train the Natural Language Processing Classifier, you must first add training data to a project, then train a model based on the training data in that project.

#### Adding training data

To add training data, use the `/languageclassifier/data/{project_id}` endpoint.  Each POST request can contain one or more data points, and you can make multiple calls to this endpoint to add more data.  For example, if we are training a system to respond to commands given on the bridge of a starship, we might use the following payload:

```
[
  {
    "label": "FIRE_PHASERS",
    "passage": "fire a phaser burst, half power"
  },{
    "label": "FIRE_PHASERS",
    "passage": "mister worf, fire phasers"
  },{
    "label": "FIRE_TORPEDO",
    "passage": "torpedo burst, five second delay"
  },{
    "label": "FIRE_TORPEDO",
    "passage": "torpedoes full spread please"
  },{
    "label": "FIRE_TORPEDO",
    "passage": "one torpedo should do it"
  },{
    "label": "GO_TO_WARP",
    "passage": "increase speed to warp 1"
  },{
    "label": "GO_TO_WARP",
    "passage": "let's go to warp"
  },{
    "label": "GO_TO_WARP",
    "passage": "helm get us out of here now"
  }
]
```

The corresponding curl command:

```commandline
curl -X POST "http://localhost:8081/languageclassifier/data/STAR_TREK" -H  "accept: application/json" -H  "Content-Type: application/json" -d "[  {    \"label\": \"FIRE_PHASERS\",    \"passage\": \"fire a phaser burst, half power\"  },{    \"label\": \"FIRE_PHASERS\",    \"passage\": \"mister worf, fire phasers\"  },{    \"label\": \"FIRE_TORPEDO\",    \"passage\": \"torpedo burst, five second delay\"  },{    \"label\": \"FIRE_TORPEDO\",    \"passage\": \"torpedoes full spread please\"  },{    \"label\": \"FIRE_TORPEDO\",    \"passage\": \"one torpedo should do it\"  },{    \"label\": \"GO_TO_WARP\",    \"passage\": \"increase speed to warp 1\"  },{    \"label\": \"GO_TO_WARP\",    \"passage\": \"let's go to warp\"  },{    \"label\": \"GO_TO_WARP\",    \"passage\": \"helm get us out of here now\"  }]"
```

This command will return a list of UUIDs, one representing each training datum.

#### Training a new model

Once you have called the `/languageclassifier/data/{project_id}` endpoint one or more times to add your training data, you can call the `/model/{project_id}` endpoint to train a model.  For example, to train a model based on our previous example:

```commandline
curl -X POST "http://localhost:8081/model/STAR_TREK" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"model_name\": \"thisisamodelname\"}"
```

This command will return a UUID representing the model that we have trained.

### Evaluating a novel input

To evaluate a novel input, use the `/languageclassifier/data/{project_id}/{model_id}` endpoint.  For example, if we want to evaluate a pair of starship bridge commands, we might use the following payload:

```
[
  "ahead warp factor 1, engage",
  "give me a full torpedo spread one thousand kilometers off the forward bow"
]
```

The corresponding curl command, with the model that we got from the training step:

```commandline
curl -X POST "http://localhost:8081/languageclassifier/data/STAR_TREK/1433b1cf-b948-4db7-ac05-fdf6f1506e3d" -H  "accept: application/json" -H  "Content-Type: application/json" -d "[  \"ahead warp factor 1, engage\",  \"give me a full torpedo spread one thousand kilometers off the forward bow\"]"
```

Expected output, showing the most likely class for the two natural language inputs:

```
["GO_TO_WARP", "FIRE_TORPEDO"]
```
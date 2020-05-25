# Reverse Geocoder

This repository holds a small web service that performs reverse geocoding to
determine whether a user specified location is within the geographic bounds of
a country. If it is then the response will contain attributes associated with
the matched country such as name, iso label, etc.

I created this simple demonstrator app to learn about FastAPI and PostGIS. It
is built using Python and a PostGIS database loaded with country outline
polygons obtained from shape files.

## API Endpoints

All endpoints are located at ``/v1/reverse-geocoder/`` and are accessible by HTTP.

The OpenAPI specification can be read from ``/v1/reverse-geocoder/openapi.json``.

A SwaggerUI that renders the OpenAPI specification can be found at ``/v1/reverse-geocoder/docs``.
The root ``/`` will also redirect to the SwaggerUI docs page.

### Reverse Geocoder Endpoint

To access the reverse geocoder send a POST to `/v1/reverse-geocoder/` with a
payload containing the location of interest.

When the user supplied point is within a county then the response contains
attributes of the country that matched. When the user supplied point is not
within a county then the response indicates that no country matched.

```http
POST /v1/reverse-geocoder/ {"location":{"longitude":146.558384,"latitude":-42.239392}}
```

The response will always contain a copy of the query parameters so that it
provides some context for the data. When the location is within a country
bounds then the response payload will look like this:
```json
{
  "location":{
    "latitude":-42.239392,
    "longitude":146.558384,
    "altitude":null
  },
  "country":{
    "name":"Australia",
    "iso2":"AU",
    "iso3":"AUS"
  }
}
```

If the point is not within a country boundary then the response will look like
this:
```json
{
  "location":{
    "latitude":-35.031741,
    "longitude":138.119541,
    "altitude":null
  },
  "country":null
}
```

## Run Demo

To simplify running the reverse geocoding service a Docker compose
configuration example is included. However, a few set up steps need to be run
first to prepare data that will go into the database - as it is not stored in
this repository.

### Clone Repo

```
$ git clone https://github.com/claws/reverse-geocoder.git
$ cd reverse-geocoder
```

### Preparation

This demonstration uses world country boundary outlines in shape file format
(.shp, .dbf, .shx files) which contain encoded polygons along with other
attributes. However, the files are not stored in this repo so they need to be
downloaded and then converted into SQL statements.

The following steps show how to download the content from
[here](http://thematicmapping.org/downloads/world_borders.php), decompress it
and then convert it into SQL statements that can later be run to insert the
contents into the database.

It is important that the name of the generated SQL file is ``100-shapes.sql``
to ensure it gets run after the builtin PostGIS initialization script (which
is ``10_postgis.sh``). This file will be used as a volume mount in the Docker
compose configuration.

``shp2pgsql`` is a command line tool that comes with PostGIS. It converts shape
files into a SQL format that can be imported into a PostGIS database. The '-G'
specifies the use of the geography data type. The '-I' option creates a spatial
index after the table is created. This is strongly recommended for improved
performance. To run the last command you may need to install PostGIS on your
host machine to get the ``shp2pgsql`` tool - there may even be a Docker
container that has it too.

```
$ cd database
$ wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
$ unzip TM_WORLD_BORDERS-0.3.zip
$ shp2pgsql -G -I TM_WORLD_BORDERS-0.3.shp countries > 90-shapes.sql
$ cd ..
```

The shape file produce columns containing the following structures:

| COLUMN    | TYPE             | DESCRIPTION                                             |
| --------- | ---------------- | ------------------------------------------------------- |
| fips      | String(2)        | FIPS 10-4 Country Code                                  |
| iso2      | String(2)        | ISO 3166-1 Alpha-2 Country Code                         |
| iso3      | String(3)        | ISO 3166-1 Alpha-3 Country Code                         |
| un        | Short Integer(3) | ISO 3166-1 Numeric-3 Country Code                       |
| name      | String(50)       | Name of country/area                                    |
| area      | Long Integer(7)  | Land area, FAO Statistics (2002)                        |
| pop2005   | Double(10,0)     | Population, World Population Prospects (2005)           |
| region    | Short Integer(3) | Macro geographical (continental region), UN Statistics  |
| subregion | Short Integer(3) | Geographical sub-region, UN Statistics                  |
| lon       | FLOAT (7,3)      | Longitude                                               |
| lat       | FLOAT (6,3)      | Latitude                                                |
| geog      | Polygon          | Country/area border as polygon(s)                       |


### Start services

Start the database and web server using Docker compose. As part of the startup
steps the database runs initialisation script - which will run SQL file created
in the setup steps above.

```
$ docker-compose up --build
```

The FastAPI framework is built upon OpenAPI and it supports a builtin viewer
for the interface specification. These allow developers to perform manual
tests.

Once the services start up you should be able to access the SwaggerUI web user
interface [here](http://localhost:8000/) which should redirect you to the
[docs](http://localhost:8000/v1/reverse-geocoder/docs) site.

Click the POST ``/v1/reverse-geocoder/`` row to expose details about the
endpoint. This endpoint is implemented to accept a payload, rather than URL
parameters, as it can then rely on the specification and Pydantic to simplify
the interface between the API endpoint and the database layer.

Click the ``Try it out`` button. This changes the form to allow user input.
Leave the default payload structure then click ``Execute``. The Responses
section should get populated with the data returned from the web service -
which in this case indicates that the point was in Australia.

Try changing the location to some of those in the table below. The last two
should return 'null' for the country as they are located in a sea.

| Rough Location  | Position                |
| --------------  | ----------------------- |
| Tasmania        | 146.558384 -42.239392   |
| New Zealand     | 167.930127 -47.033240   |
| Hawaii          | -157.935416 21.460822   |
| Iceland         | -21.478138 64.113670    |
| Cypress         | 34.321495 35.556301     |
| St Vincent Gulf | 138.119541 -35.031741   |
| Black Sea       | 34.402367 43.400157     |

The Swagger UI also shows the equivalent curl command to use too.

#### Check using curl

The Reverse Geocoder Service REST API can be used from curl too.

```
$ curl -X POST "http://localhost:8000/v1/reverse-geocoder/" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d "{\"location\":{\"longitude\":146.558384,\"latitude\":-42.239392}}"
{"location":{"latitude":-42.239392,"longitude":146.558384,"altitude":null},"country":{"name":"Australia","iso2":"AU","iso3":"AUS"}}
```

When the user supplied point is not within a county then the response
indicates that no country matched.
```
$ curl -X POST "http://localhost:8000/v1/reverse-geocoder/" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d "{\"location\":{\"longitude\":138.119541,\"latitude\":-35.031741}}"
{"location":{"latitude":-35.031741,"longitude":138.119541,"altitude":null},"country":null}
```


## Developer Notes


### Data Server

It can be useful during development to run the Python web server locally. The
instructions below show how to do that.

Create a Python virtual environment.

```console
$ python3.8 -m venv venv --prompt fast
$ source venv/bin/activate
(fast) $ pip install pip -U
(fast) $ pip install -r requirements.dev.txt
(fast) $ pip install -r requirements.txt
```

Apply code style

```
$ cd reverse_geocoder_service
$ black app
```

Run the data server. Use ``--reload`` to enable automatic reloads on code
changes.

```console
(fast) $ cd reverse_geocoder_service
(fast) $ uvicorn app.main:app --reload --log-level info
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2617]
INFO:     Started server process [2619]
INFO:     Waiting for application startup.
INFO:     Connected to database postgresql://postgres:********@localhost:54321/postgres
INFO:     Application startup complete.
```

### Database Inspection

It can be useful to attach to the database directly to test out queries. Use
`docker-compose` to connect to the running database by attaching to the
container. Once attached the ``psql`` tool can be used to execute a query
identical to that done by the web service to check if a point lies within a
polygon.

The PostGIS ``ST_Covers`` function which returns TRUE if A covers B (i.e. no
points of B are outside A).

```
$ docker-compose run database bash
postgres@4f5d94706a9b:/$
postgres@4f5d94706a9b:/$ psql --host database -U postgres postgres
Password for user postgres:
postgres=#
postgres=# SELECT name,fips,iso2,iso3 FROM countries WHERE ST_Covers(countries.geog, ST_GeographyFromText('POINT(146.558384 -42.239392)'));
   name    | fips | iso2 | iso3
-----------+------+------+------
 Australia | AS   | AU   | AUS
(1 row)
postgres=#
postgres=# SELECT name,fips,iso2,iso3 FROM countries WHERE ST_Covers(countries.geog, ST_GeographyFromText('POINT(138.119541 -35.031741)'));
 name | fips | iso2 | iso3
------+------+------+------
(0 rows)
postgres=# \q
postgres@4f5d94706a9b:/$ exit
```

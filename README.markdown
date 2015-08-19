#Wunderground Python API wrapper
WunderPython is an API wrapper for the [Wunderground API](http://www.wunderground.com/weather/api/).

##Installation
    
    $ pip install WunderPython --pre
    
The '--pre' option is requierd because there is currently no version marked as stable.

##Requirements
    Python 2

##Usage
Import the library
    
    >>> from wunderpython import wunderground
    
Create an instance of the API wrapper

    >>> wg = wunderground.Wunderground('your secret api key')

Find a location

    >>> wg.search(’Munich, G’)
    [’Munich, Germany’, ’Munich, Grenada’]

Get a info about a location

    >>> location = wg['Munich, Germany']
    >>> location.name
    'Munich, Germany'
    >>>
    >>> # getting the latitude and longitude
    >>> location.ll
    48.130001 11.700000
    
Get a data feature

    >>> conditions = location.conditions
    >>> conditions[’temperature_string’]
    64 F (18 C)

Supported features are: ['alerts', 'almanac', 'astronomy', 'conditions', 'forecast', 'forecast10day', 'hourly', 'hourly10day', 'rawtide', 'satellite', 'tide', 'webcams']

Access historical data

    >>> pastDay = location.history[’2009.06.23’]
    >>> pastDay[’observations’][0][’tempi’]
    53.6

##Examples
Some examples that can be used in IPython Notebook.

###Compare the mean temperature of several cities

    from wunderpython import wunderground
    wg = wunderground.Wunderground('your secret api key')
    from pandas import *
    x = []
    ds = {}

    for city in wg['Munich, Germany', 'New York City, New York', 'Changde, China']:
        ds[city.name] = []
        for day in city.history['2014.06.01':'2014.07.01']:
            dailysummary = day['dailysummary'][0]        
            if dailysummary['date']['year']+'.'+dailysummary['date']['mon']+'.'+dailysummary['date']['mday'] not in x:
                x.append(dailysummary['date']['year']+'.'+dailysummary['date']['mon']+'.'+dailysummary['date']['mday'])
            ds[city.name].append(float(dailysummary['meantempm']))

    df = DataFrame(ds, x)
    print df.plot(rot = 90)


###Compare wind and pressure

    from wunderpython import wunderground
    wg = wunderground.Wunderground('your secret api key')
    from pandas import *
    x = []
    ds = {
        'pressurem':[],
        'wspdm':[],
    }


    for day in wg['Munich, Germany'].history['2014.05.02':'2014.05.05']:
        for observation in day['observations']:
            x.append(observation['date']['pretty'])
            ds['pressurem'].append(float(observation['pressurem']))
            ds['wspdm'].append(float(observation['wspdm']))

    df = DataFrame(ds, x)
    df.pressurem.plot(secondary_y=True)
    df.wspdm.plot(rot = 90)


##Tests
Before running the tests you have to replace `no_valid_key` with your API Key in `tests/test_wunderpython.py`

Then you can run the tests with:
    
    python tests/test_wunderpython.py
    

##Note
* [Terms of Service](http://www.wunderground.com/weather/api/d/terms.html)
* Developed with Wunderground API Version 0.1, Python 2.7 and IPython Notebook 3.0.

Features not yet supported:
* currenthurricane
* geolookup
* planner
* yesterday

Also WunderMap Layers are not yet supported.

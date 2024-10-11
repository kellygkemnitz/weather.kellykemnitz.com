# Python application to pull data from PWS on Wunderground and create new graphs

## Background
This is a different implementation that I forked from Zach Perzan's repository available at https://github.com/zperzan/scrape_wunderground

Some of the key differences between this forked repo and the original include:
1. Removed command line arguments and ported configuration to settings.yaml
2. Moved weather station scraper functions to class WeatherStation and constructing class using values provided in settings.yaml
3. Created method within class to return settings
4. Removed requirements for selenium and chromedriver, as BeautifulSoup can handle the scraping on its own.
5. Added method for returning scraped data in html file
6. Migrated ability to export scraped data in CSV format to method
7. Created plotly.graphs.py to generate Plotly graphs
8. Created dash_app.py to run Dash app that presents Plotly graphs
9. Created requirements.txt to specify all packages needed


## Using this package
Update settings.yaml:
```
station: <change_me>
freq: 5min
attempts: 4
wait_time: 5.0
```

As long as BeautifulSoup is installed, the script should work fine after that. However, there are a few important points to note about processing the data once it's downloaded:

1. All data is listed in local time. So summer data is in daylight savings time and winter data is in standard time.
2. Depending on the quality of the station, 
3. All pressure data is reported as sea-level pressure. Depending on the weather station, it may be possible to back-calculate to absolute pressure; some manufacturers (e.g., Ambient Weather WS-2902) use a constant offset whereas others (e.g., Davis Vantage Pro2) perform a more complicated barometric pressure reduction using the station's 12-hr temperature and humidity history.

## Python dependencies 
```
APScheduler==3.10.4
beautifulsoup4==4.12.3
blinker==1.8.2
bs4==0.0.2
certifi==2024.8.30
charset-normalizer==3.4.0
click==8.1.7
dash==2.18.1
dash-bootstrap-components==1.6.0
dash-core-components==2.0.0
dash-html-components==2.0.0
dash-table==5.0.0
DateTime==5.5
Flask==3.0.3
gunicorn==23.0.0
idna==3.10
importlib_metadata==8.5.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.1
nest-asyncio==1.6.0
numpy==2.1.2
packaging==24.1
pandas==2.2.3
plotly==5.24.1
python-dateutil==2.9.0.post0
pytz==2024.2
PyYAML==6.0.2
requests==2.32.3
retrying==1.3.4
six==1.16.0
soupsieve==2.6
tenacity==9.0.0
typing_extensions==4.12.2
tzdata==2024.2
tzlocal==5.2
urllib3==2.2.3
Werkzeug==3.0.4
zipp==3.20.2
zope.interface==7.1.0
```

## Development
Pull requests are welcome. Please let me know if you have suggestions for improvement.

## Contact
Kelly Kemnitz  
[kellygkemnitz@gmail.com](mailto:kellygkemnitz@gmail.com)  

<h1 align="center">CL Search </h1>
<p align="center" style="font-size: large;">Get <strong>everything</strong> from Craigslist</p>
<br>

## Table of contents
- [Why?](#why)
- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Commands](#Commands)
    - [Location](#location)
    - [Output](#output)
    - [Browser](#browser)
    - [Headless Mode](#headless-mode)
    - [Search](#search)
    - [Image](#image)
    - [Category](#category)
- [Contributing](#contributing)

## Why
My interest in web scraping began in 2018 when I was desperate to buy a [Modcan Dual Delay](https://www.modcan.com/emodules/dualdelay.html) for my Eurorack collection and stumbled across [WiggleHunt](https://wigglehunt.com/). Since then, I’ve found the utility of organizing used items for sale from across a variety of different websites genius. I built CL Search to solve this problem.

## Features
- Supports Chrome, Chromium, Edge, Firefox, & Safari
- Supports all Craigslist locations!
- Customize your desired locations in `locations.py`
- Supports a variety of formats to export data!
- Supports headless mode in all browsers!

## Installation

**Building from source**
```
gh repo clone gavink97/cl-search .
pip install --no-cache-dir -r requirements.txt
pip install -e .
```

## Getting Started
**Using the CLI**

Use cl to begin your search:
```
cl -L austin
```

## Commands

### Location

**Location is a required flag**

Supports URLs, City Names, States, Provinces, Countries, Continents, or Craigslist!

`-L or --location foo`

<br>

Examples:

`-L 'New York'`

`-L https://dallas.craigslist.org`


🦅 Use Lower 48 to search thru the Contiguous US 🦅

`-L 'Lower 48'`

*You can customize locations by appending to the end of the dict in `locations.py`*


### Output

**Defaults to CSV**

Supports many different formats!
- csv
- json
- html
- LaTex #requires Jinja2
- xml
- excel
- hdf5
- feather
- parquet
- orc
- stata
- pickle
- clipboard

SQL support coming soon!

<br>

**Output:**

`-o or --output foo`

Simply type in the name of the format

`-o json`

or just use the extension for ease of use!

`-o xlsx`

<br>

**Export directly to clipboard!**

*Linux users may need to install xclip or xsel (with PyQt5, PyQt4 or qtpy) for use!*

`-o clipboard`

### Browser

**Defaults to Firefox**

Supports Chrome, Chromium, Edge, Firefox, & Safari.

`-b or --browser foo`


### Headless Mode

**False by Default**

Supports Headless mode in all major browsers!

`--headless`

### Search

**No Default / Not Required**

Query a search or take every listing!

`-s foo`

`-s or --search 'foo bar'`

### Image

**False by Default**

Downloads images from the listings.

`-i or --image`

### Category

**Default All for sale**

Select the category or subcategory you wish to search in.

`-C or --category 'foo bar'`

*All categories are listed in `categories.py`*

You can customize these categories by appending to the end of the dict.

<br>

**Some of my favorite categories are:**

Free -  to search for free stuff.

`-C free`

Software -  to look for Software Engineering jobs.

`-C software`

Housing - to search for housing.

`-C housing`


## Contributing

Contributions are welcomed to this project.

Please take advantage of [pre-commit](https://pre-commit.com/) to lint and test your PRs before sending them to me :)

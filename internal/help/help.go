package help

const (
	Default = `cl-search scrape from craigslist with ease.

Usage:

    	cl-search "location" "query" [arguments] [--flags]

The commands are:

	bug 		start a bug report
	help		print help for command
	version		print cl-search version

Arguments available:
	Location	required argument.
	Query		required argument.

	browser		sets the browser. default is chromium
	max-workers	sets the maximum number of workers. default is 4
	output		output path for results. default is "./output.csv"

Flags available:

	headed		enables headed mode for browser. default is false (headless)
	images		enables downloading images. default is false
	verbose		print debug messages

Use "cl-search help <command>" for more information about a command.

Additional help topics:

	search		the search command
	env-vars	environment variables

Use "cl-search help <topic>" for more information about a command.`
	Environment = `cl-search Environment variables

	XDG_DATA_HOME			used for locations.json
	XDG_CONFIG_HOME			not in use
	TZ						used for timestamp column

	CL_SEARCH_USER_AGENT	user agent`
	Bug = `Usage: cl-search bug

Bug opens the default browser and starts a new bug report.`
	Search = `Usage: cl-search "location" "query" [arguments] [--flags]

Search is the default function of cl-search when you input a valid location.

Search requires a location argument and query argument in the first and second
position.

Locations are validated via locations.json which is stored in:
$HOME/.local/share/cl-search or in $XDG_DATA_HOME/cl-search

Locations are selected by matching a location using the location argument from
highest to lowest order. In order to select a location which matches one from a
higher order you should specify it's parent element seperated by a period.

For example:
Canada and California both use "ca". To specify California use "us.ca"

You can find a complete list of locations here:
https://craigslist.org/sitemap.html


Query is the second required argument for search.

The minimum requirement for query is an empty string: "" which defaults to
search for all items in a given category.


Output is not a required argument but I recommend specifiying an output.

There are two support output types ".csv" for spreadsheets and ".db" which is
an sqlite3 database.`
	Version = `Usage: cl-search version

Version prints the binaries version details.`
)

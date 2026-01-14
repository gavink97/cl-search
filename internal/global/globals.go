package global

import (
	"log/slog"
	"os"
	"os/user"
	"path"
	"time"

	"github.com/gavink97/cl-search/internal/utils"
)

var VERSION = "2.0.0"

var CONFIG_HOME string = getConfigHome()
var DATA_HOME string = getDataHome()
var TZ *time.Location = getTimeZone()
var UserAgent string = os.Getenv("CL_SEARCH_USER_AGENT")

var ProgramLevel = &slog.LevelVar{}
var Logger *slog.Logger
var DBConnection *utils.Database

var Output string = "output.csv"
var WriteAs string = "csv"
var Category string = "sss"
var Browser string = "chromium"
var DownloadImages bool = false
var Headless bool = true
var MaximumWorkers int = 4

var Location []string
var Query string
var NewCSV bool

func getDataHome() string {
	xdg := os.Getenv("XDG_DATA_HOME")
	if xdg != "" {
		return path.Join(xdg, "cl-search")
	}

	usr, err := user.Current()
	if err != nil {
		return ""
	}

	return path.Join(usr.HomeDir, ".local", "share", "cl-search")
}

func getConfigHome() string {
	xdg := os.Getenv("XDG_CONFIG_HOME")
	if xdg != "" {
		return path.Join(xdg, "cl-search")
	}

	usr, err := user.Current()
	if err != nil {
		return ""
	}

	return path.Join(usr.HomeDir, ".config", "cl-search")
}

func getTimeZone() *time.Location {
	tz := os.Getenv("TZ")

	tzLoc, err := time.LoadLocation(tz)
	if err != nil {
		Logger.Warn("unable to load TZ", slog.String("error", err.Error()))
	}

	return tzLoc
}

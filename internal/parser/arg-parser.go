package parser

import (
	"encoding/json"
	"fmt"
	"io"
	"io/fs"
	"log/slog"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"

	"github.com/gavink97/cl-search/internal/global"
	"github.com/gavink97/cl-search/internal/help"
)

func ParseArgs(args []string) {
	argLength := len(args)
	var program string
	var argument string

	if argLength == 0 {
		program = ""
	} else {
		program = args[0]
	}

	switch program {
	case "bug":
		openBugReport()

	case "version":
		printVersion()

	case "help":
		printHelp(argument)

	default:
		if program == "" {
			printHelp("")
		}

		if !global.CheckFiles() {
			err := global.GenerateLocations()
			if err != nil {
				global.Logger.Error("a fatal error occurred generating locations.json", slog.String("error", err.Error()))
				os.Exit(1)
			}
		}

		ParseFlags(args)
	}
}

func ParseFlags(args []string) {
	for i := 0; i < len(args); i++ {
		arg := args[i]

		if i == 0 {
			loc := strings.ToLower(arg)
			if !validLocation(loc) {
				fmt.Printf("invalid location argument: %s\n", loc)
				os.Exit(1)
			}
			continue
		}

		if i == 1 {
			global.Query = arg
			continue
		}

		if strings.EqualFold(arg, "--verbose") {
			global.ProgramLevel.Set(slog.LevelDebug)
			continue
		}

		if strings.EqualFold(arg, "--headed") {
			global.Headless = false
			continue
		}

		if strings.EqualFold(arg, "--images") {
			global.DownloadImages = true
			continue
		}

		if strings.EqualFold(arg, "--max-workers") {
			i++
			workers, err := strconv.Atoi(args[i])
			if err != nil {
				global.Logger.Error("unable to convert max-workers to integer", slog.String("max-workers", args[i]), slog.String("error", err.Error()))
				os.Exit(1)
			}

			global.MaximumWorkers = workers
			continue
		}

		if strings.EqualFold(arg, "--browser") {
			i++

			switch strings.ToLower(args[i]) {
			case "chrome", "chromium":
				global.Browser = "chromium"
			case "firefox":
				global.Browser = "firefox"
			case "webkit", "safari":
				global.Browser = "webkit"
			default:
				fmt.Printf("invalid browser argument: %s\n", args[i])
				os.Exit(1)
			}

			continue
		}

		if fs.ValidPath(arg) {
			switch strings.ToLower(filepath.Ext(arg))[1:] {
			case "csv":
				_, err := os.Stat(arg)
				if err != nil {
					global.NewCSV = true
				} else {
					global.NewCSV = false
				}

				global.Output = arg
				global.WriteAs = "csv"
			case "db":
				global.Output = arg
				global.WriteAs = "sqlite"
			default:
				fmt.Printf("unknown file format in output: %s\n", arg)
				os.Exit(1)
			}
			continue
		}
	}
}

func printVersion() {
	fmt.Printf("cl-search version %s %s/%s\n", global.VERSION, runtime.GOOS, runtime.GOARCH)
	os.Exit(0)
}

func printHelp(command string) {
	switch command {
	case "":
		fmt.Println(help.Default)
	case "bug":
		fmt.Println(help.Bug)
	case "search":
		fmt.Println(help.Search)
	case "env-vars":
		fmt.Println(help.Environment)
	case "version":
		fmt.Println(help.Version)
	default:
		global.Logger.Info(fmt.Sprintf("unknown command: %v", command))
		fmt.Println(help.Default)
	}

	os.Exit(0)
}

func validLocation(str string) bool {
	locations, err := os.Open(path.Join(global.DATA_HOME, "locations.json"))
	if err != nil {
		global.Logger.Error("unable to open file", slog.String("file", path.Join(global.DATA_HOME, "locations.json")), slog.String("error", err.Error()))
		return false
	}

	defer func() {
		err := locations.Close()
		if err != nil {
			global.Logger.Error("unable to close locations.json", slog.String("error", err.Error()))
		}
	}()

	file, err := io.ReadAll(locations)
	if err != nil {
		global.Logger.Error("unable to read locations", slog.String("error", err.Error()))
		return false
	}

	var locs global.Locations
	err = json.Unmarshal(file, &locs)
	if err != nil {
		global.Logger.Error("unable to unmarshal locations json", slog.String("error", err.Error()))
		return false
	}

	str = strings.ToLower(str)
	parts := strings.Split(str, ".")
	switch len(parts) {
	case 1:
		country, ok := locs[str]
		if ok {
			for _, t := range country {
				for _, l := range t {
					global.Location = append(global.Location, l.Url)
				}
			}
			return true
		}
	case 2:
		country := parts[0]
		territory := parts[1]

		territories, ok := locs[country]
		if ok {
			localities, ok := territories[territory]
			if ok {
				for _, locality := range localities {
					global.Location = append(global.Location, locality.Url)
				}
				return true
			}
		}
		return false
	case 3:
		country := parts[0]
		territory := parts[1]
		locality := parts[2]

		territories, ok := locs[country]
		if ok {
			localities, ok := territories[territory]
			if ok {
				local, ok := localities[locality]
				if ok {
					global.Location = append(global.Location, local.Url)
					return true
				}
			}
		}
		return false
	}

	for _, countries := range locs {
		territory, ok := countries[str]
		if ok {
			for _, l := range territory {
				global.Location = append(global.Location, l.Url)
			}
			return true
		}
		for _, territories := range countries {
			for l, locality := range territories {
				local := locality.Local
				subdomain := locality.Url[8 : len(locality.Url)-15]

				if strings.Contains(l, str) {
					global.Location = append(global.Location, locality.Url)
					return true
				}

				if strings.Contains(local, str) {
					global.Location = append(global.Location, locality.Url)
					return true
				}

				if strings.Contains(subdomain, str) {
					global.Location = append(global.Location, locality.Url)
					return true
				}
			}
		}
	}

	return false
}

// include version, etc
func openBugReport() {
	var cmd string
	var args []string

	url := "https://github.com/gavink97/cl-search/issues/new?labels=bug&title=Title&body=Please+check+if+an+issue+containing+this+error+exists+before+submitting.+Also+try+to+provide+any+steps+we+can+use+to+reproduce+the+error."

	switch runtime.GOOS {
	case "windows":
		cmd = "rundll32"
		args = []string{"url.dll,FileProtocolHandler", url}
	case "darwin":
		cmd = "open"
		args = []string{url}
	default:
		if isWSL() {
			cmd = "cmd.exe"
			args = []string{"/c", "start", url}
		} else {
			cmd = "xdg-open"
			args = []string{url}
		}
	}

	if len(args) > 1 {
		args = append(args[:1], append([]string{""}, args[1:]...)...)
	}

	err := exec.Command(cmd, args...).Start()
	if err != nil {
		global.Logger.Error("An unexpected error occured", slog.String("error", err.Error()))
		os.Exit(1)
	}

	os.Exit(0)
}

func isWSL() bool {
	releaseData, err := exec.Command("uname", "-r").Output()
	if err != nil {
		return false
	}
	return strings.Contains(strings.ToLower(string(releaseData)), "microsoft")
}

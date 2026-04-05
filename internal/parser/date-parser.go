package parser

import (
	"errors"
	"fmt"
	"log/slog"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/gavink97/cl-search/internal/global"
)

func ParseDate(date string) (time.Time, error) {
	var t time.Time

	if strings.Contains(date, "ago") {
		re := regexp.MustCompile(`^(?:<(\d+)(hr|h)|(\d+)(hr|h)) ago$`)
		matches := re.FindStringSubmatch(date)
		if matches == nil {
			return t, errors.New("no matches found")
		}

		var m string

		for _, match := range matches[1:] {
			if match == "" {
				continue
			}

			m = match
			break
		}

		value, err := strconv.Atoi(m)
		if err != nil {
			global.Logger.Debug("an error occurred parsing int: %s", slog.String("match", matches[1]), slog.String("error", err.Error()))
			return t, err
		}

		now := time.Now().In(global.TZ)
		return now.Add(time.Duration(-value) * time.Hour), nil
	}

	if strings.Contains(date, ",") {
		d := strings.Split(date, ",")
		date = d[0]
	}

	cl := strings.Split(date, "/")

	m, err := strconv.Atoi(cl[0])
	if err != nil {
		global.Logger.Debug("an error occurred parsing the date", slog.String("month", cl[0]), slog.String("error", err.Error()))
		return t, err
	}

	d, err := strconv.Atoi(cl[1])
	if err != nil {
		global.Logger.Debug("an error occurred parsing the date", slog.String("day", cl[1]), slog.String("error", err.Error()))
		return t, err
	}

	now := time.Now().In(global.TZ)
	n := strings.Split(now.Format("2006-01-02"), "-")

	mn, err := strconv.Atoi(n[1])
	if err != nil {
		global.Logger.Debug("an error occurred parsing the time now", slog.String("month", n[1]), slog.String("error", err.Error()))
		return t, err
	}

	var year int
	if m > mn {
		year = now.AddDate(-1, 0, 0).Year()
	} else {
		year = now.Year()
	}

	clString := fmt.Sprintf("%d-%d-%d", year, m, d)

	clTime, err := time.Parse("2006-1-2", clString)
	if err != nil {
		global.Logger.Debug("an error occurred parsing the time", slog.String("time", clString), slog.String("error", err.Error()))
		return t, err
	}

	return clTime, nil
}

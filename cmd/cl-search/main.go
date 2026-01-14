package main

import (
	"log/slog"
	"os"

	"github.com/gavink97/cl-search/internal/cl"
	"github.com/gavink97/cl-search/internal/global"
	"github.com/gavink97/cl-search/internal/parser"
	"github.com/gavink97/cl-search/internal/utils"
	"github.com/gavink97/cl-search/internal/writer"
	"github.com/playwright-community/playwright-go"
)

func main() {
	args := os.Args[1:]
	global.SetDefaultLogger()
	parser.ParseArgs(args)

	if global.WriteAs == "sqlite" {
		sqlDB := writer.MustOpen(global.Output)

		defer func() {
			err := sqlDB.Close()
			if err != nil {
				global.Logger.Error("could not close db connection", slog.String("error", err.Error()))
			}
		}()

		err := sqlDB.CreateTables()
		if err != nil {
			global.Logger.Error("could not create tables", slog.String("error", err.Error()))
			os.Exit(1)
		}

		global.DBConnection = &utils.Database{DB: sqlDB.DB}
	}

	pw, err := playwright.Run()
	if err != nil {
		global.Logger.Error("cannot start playwright", slog.String("error", err.Error()))
		os.Exit(1)
	}

	var browser playwright.Browser
	switch global.Browser {
	case "chromium":
		browser, err = pw.Chromium.Launch(playwright.BrowserTypeLaunchOptions{
			Headless: playwright.Bool(global.Headless),
		})
	case "firefox":
		browser, err = pw.Firefox.Launch(playwright.BrowserTypeLaunchOptions{
			Headless: playwright.Bool(global.Headless),
		})
	case "webkit":
		browser, err = pw.WebKit.Launch(playwright.BrowserTypeLaunchOptions{
			Headless: playwright.Bool(global.Headless),
		})
	}

	if err != nil {
		global.Logger.Error("could not launch browser", slog.String("error", err.Error()))
		os.Exit(1)
	}

	defer func() {
		err := browser.Close()
		if err != nil {
			global.Logger.Error("could not close browser", slog.String("error", err.Error()))
		}

		err = pw.Stop()
		if err != nil {
			global.Logger.Error("could not stop playwright", slog.String("error", err.Error()))
		}
	}()

	jobs := make(chan cl.Job, len(global.Location))
	completed := make(chan cl.Job, len(global.Location))

	for w := 1; w <= global.MaximumWorkers; w++ {
		go worker(jobs, completed, browser)
	}

	for _, url := range global.Location {
		jobs <- cl.Job{
			Url: url,
		}
	}
	close(jobs)

	for range len(global.Location) {
		job := <-completed
		if job.Err != nil {
			global.Logger.Warn("an error occurred while processing", slog.String("url", job.Url), slog.String("error", job.Err.Error()))
			continue
		}

		result := job.Results
		global.Logger.Info("completed gathering results", slog.String("url", job.Url), slog.Int("results", len(result)))

		switch global.WriteAs {
		case "csv":
			err = result.ResultsToCSV(global.Output)
			if err != nil {
				global.Logger.Warn("an error occurred while writing to csv", slog.String("error", err.Error()))
			}
		case "sqlite":
			db := &writer.Database{DB: global.DBConnection.DB}
			err = db.WriteAll(result)
			if err != nil {
				global.Logger.Warn("an error occurred while writing to db", slog.String("error", err.Error()))
			}
		}
	}
}

// should print the number of jobs that will be completed
func worker(jobs <-chan cl.Job, completed chan<- cl.Job, browser playwright.Browser) {
	for job := range jobs {
		global.Logger.Info("starting to scrape", slog.String("url", job.Url))

		err := cl.StartJob(browser, &job)
		if err != nil {
			job.Err = err
		}

		completed <- job
	}
}

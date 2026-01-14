package writer

import (
	"encoding/csv"
	"log/slog"
	"os"

	"github.com/gavink97/cl-search/internal/global"
)

func (r *GalleryResult) ToCSV(output string) error {
	f, err := os.OpenFile(output, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0600)
	if err != nil {
		return err
	}

	defer func() {
		err = f.Close()
		if err != nil {
			global.Logger.Warn("unable to close file", slog.String("file", output), slog.String("error", err.Error()))
		}
	}()

	writer := csv.NewWriter(f)

	if global.NewCSV {
		header := []string{"Id", "Title", "Date", "Location", "Price", "Timestamp", "Source", "Url", "Images"}
		err := writer.Write(header)
		if err != nil {
			global.Logger.Error("an error occurred writing csv header", slog.String("error", err.Error()))
		} else {
			global.NewCSV = false
		}
	}

	table := []string{r.Id, r.Title, r.Date, r.Location, r.Price, r.TimeStamp.String(), r.Source, r.Url}

	table = append(table, r.Images...)

	err = writer.Write(table)
	if err != nil {
		global.Logger.Error("an error occurred writing csv row", slog.String("error", err.Error()))
	}

	writer.Flush()

	return nil
}

func (res *GalleryResults) ResultsToCSV(output string) error {
	f, err := os.OpenFile(output, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0600)
	if err != nil {
		return err
	}

	defer func() {
		err = f.Close()
		if err != nil {
			global.Logger.Warn("unable to close file", slog.String("file", output), slog.String("error", err.Error()))
		}
	}()

	writer := csv.NewWriter(f)

	if global.NewCSV {
		header := []string{"Id", "Title", "Date", "Location", "Price", "Timestamp", "Source", "Url", "Images"}
		err := writer.Write(header)
		if err != nil {
			global.Logger.Error("an error occurred writing csv header", slog.String("error", err.Error()))
		} else {
			global.NewCSV = false
		}
	}

	for _, r := range *res {
		table := []string{r.Id, r.Title, r.Date, r.Location, r.Price, r.TimeStamp.String(), r.Source, r.Url}

		table = append(table, r.Images...)

		err = writer.Write(table)
		if err != nil {
			global.Logger.Error("an error occurred writing csv row", slog.String("error", err.Error()))
		}

		writer.Flush()

	}

	return nil
}

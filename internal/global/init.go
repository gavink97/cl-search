package global

import (
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
	"path"
	"strings"
)

type Locations map[string]Country
type Country map[string]Territory
type Territory map[string]Locality

type Locality struct {
	Local string `json:"local"`
	Url   string `json:"url"`
}

func SetDefaultLogger() {
	options := &slog.HandlerOptions{
		Level: ProgramLevel,
	}

	ProgramLevel.Set(slog.LevelInfo)
	Logger = slog.New(slog.NewTextHandler(os.Stderr, options))
	slog.SetDefault(Logger)
}

func CheckFiles() bool {
	_, err := os.Stat(path.Join(DATA_HOME, "locations.json"))
	return err == nil
}

func GenerateLocations() error {
	res, err := http.Get("https://craigslist.org/sitemap.html")
	if err != nil {
		return err
	}

	defer func() {
		err := res.Body.Close()
		Logger.Error("could not close response body", slog.String("error", err.Error()))
	}()

	body, err := io.ReadAll(res.Body)
	if res.StatusCode > 299 {
		Logger.Debug("response", slog.String("body", string(body)))
		return fmt.Errorf("response failed with status code: %d", res.StatusCode)
	}

	if err != nil {
		return err
	}

	locations := make(Locations)
	countries := strings.Split(string(body), "</blockquote>")

	for i, c := range countries[:len(countries)-1] {
		var idx int
		if i == 0 {
			idx = strings.Index(c, "</h1>") + 5
		}

		idx2 := strings.Index(c, "<blockquote>")

		countryName := strings.ToLower(strings.TrimSpace(c[idx:idx2]))

		if _, exists := locations[countryName]; !exists {
			locations[countryName] = make(Country)
		}

		territories := strings.Split(c, "</ul>")

		for j, t := range territories[:len(territories)-1] {
			var idx int
			if j == 0 {
				idx = strings.Index(t, "<blockquote>") + 12
			}

			idx2 := strings.Index(t, "<ul>")

			territoryName := strings.ToLower(strings.TrimSpace(t[idx:idx2]))

			if _, exists := locations[countryName][territoryName]; !exists {
				locations[countryName][territoryName] = make(Territory)
			}

			localities := strings.Split(t, "</li>")

			for _, l := range localities[:len(localities)-1] {
				idx = strings.Index(l, "<li>") + 4
				splts := strings.Split(l[idx:], `"`)

				localName := strings.TrimSpace(strings.TrimPrefix(splts[2], ">"))
				cleanLocalName := strings.ToLower(localName[:len(localName)-4])
				url := strings.ToLower(strings.TrimSpace(splts[1]))

				local := Locality{
					Local: cleanLocalName,
					Url:   url[:len(url)-13],
				}

				locations[countryName][territoryName][cleanLocalName] = local
			}
		}
	}

	data, err := json.MarshalIndent(locations, "", "  ")
	if err != nil {
		return err
	}

	err = os.MkdirAll(DATA_HOME, 0755)
	if err != nil {
		return err
	}

	err = os.WriteFile(path.Join(DATA_HOME, "locations.json"), data, 0644)
	if err != nil {
		return err
	}

	return nil
}

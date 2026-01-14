package parser

import (
	"fmt"
	"log/slog"
	"os"
	"path"
	"strings"
	"time"

	"github.com/gavink97/cl-search/internal/global"
	"github.com/gavink97/cl-search/internal/utils"
	"github.com/gavink97/cl-search/internal/writer"
	"github.com/playwright-community/playwright-go"
)

func Parse(entry playwright.Locator) writer.GalleryResult {
	id, err := entry.GetAttribute("data-pid")
	if err != nil {
		global.Logger.Debug("An error occurred when getting id", slog.String("error", err.Error()))
	}

	if id == "" {
		return writer.GalleryResult{}
	}

	title, err := entry.Locator("span.label").TextContent()
	if err != nil {
		global.Logger.Debug("An error occurred when getting title", slog.String("error", err.Error()))
	}

	var price string

	isPrice, err := entry.Locator("span.priceinfo").IsVisible()
	if err != nil {
		global.Logger.Debug("An error occurred when getting price", slog.String("error", err.Error()))
	}

	if isPrice {
		price, err = entry.Locator("span.priceinfo").TextContent()
		if err != nil {
			global.Logger.Debug("An error occurred when getting price", slog.String("error", err.Error()))
			price = ""
		}
	}

	meta, err := entry.Locator("div.meta").InnerHTML()
	if err != nil {
		global.Logger.Debug("An error occurred when getting meta", slog.String("error", err.Error()))
	}

	md := strings.Split(meta, `<span class="separator"></span>`)

	var date string
	var location string
	// log info if no location

	switch len(md) {
	case 1:
		date = md[0]
	case 2:
		date = md[0]
		location = md[1]
	case 3:
		date = md[0]
		location = md[2]
	default:
		global.Logger.Debug("unknown meta length", slog.Int("length", len(md)), slog.String("meta", meta))
	}

	url, err := entry.Locator("a.main").GetAttribute("href")
	if err != nil {
		global.Logger.Debug("An error occurred when getting url", slog.String("error", err.Error()))
	}

	var images []string

	et := utils.EntryType(entry)
	switch et {
	case "single":
		a, err := entry.Locator("img").GetAttribute("src")
		if err != nil {
			global.Logger.Debug("An error occurred when getting image", slog.String("error", err.Error()))
		}

		image := strings.Replace(a, "300x300", "600x450", 1)
		images = append(images, image)

	case "gallery":
		imgs, err := entry.Locator("img").All()
		if err != nil {
			global.Logger.Debug("An error occurred when getting images", slog.String("error", err.Error()))
		}

		for _, src := range imgs {
			srcHtml, err := src.InnerHTML()
			if err != nil {
				global.Logger.Debug("An error occurred when getting image innerHTML", slog.String("error", err.Error()))
				continue
			}

			if strings.Contains(srcHtml, `data-cloned="true"`) {
				continue
			}

			a, err := src.GetAttribute("src")
			if err != nil {
				global.Logger.Debug("An error occurred when getting image src", slog.String("error", err.Error()))
				continue
			}

			image := strings.Replace(a, "300x300", "600x450", 1)
			images = append(images, image)
		}
	default:
		images = append(images, "")
	}

	if global.DownloadImages {
		for _, img := range images {
			if !strings.Contains(img, "http") {
				continue
			}

			imgDir := path.Join(path.Dir(global.Output), "images")

			err = os.MkdirAll(imgDir, 0755)
			if err != nil {
				global.Logger.Error("unable to make image directory", slog.String("error", err.Error()))
			}

			global.Logger.Debug("downloading image", slog.String("image", img))

			splts := strings.Split(img, "/")

			errs := make(chan error, 1)
			go func() {
				errs <- utils.Download(img, path.Join(imgDir, fmt.Sprintf("%s_%s", splts[len(splts)-2], splts[len(splts)-1])))
			}()

			if err := <-errs; err != nil {
				global.Logger.Error("an error occurred downloading image", slog.String("image", img), slog.String("error", err.Error()))
			}
		}
	}

	return writer.GalleryResult{
		Id:        id,
		Title:     title,
		Price:     price,
		Location:  location,
		Date:      date,
		Url:       url,
		TimeStamp: time.Now().In(global.TZ),
		Images:    images,
	}
}

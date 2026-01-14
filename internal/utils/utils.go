package utils

import (
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/playwright-community/playwright-go"
)

func EntryType(entry playwright.Locator) string {
	gallery, err := entry.Locator("div.cl-gallery").GetAttribute("class")
	if err != nil {
		log.Printf("An error occurred getting the gallery: %v", err)
		return ""
	}

	if strings.Contains(gallery, "empty") {
		return "empty"
	}

	swipe, err := entry.Locator("div.swipe").Count()
	if err != nil {
		return "single"
	}

	if swipe > 0 {
		return "gallery"
	} else {
		return "single"
	}
}

func ViewMode(page playwright.Page) bool {
	class, err := page.Locator("html").First().GetAttribute("class")
	if err != nil {
		log.Printf("An error occurred when getting html: %v", err)
	}

	isGallery := strings.Contains(class, "cl-search-view-mode-gallery")
	if !isGallery {
		err = page.Locator("button.cl-search-view-mode-gallery").Click()
		if err != nil {
			log.Fatalf("An error clicking the gallery view button: %v", err)
		}
		return false
	}

	return true
}

func Download(url string, filepath string) error {
	out, err := os.Create(filepath)
	if err != nil {
		return err
	}

	defer func() {
		err := out.Close()
		if err != nil {
			log.Printf("an error occurred closing file: %s: %v\n", filepath, err)
		}
	}()

	res, err := http.Get(url)
	if err != nil {
		return err
	}

	defer func() {
		err := res.Body.Close()
		if err != nil {
			log.Printf("an error occurred closing result body: %s: %v\n", url, err)
		}
	}()

	_, err = io.Copy(out, res.Body)
	if err != nil {
		return err
	}

	return nil
}

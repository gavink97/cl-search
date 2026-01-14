package cl

import (
	"fmt"
	"log/slog"
	"strconv"
	"strings"
	"time"

	"github.com/gavink97/cl-search/internal/global"
	"github.com/gavink97/cl-search/internal/parser"
	"github.com/gavink97/cl-search/internal/utils"
	"github.com/gavink97/cl-search/internal/writer"
	"github.com/playwright-community/playwright-go"
)

type Job struct {
	Url     string
	Err     error
	Results writer.GalleryResults
}

func StartJob(browser playwright.Browser, job *Job) error {
	userAgent := global.UserAgent
	if userAgent == "" {
		userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0"
	}

	context, err := browser.NewContext(playwright.BrowserNewContextOptions{
		UserAgent: &userAgent,
		Viewport: &playwright.Size{
			Width:  1400,
			Height: 900,
		},
	})

	if err != nil {
		return fmt.Errorf("could not create context: %w", err)
	}

	defer func() {
		err := context.Close()
		if err != nil {
			global.Logger.Error("could not close playwright context", slog.String("error", err.Error()))
		}
	}()

	page, err := context.NewPage()
	if err != nil {
		return fmt.Errorf("could not create page: %v", err)
	}

	query := global.Query
	category := global.Category
	qsplits := strings.Split(query, " ")

	var b strings.Builder

	for i, v := range qsplits {
		if i == len(qsplits) {
			b.WriteString(v)
		} else {
			fmt.Fprintf(&b, "%s%s", v, "%20")
		}
	}

	url := fmt.Sprintf("%s/search/%s?query=%s", job.Url, category, b.String())

	_, err = page.Goto(url, playwright.PageGotoOptions{
		WaitUntil: playwright.WaitUntilStateNetworkidle,
	})

	if err != nil {
		return fmt.Errorf("could not goto: %v", err)
	}

	res := job.processResults(page)
	if res == nil {
		return fmt.Errorf("could not process results")
	}

	job.Results = res

	return nil
}

func (job *Job) processResults(page playwright.Page) writer.GalleryResults {
	if !utils.ViewMode(page) {
		err := page.WaitForLoadState(playwright.PageWaitForLoadStateOptions{
			State: playwright.LoadStateNetworkidle,
		})

		if err != nil {
			global.Logger.Error("an error occurred waiting for network idle", slog.String("error", err.Error()))
		}
	}

	counts, err := page.Locator("div.visible-counts").First().TextContent()
	if err != nil {
		global.Logger.Error("an error occurred getting result count", slog.String("error", err.Error()))
		return nil
	}

	splts := strings.Split(counts, "of")
	if len(splts) < 2 {
		return nil
	}

	listingCount, err := strconv.Atoi(strings.TrimSpace(splts[1]))
	if err != nil {
		global.Logger.Error("could not convert result count to integer", slog.String("error", err.Error()))
		return nil
	}

	var results writer.GalleryResults
	count := 1
	var dataIndex int

	for (dataIndex*100 + count) < listingCount {
		if count > 100 {
			dataIndex++
			count = 1
		}

		renx := fmt.Sprintf("//div[contains(@class, 'results-rendered') and @data-index='%d']", dataIndex)
		resx := fmt.Sprintf("/following-sibling::div[contains(@class, 'cl-search-result')][%d]", count)
		xpath := strings.Join([]string{renx, resx}, "")
		result := page.Locator(xpath).First()

		resultHtml, err := result.InnerHTML()
		if err != nil {
			global.Logger.Error("unable to get result inner HTML", slog.String("error", err.Error()))
			count++
			continue
		}

		if strings.Contains(resultHtml, `class="gallery-card spacer"`) {
			count++
			continue
		}

		viz, err := result.IsVisible()
		if err != nil {
			global.Logger.Error("an error occurred checking if the result was in view", slog.String("error", err.Error()))
		}

		for !viz {
			err := result.ScrollIntoViewIfNeeded()
			if err != nil {
				global.Logger.Error("an error occurred scrolling result into view", slog.String("error", err.Error()))
			}

			// should probably change to waitFor LoadStateNetworkidle
			time.Sleep(time.Duration(500) * time.Millisecond)

			viz, err = result.IsVisible()
			if err != nil {
				global.Logger.Error("an error occurred checking if the result was in view", slog.String("error", err.Error()))
			}
		}

		if strings.Contains(resultHtml, `class="swipe"`) {
			err = result.Hover(playwright.LocatorHoverOptions{
				Position: &playwright.Position{
					X: float64(14),
					Y: float64(190),
				},
			})
			if err != nil {
				global.Logger.Error("an error occurred hovering the result", slog.String("error", err.Error()))
			}

			err = result.Click(playwright.LocatorClickOptions{
				Position: &playwright.Position{
					X: float64(14),
					Y: float64(190),
				},
			})

			if err != nil {
				global.Logger.Error("an error occurred clicking the result gallery", slog.String("error", err.Error()))
			}
		}

		r := parser.Parse(result)
		if r.Id == "" {
			continue
		}

		r.Source = job.Url
		results = append(results, r)

		count++
		time.Sleep(time.Duration(250) * time.Millisecond)
	}

	return results
}

package writer

import (
	"time"

	"gorm.io/gorm"
)

type GalleryResult struct {
	Id        string
	Title     string
	Price     string
	Location  string
	Date      string
	Url       string
	TimeStamp time.Time
	Source    string
	Images    []string
}

type GalleryResults []GalleryResult

type Database struct {
	DB *gorm.DB
}

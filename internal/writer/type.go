package writer

import (
	"time"

	"github.com/gavink97/cl-search/internal/global"
	"gorm.io/gorm"
)

type GalleryResult struct {
	Id        string
	Title     string
	Price     string
	Location  string
	Date      string
	PostDate  *time.Time
	Url       string
	TimeStamp time.Time
	Source    global.Loc
	Images    []string
}

type GalleryResults []GalleryResult

type Database struct {
	DB *gorm.DB
}

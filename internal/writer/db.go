package writer

import (
	"fmt"
	"log/slog"
	"os"
	"strconv"

	"github.com/gavink97/cl-search/internal/global"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func open(dbName string) (*gorm.DB, error) {
	err := os.MkdirAll("/tmp", 0755)
	if err != nil {
		return nil, err
	}

	return gorm.Open(sqlite.Open(dbName), &gorm.Config{})
}

func MustOpen(dbName string) *Database {
	if dbName == "" {
		dbName = "output.db"
	}

	db, err := open(dbName)
	if err != nil {
		panic(err)
	}

	err = db.AutoMigrate()
	if err != nil {
		panic(err)
	}

	return &Database{DB: db}
}

func (d *Database) CreateTables() error {
	err := d.DB.Exec("PRAGMA foreign_keys = ON").Error
	if err != nil {
		return err
	}

	err = d.DB.AutoMigrate(
		&Source{},
		&Item{},
		&SourceItem{},
		&ItemImage{},
	)

	return err
}

func (d *Database) Insert(data GalleryResult) error {
	source := Source{Source: data.Source}

	err := d.DB.Where(source).FirstOrCreate(&source).Error
	if err != nil {
		return err
	}

	id, err := strconv.Atoi(data.Id)
	if err != nil {
		return fmt.Errorf("an error occurred converting the id to int: %w", err)
	}

	item := Item{
		DataId:    id,
		Title:     data.Title,
		Date:      data.Date,
		Location:  &data.Location,
		Price:     &data.Price,
		TimeStamp: data.TimeStamp,
		Url:       data.Url,
	}

	err = d.DB.Where(Item{DataId: id}).FirstOrCreate(&item).Error
	if err != nil {
		return err
	}

	sourceItem := SourceItem{
		ItemId:   item.ID,
		SourceId: source.ID,
	}

	err = d.DB.Where(sourceItem).FirstOrCreate(&sourceItem).Error
	if err != nil {
		return err
	}

	for _, img := range data.Images {
		image := ItemImage{
			ItemId: item.ID,
			Url:    img,
		}

		err = d.DB.Where(image).FirstOrCreate(&image).Error
		if err != nil {
			global.Logger.Warn("could not insert image", slog.String("image", img), slog.String("error", err.Error()))
			continue
		}
	}

	return nil
}

func (d *Database) WriteAll(results GalleryResults) error {
	for _, result := range results {
		err := d.Insert(result)
		if err != nil {
			return err
		}
	}
	return nil
}

func (d *Database) Close() error {
	sql, err := d.DB.DB()
	if err != nil {
		return err
	}

	return sql.Close()
}

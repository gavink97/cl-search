package writer

import "time"

type Source struct {
	ID     int    `gorm:"primaryKey;column:id"`
	Source string `gorm:"unique;column:source"`
}

type Item struct {
	ID        int       `gorm:"primaryKey;column:id"`
	DataId    int       `gorm:"unique;column:data_id;size:255"`
	Title     string    `gorm:"column:title;size:500"`
	Date      string    `gorm:"column:date;size:255"`
	Location  *string   `gorm:"column:location;size:255"`
	Price     *string   `gorm:"column:price;size:255"`
	TimeStamp time.Time `gorm:"column:timestamp"`
	Url       string    `gorm:"column:url;size:500"`
}

type SourceItem struct {
	ID       int    `gorm:"primaryKey;column:id"`
	ItemId   int    `gorm:"column:item_id"`
	SourceId int    `gorm:"column:source_id"`
	Item     Item   `gorm:"foreignKey:ItemId;references:ID;constraint:OnDelete:CASCADE"`
	Source   Source `gorm:"foreignKey:SourceID;references:ID"`
}

type ItemImage struct {
	ID     int    `gorm:"primaryKey;column:id"`
	ItemId int    `gorm:"column:item_id"`
	Url    string `gorm:"column:url;size:500"`
	Item   Item   `gorm:"foreignKey:ItemId;references:ID;constraint:OnDelete:CASCADE"`
}

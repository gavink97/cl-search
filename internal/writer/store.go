package writer

import "time"

type Source struct {
	ID   int    `gorm:"primaryKey;column:id"`
	Name string `gorm:"unique;column:name"`
	Url  string `gorm:"unique;column:url"`
}

type Country struct {
	ID      int    `gorm:"primaryKey;column:id"`
	Country string `gorm:"unique;column:country"`
}

type Territory struct {
	ID        int     `gorm:"primaryKey;column:id"`
	Territory string  `gorm:"column:territory"`
	CountryId int     `gorm:"column:country_id"`
	Country   Country `gorm:"foreignKey:CountryId;references:ID"`
}

type Local struct {
	ID          int       `gorm:"primaryKey;column:id"`
	Local       string    `gorm:"column:local"`
	Url         string    `gorm:"unique;column:url"`
	CountryId   int       `gorm:"column:country_id"`
	TerritoryId int       `gorm:"column:territory_id"`
	Country     Country   `gorm:"foreignKey:CountryId;references:ID"`
	Territory   Territory `gorm:"foreignKey:TerritoryId;references:ID"`
}

type Item struct {
	ID        int        `gorm:"primaryKey;column:id"`
	DataId    int        `gorm:"unique;column:data_id;size:255"`
	Title     string     `gorm:"column:title;size:500"`
	Date      *string    `gorm:"column:date;size:255"`
	PostDate  *time.Time `gorm:"column:post_date"`
	Location  *string    `gorm:"column:location;size:255"`
	Price     *string    `gorm:"column:price;size:255"`
	TimeStamp time.Time  `gorm:"column:timestamp"`
	Url       string     `gorm:"column:url;size:500"`
}

type SourceItem struct {
	ID       int    `gorm:"primaryKey;column:id"`
	ItemId   int    `gorm:"column:item_id"`
	SourceId int    `gorm:"column:source_id"`
	LocalId  int    `gorm:"column:local_id"`
	Item     Item   `gorm:"foreignKey:ItemId;references:ID;constraint:OnDelete:CASCADE"`
	Source   Source `gorm:"foreignKey:SourceId;references:ID"`
	Local    Local  `gorm:"foreignKey:LocalId;references:ID"`
}

type ItemImage struct {
	ID     int    `gorm:"primaryKey;column:id"`
	ItemId int    `gorm:"column:item_id"`
	Url    string `gorm:"column:url;size:500"`
	Item   Item   `gorm:"foreignKey:ItemId;references:ID;constraint:OnDelete:CASCADE"`
}

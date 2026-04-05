package parser

import (
	"os"
	"testing"
	"time"

	"github.com/gavink97/cl-search/internal/global"
)

func TestMain(m *testing.M) {
	global.SetDefaultLogger()
	exitVal := m.Run()

	os.Exit(exitVal)
}

func TestParseDate(t *testing.T) {
	expected := "2026-03-13"

	sample := "3/13"

	result, err := ParseDate(sample)
	if err != nil {
		t.Error(err)
	}

	if result.Format("2006-01-02") != expected {
		t.Errorf("Incorrect Result: \nresult: %v \nexpected: %v", result, expected)
	}

	expected = "25-12-25"

	sample = "12/25"

	result, err = ParseDate(sample)
	if err != nil {
		t.Error(err)
	}

	if result.Format("06-1-2") != expected {
		t.Errorf("Incorrect Result: \nresult: %v \nexpected: %v", result, expected)
	}

	format := "2006-Jan-02 03:04"

	expected = time.Now().In(global.TZ).Add(time.Duration(-1) * time.Hour).Format(format)

	sample = "<1hr ago"

	result, err = ParseDate(sample)
	if err != nil {
		t.Error(err)
	}

	if result.Format(format) != expected {
		t.Errorf("Incorrect Result: \nresult: %v \nexpected: %v", result, expected)
	}

	expected = time.Now().In(global.TZ).Add(time.Duration(-8) * time.Hour).Format(format)

	sample = "8h ago"

	result, err = ParseDate(sample)
	if err != nil {
		t.Error(err)
	}

	if result.Format(format) != expected {
		t.Errorf("Incorrect Result: \nresult: %v \nexpected: %v", result, expected)
	}

	expected = "26-03-12"
	sample = "3/12,3/13,3/14"

	result, err = ParseDate(sample)
	if err != nil {
		t.Error(err)
	}

	if result.Format("06-01-02") != expected {
		t.Errorf("Incorrect Result: \nresult: %v \nexpected: %v", result, expected)
	}
}

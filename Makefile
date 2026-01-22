.PHONY: run
run:
	go run cmd/cl-search/main.go "us.tx" "record players" "output.csv"

.PHONY: test
test:
	go test ./...

.PHONY: build
build:
	goreleaser release --clean --snapshot

.PHONY: build-darwin
build-darwin:
	GOOS=darwin GOARCH=arm64 CGO_ENABLED=1 go build cmd/cl-search/main.go

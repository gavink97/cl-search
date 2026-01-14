.PHONY: run
run:
	go run cmd/cl-search/main.go "austin" "record players" "output.db"

.PHONY: test
test:
	go test ./...

.PHONY: build
build:
	goreleaser release --clean

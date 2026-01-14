.PHONY: run
run:
	go run cmd/cl-search/main.go "austin" "record players" "output.db"

.PHONY: test
test:
	go test ./...

.PHONY: build
build:
	SDK_PATH=$(xcrun --show-sdk-path) goreleaser release --clean

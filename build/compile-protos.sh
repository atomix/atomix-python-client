#!/bin/sh

proto_imports="./build/api/proto:${GOPATH}/src/github.com/gogo/protobuf/protobuf:${GOPATH}/src/github.com/gogo/protobuf:${GOPATH}/src"

git clone --branch master https://github.com/atomix/api.git build/api

mkdir -p build/gen

protoc -I=$proto_imports --python_betterproto_out=build/gen \
  build/api/proto/atomix/membership/*.proto \
  build/api/proto/atomix/database/*.proto \
  build/api/proto/atomix/primitive/*.proto \
  build/api/proto/atomix/session/*.proto \
  build/api/proto/atomix/election/*.proto \
  build/api/proto/atomix/indexedmap/*.proto \
  build/api/proto/atomix/leader/*.proto \
  build/api/proto/atomix/list/*.proto \
  build/api/proto/atomix/lock/*.proto \
  build/api/proto/atomix/log/*.proto \
  build/api/proto/atomix/map/*.proto \
  build/api/proto/atomix/set/*.proto \
  build/api/proto/atomix/value/*.proto

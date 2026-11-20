# Dockerfile for IAM Service
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY iam_service/go.mod iam_service/go.sum ./
RUN go mod download

COPY iam_service/ .
RUN CGO_ENABLED=0 GOOS=linux go build -o iam-service .

FROM alpine:latest
RUN apk --no-cache add ca-certificates \
    && addgroup -S -g 10001 app \
    && adduser -S -u 10001 -G app -H -D -s /sbin/nologin app
WORKDIR /app
COPY --from=builder /app/iam-service .
USER app
CMD ["./iam-service"]

FROM python:3.9-slim as base
# NOTE: When using COPY, the build context is the root directory.

# K8s commands will use this entry point
ENTRYPOINT ["python"]
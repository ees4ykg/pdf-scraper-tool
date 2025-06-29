# Use AWS Lambda Python base image with Amazon Linux 2023 (has newer GCC)
FROM public.ecr.aws/lambda/python:3.12

# Install system dependencies and build tools required for PyMuPDF and other common libraries
# Note: Amazon Linux 2023 has different package names than AL2
RUN dnf update -y && \
    dnf install -y \
        gcc \
        gcc-c++ \
        make \
        wget \
        tar \
        python3-devel \
        libjpeg-turbo-devel \
        harfbuzz-devel \
        openjpeg2-devel \
        swig \
        freetype-devel \
        libffi-devel \
        && dnf clean all

# IMPORTANT: Remove PyMuPDF from your requirements.txt.
# We will install it directly from source to ensure consistency.
# If PyMuPDF is in requirements.txt, pip will try to install it again,
# potentially leading to conflicts or trying to fetch a pre-compiled wheel that
# might not be compatible or trigger another source build attempt.

# Install PyMuPDF using pip (the recommended way)
# Ensure pip is up-to-date before installing PyMuPDF
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade pymupdf

# Copy requirements.txt and install other dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
# Install remaining dependencies from requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

# Set the Lambda handler
CMD ["lambda_function.lambda_handler"]
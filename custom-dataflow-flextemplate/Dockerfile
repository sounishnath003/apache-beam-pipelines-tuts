# Use the base image for Dataflow Python SDK
FROM gcr.io/dataflow-templates-base/python311-template-launcher-base

# Set the working directory inside the container
ARG WORKDIR=/dataflow/template
ENV WORKDIR=${WORKDIR}

RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get -y upgrade
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project code to the working directory
COPY . ${WORKDIR}

# Set the environment variables for Dataflow
ENV PYTHONPATH="${WORKDIR}/appp:${PYTHONPATH}"
ENV RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/appp/main.py"

# Build the package and install it
RUN python -m build --sdist && pip install dist/*.tar.gz

# Since we already downloaded all the dependencies, there's no need to rebuild everything.
ENV PIP_NO_DEPS=True


# Set the entrypoint to the Dataflow template launcher
ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]

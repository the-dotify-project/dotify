FROM gitpod/workspace-full

ENV POETRY_VERSION 1.1.6
ENV PATH "${HOME}/.poetry/bin:${PATH}"
ENV PIP_USER "false"

RUN sudo apt-get update \
    && sudo apt-get install -y \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

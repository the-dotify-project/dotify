FROM gitpod/workspace-full

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PATH "${HOME}/.poetry/bin:${PATH}"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - \
    && poetry config virtualenvs.create "true" \
    && poetry config virtualenvs.in-project "true" \
    && pyenv update \
    && pyenv install -s 3.7.10 \
    && pyenv install -s 3.8.9 \
    && pyenv install -s 3.9.4 \
    && pyenv local 3.7.10 3.8.9 3.9.4 \
    && if ! grep -q "export PIP_USER=no" "$HOME/.bashrc"; then printf '%s\n' "export PIP_USER=no" >> "$HOME/.bashrc"; fi

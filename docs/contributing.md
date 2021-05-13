# Contributing

Hello and thank you for considering contributing to **Dotify**!

Reading and following these guidelines will help us make the contribution process easy and effective for everyone involved.

This project follows the [all-contributors](https://allcontributors.org/) specification. You can read more [here](https://allcontributors.org/docs/en/bot/usage).

## Code of Conduct

By participating and contributing to this project, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Help

In case all you need is an answer to a question, please refrain from opening an issue and instead visit the project's [discussion page](https://github.com/the-dotify-project/dotify/discussions/categories/q-a).

## Getting Started

Contributions are made to this repository via Issues and Pull Requests (PRs). A few general guidelines that cover both:

- Search for existing Issues and PRs before creating your own.
- We work hard to make sure issues are handled in a timely manner but, depending on the impact, it could take a while to investigate the root cause. A friendly ping in the comment thread to the submitter or a contributor can help draw attention if your issue is blocking.

### Issues

Issues should be used to report problems with the library or request a new feature or documentation change. When you create a new Issue, a template will be loaded that will guide you through collecting and providing the required information.

If you find an Issue that addresses the problem you're having, please add your own reproduction information to the existing issue rather than creating a new one. Adding a [reaction](https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) can also help in indicating to our maintainers that a particular problem is affecting more than just the reporter.

### Pull Requests

PRs can be a quick way to get your fix or improvement slated for the next release. In general, PRs should:

- Only fix/add the functionality in question **OR** address wide-spread whitespace/style issues, not both.
- Address a single concern in the least number of changed lines as possible.
- Be accompanied by a complete Pull Request template (loaded automatically when a PR is created).
- Add [unit or integration tests](/tests) for added or changed functionality.
- Any code related changes should be accompanied by corresponding changes to the project's documentation.
- If your pull request introduces a new feature, the corresponding `README` [section](/README.md#features) must be updated to reflect this. Make sure you also include [an example](/examples), showcasing this new functionality.
- Write clear, concise commit message(s) using [conventional-changelog format](https://github.com/conventional-changelog/conventional-changelog-angular/blob/master/convention.md). [Why?](#writing-your-commit-message)
- If your PR is connected to an open issue, add a line in your PR's description that says `Fixes: #123`, where `#123` is the number of the issue you're fixing.

For changes that address core functionality or would require breaking changes (e.g. a major release), it's best to open an Issue to discuss your proposal first. This is not required but can save time creating and reviewing changes.

In general, we follow the ["fork-and-pull" Git workflow](https://github.com/susam/gitpr)

1. Fork the repository to your own Github account
2. Clone the project to your machine
3. Create a branch locally with a succinct but descriptive name
4. Commit changes to the branch
5. Push changes to your fork
6. [Open a PR in our repository](https://github.com/the-dotify-project/dotify/compare) and follow the PR template so that we can efficiently review the changes

## Setting up a local development environment

The following sections assume that you have already locally [cloned the repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

### Installing Poetry

The **Dotify** project utilizes the [Poetry](https://python-poetry.org/) Python package manager. [Having installed Poetry](https://python-poetry.org/docs/#installation) in the **global** namespace you may now run `poetry shell` to create a brand new [virtual environment](https://docs.python.org/3/tutorial/venv.html) and `poetry install`, in order to install the project's dependencies (development dependencies as well).

### Creating & Using Spotify client credentials

Start by visiting the [Spotify Developer Portal](https://developer.spotify.com/dashboard/login) and creating an account. You are also required to [create a Spotify client ID](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app), which you will be using during development. You may reed more [here](https://developer.spotify.com/documentation/web-api/quick-start/).

You can either export the required variables as such

```bash
export SPOTIFY_ID="<SPOTIFY_ID>"
export SPOTIFY_SECRET="<SPOTIFY_SECRET>"
```

or you may also create a a JSON file, of the following format, in the project's root directory.

```json
{
    "spotify_id": "<SPOTIFY_ID>",
    "spotify_secret": "<SPOTIFY_SECRET>"
}
```

_**ATTENTION**: Even though, using a JSON file is far more convenient than re-exporting  environment variables each and every time you open up a new shell, it is **strongly** recommended that, you prefer the first approach as you risk compromising your client credentials otherwise._

### Installing pre-commit hooks

The project utilizes the [pre-commit](https://pre-commit.com/) framework. Having [created a virtual environment and installed the required dependencies](#installing-poetry), you may run `pre-commit install` to install the [git hook scripts](/.pre-commit-config.yaml).

### Formatting, Linting and Testing

All of the above can be done via [tox](https://tox.readthedocs.io/en/latest/config.html):

- You can lint the code by simply running `tox -e lint`
- Checking for type errors, using [Mypy](https://mypy.readthedocs.io/en/stable/), can be achieved via `tox -e type-check`
- Checking if your changes follow the project's formatting standard can be done via `tox -e fmt-check`
- You may run `tox -e py38` in order to run the library's unit tests using Python 3.8 (the `py37`, `py38` and `py39` test environments assumes that you have **Python 3.7, 3.8 or 3.9** installed)
- Alternatively, you may simply run `tox` to execute all of the above

#### (Optional) Installing pyenv

[pyenv](https://github.com/pyenv/pyenv) is used, in the context of the **Dotify** project, in order to determine the project's compatibility with various versions of Python. Installing `pyenv` is not strictly required, but it is **strongly** recommended.

Having installed `pyenv` in the **global** namespace, you may now run the following snippet, in order to install Python 3.7, 3.8 and 3.9, which, at the time of writing this document, are the only Python versions, supported by **Dotify**.

```bash
pyenv install 3.7.10 3.8.9 3.9.4
pyenv local 3.7.10 3.8.9 3.9.4
```

You will now be able to run `tox` (an as a result any test environment subset `py3[7|8|9]`), without any test environment being skipped due to [skip_missing_interpreters](https://tox.readthedocs.io/en/latest/config.html#conf-skip_missing_interpreters).

Feel free to read more about using `pyenv`, in the context of `poetry`, [here](https://blog.jayway.com/2019/12/28/pyenv-poetry-saviours-in-the-python-chaos/).

### Documenting your changes

**Dotify** utilizes [MkDocs](https://www.mkdocs.org/) to build and deploy its documentation to [GitHub Pages](https://pages.github.com/). The documentation is auto-generated from the [python docstrings](https://www.python.org/dev/peps/pep-0257/#id15) throughout the source code. As a result, any code related change should be accompanied by a corresponding change to the method / class at hand.

Having made your changes, please run `mkdocs server` and make sure that no error is being raised and the documentation renders fine.

### Writing your commit message

The project's version number and [Changelog](/CHANGELOG.md), depend on a consistent commit history. As a result, your commit message's format is extremely important. Before opening a pull request, please make sure that your commits strictly follow the [conventional-changelog format](https://github.com/conventional-changelog/conventional-changelog-angular/blob/master/convention.md).

### Creating a pull request

Make sure you review our [Pull Request Guidelines](#pull-requests), before initiating a PR.

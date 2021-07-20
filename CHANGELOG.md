# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit guidelines.

<!--next-version-placeholder-->

## v2.0.3 (2021-07-20)
### Fix
* Use the upcoming version when deploying docs ([`f778318`](https://github.com/the-dotify-project/dotify/commit/f7783189bf683e516e2b0ce9a0c9c13441acc812))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v2.0.2...v2.0.3)**

## v2.0.2 (2021-07-20)
### Fix
* Sync workflow depending on "Publish" ([`0e5dea3`](https://github.com/the-dotify-project/dotify/commit/0e5dea33bdb36da452d40653a962e296652411f5))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v2.0.1...v2.0.2)**

## v2.0.1 (2021-07-19)
### Fix
* Include `py.typed` in module according to https://www.python.org/dev/peps/pep-0561/ ([`17d4387`](https://github.com/the-dotify-project/dotify/commit/17d438742ea1cd054b89d97b3aa1a66c65a79fa4))

### Documentation
* Replace `keep-a-changelog` with `conventional-commits` ([`e56a817`](https://github.com/the-dotify-project/dotify/commit/e56a81707342d2815e836612b21b0ea105120b29))
* Add `CD` badge to `README` ([`9f5bb26`](https://github.com/the-dotify-project/dotify/commit/9f5bb26d54ad3b586f2f7deec27bc0508f7fb0f3))
* Removed `docs.yml` badge from `README` ([`251e499`](https://github.com/the-dotify-project/dotify/commit/251e499f282e1551563fd99cbb8b44f8fa6872f1))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v2.0.0...v2.0.1)**

## v2.0.0 (2021-06-25)
### Feature
* Auto-populate the `Json` meta ([`2af3ad2`](https://github.com/the-dotify-project/dotify/commit/2af3ad2bb60cebb0088cab57b41400156b056414))

### Fix
* Do not re-raise `ValidationError` when setting an attribute of `JsonSerializable` ([`5a039c5`](https://github.com/the-dotify-project/dotify/commit/5a039c54569332d0b0b592dcd7ec26a09cd0e9ee))

### Breaking
* auto-populate the `Json` meta ([`2af3ad2`](https://github.com/the-dotify-project/dotify/commit/2af3ad2bb60cebb0088cab57b41400156b056414))

### Documentation
* Fix broken links due to multiple versions ([`21f934b`](https://github.com/the-dotify-project/dotify/commit/21f934b1710e92767357bbb0fddb148faf6df335))
* Change accent color to `teal` ([`cb96481`](https://github.com/the-dotify-project/dotify/commit/cb9648107b54adcf56253bc10dc2152bf46ec305))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v1.1.0...v2.0.0)**

## v1.1.0 (2021-06-17)
### Feature
* Client retrieve credentials from env ([`d5f52e7`](https://github.com/the-dotify-project/dotify/commit/d5f52e77b407d45fe08854ec524688435dadccdd))

### Documentation
* Multiple versions via `mike` ([`a6cdd45`](https://github.com/the-dotify-project/dotify/commit/a6cdd4511b24a40a411160b77eea2784ba16620e))
* Add `Documentation` url to PyPI page ([`7b7389d`](https://github.com/the-dotify-project/dotify/commit/7b7389dfb9135609c74eff95cdfeba2fbad68a3b))
* Fix broken link to features section ([`07cf730`](https://github.com/the-dotify-project/dotify/commit/07cf730224bdd433cc59e78cc5db61bcc595dbf2))
* Fix broken links ([`1e54c48`](https://github.com/the-dotify-project/dotify/commit/1e54c48672dace21673749001ea28f0eb3c3da3b))
* Uppercase `CHANGELOG.md` and `LICENSE.md` ([`592be6e`](https://github.com/the-dotify-project/dotify/commit/592be6e7b7dddfd0643ba5db2c7a86e78e86b348))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v1.0.0...v1.1.0)**

## v1.0.0 (2021-06-09)
### Fix
* Convert `Album.cover` to a `cached_property` ([`6777ad3`](https://github.com/the-dotify-project/dotify/commit/6777ad319e6b733f1f59f891afff987b4d186503))

### Breaking
* convert internal modules into protected ([`b7bc5a8`](https://github.com/the-dotify-project/dotify/commit/b7bc5a8f8da27d75d46001b7914ec8add80abd4a))

### Documentation
* Correctly indent nested lists in `.md` files ([`5caa257`](https://github.com/the-dotify-project/dotify/commit/5caa2579d9a2af769174ef196d88e7dd0b019998))
* Add `Playlist` documentation ([`44d961d`](https://github.com/the-dotify-project/dotify/commit/44d961df005b08a7c462a3e6da2c04af7ed15c92))
* Add `Album` documentation ([`7cbf3bc`](https://github.com/the-dotify-project/dotify/commit/7cbf3bcd8619aae5a8d6b544de33dd47753d1600))
* Add `Track` documentation ([`29c48a1`](https://github.com/the-dotify-project/dotify/commit/29c48a1c74fc80f2232d972d210828c03be3a294))
* Fix `codeclimate` urls ([`c42a775`](https://github.com/the-dotify-project/dotify/commit/c42a77598bdfd32b3e39bc2570ee18041af9a5cf))
* `Model.context` do not throw `TypeError` during `mkdocs build` ([`da80a51`](https://github.com/the-dotify-project/dotify/commit/da80a515995cbabd988ec277bf3ff53a11840949))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v0.3.9...v1.0.0)**

## v0.3.9 (2021-05-31)
### Fix
* Raise `NotFound` instead of `HTTPError` ([`e4c83da`](https://github.com/the-dotify-project/dotify/commit/e4c83dae880f751c63bd4237762bf1a5ecf8d7aa))

### Documentation
* Uppercase filenames ([`b679f5b`](https://github.com/the-dotify-project/dotify/commit/b679f5bbc2347a9861f0e36fdfc9b24c91e104f1))
* Remove folder references ([`e699080`](https://github.com/the-dotify-project/dotify/commit/e6990800433da507b0a7ed4f2b7647b09c1ab6fb))
* Fix broken urls ([`66c7f12`](https://github.com/the-dotify-project/dotify/commit/66c7f12d15f2cf9c1fad46fa3deb4a10b78db589))
* **README.md:** Center aligned badges ([`4539453`](https://github.com/the-dotify-project/dotify/commit/45394532b430cce30a5b330e1cc4efa142c5a464))
* **logo.png:** Enlarged ([`f9e939d`](https://github.com/the-dotify-project/dotify/commit/f9e939d5750af12e05a342ea3ae18bdc5c1157d2))
* **CONTRIBUTING.md:** Removed toc ([`4ebb5f9`](https://github.com/the-dotify-project/dotify/commit/4ebb5f9426c7bd4bc79975537fe03ebb2a01a0dd))
* Added license ([`637bbc2`](https://github.com/the-dotify-project/dotify/commit/637bbc22590d666d30bb97a3dc1aed336b8c9300))
* Added contributing ([`d2bed00`](https://github.com/the-dotify-project/dotify/commit/d2bed003388ec4d5da5c8999bb6684869f8466c8))
* Added code of conduct ([`de0bcfe`](https://github.com/the-dotify-project/dotify/commit/de0bcfe5267c9af936ec17442810495be1ddc309))
* Added changelog ([`dfe478d`](https://github.com/the-dotify-project/dotify/commit/dfe478d25ea04a7aaafb71cb3d0a250432bbcbb4))
* Added logo ([`43eec65`](https://github.com/the-dotify-project/dotify/commit/43eec6526b4009bfa360099378d94d89354d20cb))
* **CONTRIBUTING.md:** Mentioning `examples` ([`aa16fcf`](https://github.com/the-dotify-project/dotify/commit/aa16fcffff2871e6a9a116e1d0d990fbb048f389))
* **CONTRIBUTING.md:** Added `pyenv` section in testing with `tox` ([`6986af0`](https://github.com/the-dotify-project/dotify/commit/6986af00f24ed617e05cf47f36ba17e6ec779d3b))
* **tests:** Added a `README` ([`437ee1f`](https://github.com/the-dotify-project/dotify/commit/437ee1f6860c91411047f94de197ce4a69ea6e4e))
* Create .all-contributorsrc [skip ci] ([`043e974`](https://github.com/the-dotify-project/dotify/commit/043e97453c4c0df94e30a6a1fc48198642469335))
* Update README.md [skip ci] ([`0847fd3`](https://github.com/the-dotify-project/dotify/commit/0847fd3af716c4903cc58564aa324777cbef69d6))
* **mkdocs.yml:** Corrected `edit_uri` ([`491a49b`](https://github.com/the-dotify-project/dotify/commit/491a49b684a3bfd0f7d31e0ee9596e3b975afa65))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v0.3.8...v0.3.9)**

## v0.3.8 (2021-05-01)
### Fix
* **model.py:** `context` now does not throw ([`82f93d9`](https://github.com/the-dotify-project/dotify/commit/82f93d92e16860e3dd751125e0c5f72125781231))

### Documentation
* **README.md:** Added `docs` link & badge ([`42d4abe`](https://github.com/the-dotify-project/dotify/commit/42d4abe9b050f0cca20db6ea002e3cea07dcb6ab))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v0.3.5...v0.3.8)**

## v0.3.5 (2021-04-27)
### Fix
* **publish.yml:** Publishing via another gh-action ([`8487eb7`](https://github.com/the-dotify-project/dotify/commit/8487eb7dc5f24ede32f5300f6f0d640fd0b21c0c))

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v0.1.5...v0.3.5)**

## v0.1.5 (2021-04-17)
### Feature

- Enabled automatic releases via [GitHub Actions](.github/workflows/publish.yml)
- Enabled automatic `Changelog` generation via [GitHub Actions](.github/workflows/generate-changelog.yml)

**[See all commits in this version](https://github.com/the-dotify-project/dotify/compare/v0.1.4...v0.1.5)**

## v0.1.4 (2021-04-17)

🎂🎉 Initial Release 🎂🎉

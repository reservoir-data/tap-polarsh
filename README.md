<div align="center">

# tap-polarsh

<div>
  <a href="https://github.com/reservoir-data/tap-polarsh/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/reservoir-data/tap-polarsh"/>
  </a>
  <a href="https://results.pre-commit.ci/latest/github/reservoir-data/tap-polarsh/main">
    <img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/reservoir-data/tap-polarsh/main.svg"/>
  </a>
  <a href="https://scientific-python.org/specs/spec-0000/">
    <img alt="SPEC 0 — Minimum Supported Dependencies" src="https://img.shields.io/badge/SPEC-0-green"/>
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
  </a>
  <a href="https://github.com/astral-sh/uv">
   <img alt="uv" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json"/>
  </a>
</div>

Singer tap for [Polar.sh](https://polar.sh).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

</div>

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Settings

| Setting                           | Required | Default | Description                                                                                                                                                                                                                                              |
| :-------------------------------- | :------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| token                             | True     | None    | API Token for Polar                                                                                                                                                                                                                                      |
| is_member                         | False    | true    | Whether to only query organizations the user is a member of. Defaults to True.                                                                                                                                                                           |
| start_date                        | False    | None    | Earliest datetime to get data from                                                                                                                                                                                                                       |

<details>
<summary>Built-in Singer SDK Settings</summary>

| Setting                           | Required | Default | Description                                                                                                                                                                                                                                              |
| :-------------------------------- | :------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| stream_maps                       | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html).                                                                                                              |
| stream_map_config                 | False    | None    | User-defined config values to be used within map expressions.                                                                                                                                                                                            |
| faker_config                      | False    | None    | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an addtional dependency (through the `singer-sdk` `faker` extra or directly). |
| faker_config.seed                 | False    | None    | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator                                                                                                                                |
| faker_config.locale               | False    | None    | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization                                                                                                                                    |
| flattening_enabled                | False    | None    | 'True' to enable schema flattening and automatically expand nested properties.                                                                                                                                                                           |
| flattening_max_depth              | False    | None    | The max depth to flatten schemas.                                                                                                                                                                                                                        |
| batch_config                      | False    | None    |                                                                                                                                                                                                                                                          |
| batch_config.encoding             | False    | None    | Specifies the format and compression of the batch files.                                                                                                                                                                                                 |
| batch_config.encoding.format      | False    | None    | Format to use for batch files.                                                                                                                                                                                                                           |
| batch_config.encoding.compression | False    | None    | Compression format to use for batch files.                                                                                                                                                                                                               |
| batch_config.storage              | False    | None    | Defines the storage layer to use when writing batch files                                                                                                                                                                                                |
| batch_config.storage.root         | False    | None    | Root path to use when writing batch files.                                                                                                                                                                                                               |
| batch_config.storage.prefix       | False    | None    | Prefix to use when writing batch files.                                                                                                                                                                                                                  |

</details>

A full list of supported settings and capabilities is available by running: `tap-polarsh --about`

### Source Authentication and Authorization

Get a [Personal Access Token](https://polar.sh/settings) and provide it as the `token` setting.

## Supported Python Versions

* 3.12
* 3.13
* 3.14

## Installation

### In a Meltano project

#### Using a direct reference

```bash
meltano add extractor tap-polarsh --from-ref=https://raw.githubusercontent.com/reservoir-data/tap-polarsh/main/plugin.yaml
```

Requires Meltano v3.1.0+.

#### From MeltanoHub

Not yet available.

### From PyPI

Not yet available.

### With [pipx][pipx]

```bash
pipx install git+https://github.com/reservoir-data/tap-polarsh.git@main
```

[pipx]: https://github.com/pypa/pipx

## Usage

You can easily run `tap-polarsh` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-polarsh --version
tap-polarsh --help
tap-polarsh --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
uv tool install --with tox-uv tox
```

### Create and Run Tests

Run all tests:

```bash
tox run-parallel
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Use Meltano to run an EL pipeline:

```bash
uvx meltano invoke tap-polarsh --version
uvx meltano run tap-polarsh target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

# `tap-polarsh`

Singer tap for [Polar.sh](https://polar.sh).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

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

* 3.8
* 3.9
* 3.10
* 3.11
* 3.12

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
pipx install hatch
```

### Create and Run Tests

Run integration tests:

```bash
hatch run test:integration
```

You can also test the `tap-polarsh` CLI interface directly:

```bash
hatch run sync:console -- --about --format=json
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file. Go ahead and [install Meltano](https://docs.meltano.com/getting-started/installation/) if you haven't already.

1. Install all plugins

   ```bash
   meltano install
   ```

1. Check that the extractor is working properly

   ```bash
   meltano invoke tap-polarsh --version
   ```

1. Execute an ELT pipeline

   ```bash
   meltano run tap-polarsh target-jsonl
   ```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

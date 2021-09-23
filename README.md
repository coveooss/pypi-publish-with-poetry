# pypi-publish-with-poetry

This GitHub Action will publish a Python project to [pypi.org](https://pypi.org).


# Features

- Publish to pypi using your pypi token.
- Semi-automatic versioning.
- Automatic repository version tagging.
- Prerelease support.
- Dry run support.


# Limitations

Some limitations exist by design:
 
- You cannot overwrite an existing package.
- You cannot publish a version that is lower than the latest from pypi.


# Requirements

- Python must be preconfigured and installed; a `python` executable must be in the path.
- The Python project must be configured to use [Poetry](https://python-poetry.org).
- You must provide a secret `pypi` token.

Note: The packages `pip`, `setuptools`, `wheel` and `pipx` will be installed/upgraded 
using the `python` executable from the path.

# Default usage

The default usage requires a project name and a token:

      - name: Publish to pypi
        uses: coveooss/pypi-publish-with-poetry@v1.0.0
        with:
          project-name: my-project-name
          pypi-token: ${{ secrets.PYPI_TOKEN }}

The project will be published, your changeset will be tagged with a `v1.2.3` kind of tag and revisions will increase automatically.

## About the action's version

In this repository, we don't keep a `@v1` or `latest` tag that we update as new revisions are released.

Instead, we leverage our own repository tagging feature to provide users with a `v{major}.{minor}.{revision}` tag.
This is similar to specifying the changeset's sha, but offers more visibility on the evolution of the action
and allows us to transparently issue security and emergency hotfixes if that ever becomes a necessity.

- If you want guaranteed immutability, specify a `@sha`.
- If you want general immutability and potential hotfixes, specify a `v{major}.{minor}.{revision}`.
- If you want to live dangerously, specify `@main`.


# Documentation

## Semi-Automatic Versioning

This action features semi-automatic versioning based on the value of the `version` field from your `pyproject.toml`
and the latest released version from pypi.

In a nutshell:
- Use the `pyproject.toml` to set a minimum version to release. The action will increment from there.
- Keep publishing to bump revisions. No need to edit the version in `pyproject.toml`.
- To set a new minor or major, bump and commit the version in `pyproject.toml` (i.e.: step 1!).

### The automatic part

The revision bump is automatic (the `x` in `3.5.x`).
The next revision is always based on pypi's realtime api; you cannot overwrite an existing package or go back in time.

The new version will be added to the `pyproject.toml` file included with the distribution,
but it will **not** be committed to the repository. This is normal!

We use 
[coveo-pypi-cli](https://github.com/coveooss/coveo-python-oss/tree/main/coveo-pypi-cli#pypi-cli-in-action) 
to compute the next version.

### The manual part

If you want to bump the minor or major, just do it manually in the `pyproject.toml` and commit that.
It will become the next released version.

1. Open the `pyproject.toml` file.
2. Edit and commit the next version number (e.g.: 1.1.0 -> 1.2.0).
3. Publish your project.


### Example

#### New project
- Your `pyproject.toml` has `version=0.1.0`.
- There are no releases in pypi.
- The next prerelease would be `0.1.0a1`.
- The next release will be `0.1.0`.

#### Automated revision
- Your `pyproject.toml` still has `version=0.1.0`.
- The latest release is `0.1.0`.
- The next prerelease would be `0.1.1a1`.
- The next release will be `0.1.1`.

#### Minor revision w/prerelease
- Update your `pyproject.toml` to `version=0.2.0` and commit.
- The latest release is `0.1.1`.
- The next prerelease would be `0.2.0a1`.
- The next release will be `0.2.0`.

#### Major revision w/prerelease
- Update your `pyproject.toml` to `version=1.0.0` and commit.
- The latest release is `0.2.0`.
- The next prerelease would be `1.0.0a1`.
- The next release will be `1.0.0`.

#### Skipping revisions
- Update your `pyproject.toml` to `version=1.4.4` and commit.
- The latest release is `1.0.0`.
- The next prerelease would be `1.4.4a1`.
- The next release will be `1.4.4`.

#### Automated revisions
Just for the sake of completing the example:
- Your `pyproject.toml` is still set to `version=1.4.4`.
- The latest release is `1.4.4`.
- The next prerelease would be `1.4.5a1`.
- The next release will be `1.4.5`.


## Automatic Tagging

Whenever a new distribution is published, the repository will be tagged with its version.

The tag has the `{prefix}{version}{prerelease}` format and the default settings will give you something like `v1.2.3a4`.
Use the `tag-prefix` option to customize the prefix part.

Note: The tag and the auto versioning system are completely independent. 
If you don't want the tags, feel free to delete them, or better: open a PR with a new option to skip them! :rocket:


## Dry Run

You can launch a dry run of the publish operation, which will:

- Compute the next version and prerelease version it would publish and echo it to the logs.
- Compute the tag it would write and echo that to the logs.
- Build the sdist and wheel of your project.

The dry run option is detailed at  [the top of the action file](./action.yml).


# Recommended usage

The recommended usage will provide you this behavior:

- Running the action from the main branch will automatically publish a new version.
- Running the action from other branches will produce a dry run.
- Running the action manually on a branch and typing in "true" when prompted will publish a prerelease version.

First, you need to add some inputs in the workflow dispatch: 

      workflow_dispatch:
        inputs:
          publish:
            description: "Publish to pypi.org? (will not work from forks!)"
            required: false
            default: 'false'


Here's how we suggest you design the `uses` step:
    
      - name: Publish to pypi
        uses: coveooss/pypi-publish-with-poetry@v1.0.0
        with:
          project-name: my-project-name
          pypi-token: ${{ secrets.PYPI_TOKEN }}
          pre-release: ${{ github.ref != 'refs/heads/main' }}
          dry-run: ${{ github.ref != 'refs/heads/main' && github.event.inputs.publish != 'true' }}


More options are described at [the top of the action file](./action.yml).


# How to start a new project

When starting a new project, we recommend setting your project's version to `0.1.0` as the first official public release, 
as described in the [semantic versioning FAQ](https://semver.org/#how-should-i-deal-with-revisions-in-the-0yz-initial-development-phase).


# How to migrate an existing project

Since the action cannot overwrite packages or go back in time, you only have to start using this action.

- If the version already exists in pypi, a new one will be used.
- If the version doesn't exist, it's the new starting point.

So, it's perfectly fine to use a `version` of `0.1.0` for an existing package even if e.g. `3.5.6` is released.
The next version will be `3.5.7`! Or if you think this move is potentially breaking, set it to `3.6` or `4.0` to set a new minimum.

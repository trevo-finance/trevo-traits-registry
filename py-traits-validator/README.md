# Traits validator

This package provides a tool to validate the traits contained in the metadata of TRAIT on-chain objects.

## Developemnt

Every time you make changes to the registry you need to run:

- Copy the registry to the dir with python code, so that setuptool includes it into the package:

``` command
python3 scripts/bundle_registry.py
```

- Re-install the package in editable mode:

``` command
pip install -e '.[dev]' --config-settings editable_mode=strict
```

After that python package and tests work correctly.

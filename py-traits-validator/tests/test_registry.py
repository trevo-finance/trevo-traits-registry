import http
import json
import os
from pathlib import Path

import requests
from pydantic import BaseModel

from traitsvalidator import TraitsValidator


class TestConfig:
    REGISTRY_NAME: str = "registry.json"
    REGISTRY_PATH: Path = Path(__file__).parent.parent.parent / REGISTRY_NAME
    TRAITS_PATH: Path = Path(__file__).parent.parent.parent / "traits"

    TRAITS_BASE_URI: str = "https://trevo-finance.github.io/trevo-traits-registry/traits/"

    HTTP_TIMEOUT: float = 30.0  # 30 seconds

    EXAMPLE_META_DIR: Path = Path(__file__).parent.parent.parent / "examples"


class Trait(BaseModel):
    trait_id: str
    specification: str
    description: str
    status: str


class Registry(BaseModel):
    version: str
    registry: list[Trait]


def test_consistency_of_registry() -> None:
    # Read the registry
    with TestConfig.REGISTRY_PATH.open() as fp:
        reg_obj = json.load(fp)
    registry = Registry.model_validate(reg_obj)

    # Collect traits that actually exist in the repo
    trait_id_list = set()
    for dirpath, _dirnames, filenames in os.walk(TestConfig.TRAITS_PATH):
        if "trait.json" not in filenames:
            continue

        subfolder = dirpath[len(str(TestConfig.TRAITS_PATH)) + 1 :]
        trait_id = subfolder.replace(os.path.sep, ".")
        trait_id_list.add(trait_id)

    # Check content of `registry.json`
    for trait in registry.registry:
        # Check `id` points to a subfolder `traits/` of this repo
        if trait.trait_id not in trait_id_list:
            msg = f"`trait_id` is not pointing to a subfolder `traits/`: {trait.trait_id}"
            raise ValueError(msg)

        # Check `specification`
        if not trait.specification.startswith(TestConfig.TRAITS_BASE_URI):
            msg = f"Malformed trait `specification`: {trait.specification}"
            raise ValueError

        resp = requests.get(url=trait.specification, timeout=TestConfig.HTTP_TIMEOUT)
        if resp.status_code != http.HTTPStatus.OK:
            msg = f"Object, specified in 'trait.specification' not found by the URL `{trait.specification}`."
            raise ValueError(msg)

    # Check that all traits added to the `registry.json`
    for trait_id in trait_id_list:
        found = any(trait for trait in registry.registry if trait.trait_id == trait_id)
        if not found:
            msg = f"Trait `{trait_id}` is not present in `registry.json`."
            raise ValueError(msg)


def test_validation_of_traits() -> None:
    validator = TraitsValidator()

    # Validate AppAgent metadata
    with (TestConfig.EXAMPLE_META_DIR / "appagent.json").open() as fp:
        appagent_meta = json.load(fp)
    available_traits = validator.validate_metadata(appagent_meta)
    assert available_traits == ["named", "finance.trevo.wallet.square_icon"]

    # Validate metadata of fungible token
    with (TestConfig.EXAMPLE_META_DIR / "fungible_token.json").open() as fp:
        fungible_meta = json.load(fp)
    available_traits = validator.validate_metadata(fungible_meta)
    assert available_traits == [
        "named",
        "fungible",
        "finance.trevo.wallet.square_icon",
        "finance.trevo.wallet.price_feed",
    ]

    # Validate metadata of nft collection
    with (TestConfig.EXAMPLE_META_DIR / "nft_collection.json").open() as fp:
        nft_collection_meta = json.load(fp)
    available_traits = validator.validate_metadata(nft_collection_meta)
    assert available_traits == [
        "named",
        "finance.trevo.wallet.square_icon",
        "finance.trevo.wallet.nft_collection_listing_image",
    ]

    # Validate metadata of nft token
    with (TestConfig.EXAMPLE_META_DIR / "nft_token.json").open() as fp:
        nft_token_meta = json.load(fp)
    available_traits = validator.validate_metadata(nft_token_meta)
    assert available_traits == [
        "named",
        "finance.trevo.wallet.square_icon",
        "finance.trevo.wallet.nft_token_listing_image",
        "finance.trevo.wallet.nft_token_cover_image",
        "finance.trevo.wallet.nft_token_description",
        "finance.trevo.wallet.nft_token_attributes",
    ]

    # Validate metadata of compliance provider
    with (TestConfig.EXAMPLE_META_DIR / "compliance_provider.json").open() as fp:
        compliance_provider_meta = json.load(fp)
    available_traits = validator.validate_metadata(compliance_provider_meta)
    assert available_traits == [
        "named",
        "finance.trevo.wallet.square_icon",
    ]

    # Validate metadata of identity provider
    with (TestConfig.EXAMPLE_META_DIR / "identity_provider.json").open() as fp:
        identity_provider_meta = json.load(fp)
    available_traits = validator.validate_metadata(identity_provider_meta)
    assert available_traits == [
        "named",
        "finance.trevo.wallet.square_icon",
    ]

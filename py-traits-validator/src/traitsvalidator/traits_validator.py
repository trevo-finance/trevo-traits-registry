import json
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator, validate

_TRAITS_BASE_URI: str = "https://trevo-finance.github.io/trevo-traits-registry/traits/"


class TraitsValidator:
    """
    TraitsValidator performs validation of the data against the traits registry and (optional) list of private traits.
    """

    _metadata_schema: dict[str, Any]
    _traits_registry: dict[str, dict[str, Any]]

    def __init__(self: "TraitsValidator", *, custom_traits: dict[str, dict[str, Any]] | None = None) -> None:
        """
        Initializes the TraitsValidator instance.

        Parameters:
            custom_traits (dict[str, dict[str, Any]] | None): A dictionary of custom traits
            to update the traits registry with.

        Returns:
            None
        """
        # Check input
        if custom_traits is not None and not isinstance(custom_traits, dict):
            msg = f"Expected `custom_traits` to be a dict, got `{type(custom_traits)}`"
            raise ValueError(msg)

        # Load schema of the metadata document
        self._metadata_schema = self._load_metadata_schema()

        # Load traits registry and update it with provided traits
        self._traits_registry = self._load_traits_registry()
        if custom_traits is not None:
            self._traits_registry.update(custom_traits)

    @staticmethod
    def _load_metadata_schema() -> dict[str, Any]:
        metadata_schema_text = files("traitsvalidator.registry").joinpath("metadata_schema.json").read_text()
        return json.loads(metadata_schema_text)

    @staticmethod
    def _load_traits_registry() -> dict[str, dict[str, Any]]:
        dicovered_traits: dict[str, Any] = {}
        for resource_item in files("traitsvalidator.registry").iterdir():
            if resource_item.is_file() and resource_item.name not in {"registry.json", "metadata_schema.json"}:
                trait_text: str = resource_item.read_text()
                trait_content: dict[str, Any] = json.loads(trait_text)
                trait_id: str = trait_content["$id"]
                trait_id = trait_id[len(_TRAITS_BASE_URI) : -len("/trait.json")].replace("/", ".")
                dicovered_traits[trait_id] = trait_content
        return dicovered_traits

    def validate_metadata(  # noqa: C901
        self: "TraitsValidator", metadata: dict[str, Any], *, traits_to_validate: list[str] | None = None
    ) -> list[str]:
        """
        Validates the provided metadata against the traits registry.

        Args:
            self (TraitsValidator): The instance of the TraitsValidator class.
            metadata (dict[str, Any]): The metadata to be validated.
            traits_to_validate (list[str] | None, optional): A list of trait IDs to be validated. Defaults to None.

        Returns:
            list[str]: A list of validated trait IDs.
        """
        # Check input params
        if not isinstance(metadata, dict):
            msg = f"Expected `data` to be a dict, got `{type(metadata)}`"
            raise ValueError(msg)  # noqa: TRY004
        if traits_to_validate is not None:
            if not isinstance(traits_to_validate, list):
                msg = f"Expected `traits_to_validate` to be a list, got `{type(traits_to_validate)}`"
                raise ValueError(msg)
            if len(traits_to_validate) == 0:
                msg = "Expected `traits_to_validate` to be not empty"
                raise ValueError(msg)
            if any(t for t in traits_to_validate if not isinstance(t, str)):
                msg = "Expected `traits_to_validate` to be a list of strings"
                raise ValueError(msg)

        # validate data with the document schema
        self._validate_document_schema(metadata)

        # validate individual traits
        validated_traits: list[str] = []

        if traits_to_validate is None:
            # validate all traits that present in metadata
            for trait_id, trait_data in metadata["traits"].items():
                if self._validate_trait_schema(trait_id, trait_data):
                    validated_traits.append(trait_id)

        else:
            # validate only provided traits
            for trait_id in traits_to_validate:
                if trait_id in metadata["traits"] and self._validate_trait_schema(
                    trait_id, metadata["traits"][trait_id]
                ):
                    validated_traits.append(trait_id)

        return validated_traits

    def get_initialised_traits(self: "TraitsValidator") -> list[str]:
        return list(self._traits_registry.keys())

    def _validate_document_schema(self: "TraitsValidator", data: dict[str, Any]) -> None:
        try:
            validate(instance=data, schema=self._metadata_schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
        except Exception as e:
            msg = "Failed to validate metadata document schema"
            raise ValueError(msg) from e

    def _validate_trait_schema(self: "TraitsValidator", trait_id: str, trait_data: dict[str, Any]) -> bool:
        if trait_id not in self._traits_registry:
            return False

        try:
            validate(
                instance=trait_data,
                schema=self._traits_registry[trait_id],
                format_checker=Draft202012Validator.FORMAT_CHECKER,
            )
        except Exception as e:
            msg = f"Failed to validate content of the trait `{trait_id}`"
            raise ValueError(msg) from e

        return True

from typing import Any

class TraitsValidator:
    def __init__(self: TraitsValidator, *, custom_traits: dict[str, dict[str, Any]] | None = None) -> None: ...
    def validate_metadata(
        self: TraitsValidator, metadata: dict[str, Any], *, traits_to_validate: list[str] | None = None
    ) -> list[str]: ...

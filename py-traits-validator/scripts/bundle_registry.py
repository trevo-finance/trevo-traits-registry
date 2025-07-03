# Script collects all traits from the registry
# and copies to the `py-traits-validator` to include in the distributed package.

import hashlib
import os
import shutil
from pathlib import Path

print("Start to prepare the traits files for package bundling")  # noqa: T201

print("Calcualte the dirs")  # noqa: T201
repo_root_dir = Path(__file__).parent.parent.parent.resolve()
registry_trais_dir = repo_root_dir / "traits"
package_registry_dir = repo_root_dir / "py-traits-validator" / "src" / "traitsvalidator" / "registry"


print("Empty target dir if exists")  # noqa: T201
if package_registry_dir.exists():
    shutil.rmtree(package_registry_dir)
package_registry_dir.mkdir()


print("Collect traits that actually exist in the repo")  # noqa: T201
for dirpath, _dirnames, filenames in os.walk(registry_trais_dir):
    for filename in filenames:
        if filename == "trait.json":
            src_file_path = Path(dirpath) / filename

            dest_file_name_material = str(src_file_path)[len(str(repo_root_dir)) :]
            print(f"Filename material: {dest_file_name_material}")  # noqa: T201
            m = hashlib.sha256()
            m.update(dest_file_name_material.encode())
            dest_file_name = f"{m.hexdigest()}.json"
            print(f"Filename: {dest_file_name}")  # noqa: T201
            dest_file_path = package_registry_dir / dest_file_name
            print(f"Destination filepath for package bundling: {dest_file_path}")  # noqa: T201

            shutil.copyfile(src_file_path, dest_file_path)


print("Copy metadata_schema.json")  # noqa: T201
src_file_path = registry_trais_dir / "metadata_schema.json"
dest_file_path = package_registry_dir / "metadata_schema.json"
shutil.copyfile(src_file_path, dest_file_path)


print("Copy registry.json")  # noqa: T201
src_file_path = repo_root_dir / "registry.json"
dest_file_path = package_registry_dir / "registry.json"
shutil.copyfile(src_file_path, dest_file_path)

print("Finished to prepare the traits files for package bundling")  # noqa: T201

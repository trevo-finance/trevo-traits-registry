# Trevo Traits Registry ![Version](https://img.shields.io/badge/version-v1.0.0-blue)

Traits are features of on-chain entities such as tokens, NFTs, AppAgents, Identity providers and Compliance providers.
These traits are manifested in the metadata of on-chain entities and are available for use by off-chain applications.
The metadata, which is a document in JSON format, contains all the necessary information about the on-chain entities. 
This information includes identifiers, text, numbers, links to external resources, and more.

This repository is a registry of schemas of well-known traits in the Trevo ecosystem.
The schemas of traits are represented in the [JSON Schema](https://json-schema.org/).

Please read more about metadata and traits in the docs portal: [Trevo Docs](https://trevo.gitbook.io/trevo-docs).

## Process

- Fork and clone this repo;
- Add an additional trait to the dir `traits/`;
  - name of the directory is the ID of the trait. ID of app-specific traits must follow reverse DNS notation;
  - directory can contain several files with definition of the trait. The root file in the directoty must be named `trait.json`;
- Add an entry to the `registry.json` file;
- Increase the minor (middle) version number;
- Run git stage, commit, push to GitHub;
- Create a pull request and provide a description of the triats you want to add;
- Once the PR has merged, one of the admins will create a new release of the registry;

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

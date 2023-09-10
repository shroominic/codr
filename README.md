# Codr Project

## Project Overview

'codr' is a Python-based coding assistant that automates and streamlines the task-solving process for developers. It leverages the power of GPT models to interact with codebases, generate prompts, parse outputs, and manage token counts and truncations.

## Features

- **GPT Model Interaction**: 'codr' uses GPT models to understand and interact with the codebase.
- **Prompt Generation**: It generates prompts based on the task at hand, facilitating a conversational approach to task-solving.
- **Output Parsing**: 'codr' parses the output from the GPT models to extract meaningful information.
- **Token Management**: It handles token count and truncation for long inputs, ensuring efficient use of resources.
- **Task Automation**: 'codr' automates various tasks such as debugging, committing changes, and testing.
- **File Management**: It provides functionalities for managing the codebase, including file creation, modification, and deletion.

## Codebase Structure

The 'codr' project is organized into three main modules: 'funcchain', 'codr', and 'codebase'.

- **Funcchain**: This module provides utilities for interacting with GPT models, including prompt generation, output parsing, and token management.
- **Codr**: This module contains scripts for automating tasks related to file management and debugging. It includes submodules for handling codebase nodes, running commands and file operations, and automating programming tasks.
- **Codebase**: This module provides classes and functions for representing and managing a codebase as a tree of nodes.

## Documentation

For a comprehensive understanding of the project, its modules, and usage, refer to the detailed documentation in the [docs](./docs) directory. The documentation provides a self-contained guide to the 'codr' project, making it accessible and understandable even to a developer with limited access to the codebase.

## Installation and Setup

To install and setup the project, you need Python 3.7 or higher and the Poetry package manager. Clone the repository and install the dependencies using Poetry.

## Usage

The 'codr' project provides a command-line interface (CLI) for executing tasks asynchronously. The CLI offers features for task-solving, debugging, committing changes, and testing.

## Contributing

Contributions to the 'codr' project are welcome. If you wish to contribute, please make sure to update tests as appropriate and adhere to the pre-commit hooks configuration for tasks like YAML checking, file fixing, code formatting, type checking, and code linting.

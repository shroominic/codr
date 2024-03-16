# Codr Project

## Introduction

Welcome to 'codr', a revolutionary Python-based coding assistant designed to automate and simplify the coding process. By harnessing the power of GPT models, 'codr' can interact with Codebases, generate prompts, parse outputs, and manage tokens. This allows it to automate a variety of tasks such as debugging, committing changes, testing, and file management.

## Features

- **GPT Model Interaction**: 'codr' utilizes GPT models to interact with the Codebase, providing a deeper understanding of the code and facilitating more effective problem-solving.
- **Prompt Generation**: 'codr' generates prompts based on the task at hand, allowing for a more conversational and intuitive approach to coding.
- **Output Parsing**: 'codr' parses the output from the GPT models, extracting meaningful and actionable information to guide the coding process.
- **Token Management**: 'codr' efficiently manages token counts and truncations for long inputs, ensuring optimal use of resources and preventing unnecessary waste.
- **Task Automation**: 'codr' automates a variety of tasks such as debugging, committing changes, and testing. This saves valuable time and effort, allowing developers to focus on more complex problems.
- **File Management**: 'codr' offers functionalities for managing the Codebase, including file creation, modification, and deletion. This makes it easier to manage large Codebases and keep track of changes.

## Project Structure

The 'codr' project is organized into three main modules: 'funcchain', 'codr', and 'Codebase'.

- **Funcchain**: This module provides utilities for interacting with GPT models, including prompt generation, output parsing, and token management.
- **Codr**: This module contains scripts for automating tasks related to file management and debugging. It includes submodules for handling Codebase nodes, running commands and file operations, and automating programming tasks.
- **Codebase**: This module provides classes and functions for representing and managing a Codebase as a tree of nodes.

## Documentation

For a comprehensive understanding of the project, its modules, and usage, refer to the detailed documentation in the [docs](./docs) directory. The documentation provides a self-contained guide to the 'codr' project, making it accessible and understandable even to a developer with limited access to the codebase.

## Installation and Setup

To install and setup the project, you need Python 3.7 or higher and the Poetry package manager. Clone the repository and install the dependencies using Poetry.

## Usage

The 'codr' project provides a command-line interface (CLI) for executing tasks asynchronously. The CLI offers features for task-solving, debugging, committing changes, and testing.

## Contributing

Contributions to the 'codr' project are welcome. If you wish to contribute, please make sure to update tests as appropriate and adhere to the pre-commit hooks configuration for tasks like YAML checking, file fixing, code formatting, type checking, and code linting.

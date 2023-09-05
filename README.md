# Codr Project

## Project Overview

'codr' is a Python project that provides a coding assistant to solve tasks for developers. It uses GPT models and various utilities to interact with the codebase, generate prompts, parse the output, and handle token count and truncation for long inputs.

## Features

- Interacting with GPT models
- Extracting docstrings
- Determining the parser based on the return type
- Extracting kwargs from the parent function
- Creating prompts
- Handling token count and truncation for long inputs

## Codebase Structure

The codebase is organized into several modules and submodules, each with specific functionalities. The main modules include 'funcchain', 'codr', and 'codebase'. The 'funcchain' module provides utilities for interacting with GPT models. The 'codr' module contains scripts for automating tasks related to file management and debugging. The 'codebase' module provides classes for representing a codebase as a tree of nodes.

## Installation and Setup

To install and setup the project, clone the repository and install the dependencies using Poetry.

## Usage

The project provides a command-line interface script that provides commands to solve a task based on a description, automatically debug, commit changes, and run a test.

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate.

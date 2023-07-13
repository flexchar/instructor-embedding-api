# Instructor Embedding API

This repository contains a lightweight Sanic API for creating embeddings using the Instructor model. It is provided as a Docker container and based on the `hkunlp/instructor-large` model. The API can be used for versatile purposes, including in applications such as text classification, similarity, or clustering tasks.

## Quick Start

### Prerequisites

-   [Docker](https://www.docker.com/get-started), version 20.10 or newer

### Build and Run the API

1. Clone this repository:

    ```sh
    git clone https://github.com/flexchar/instructor-embedding-api.git
    cd instructor-embedding-api
    ```

2. Build a Docker image:

    ```sh
    make build
    ```

3. Run the Docker container:

    ```sh
    make run
    ```

The API will be available at `http://127.0.0.1:8000/`.

### Use the API

You can use the API to generate embeddings by sending a POST request to `http://127.0.0.1:8000/` with a JSON payload in the format:

```json
{
    "input": [instruction_sentence_pairs]
}
```

`instruction_sentence_pairs` is a list of pairs, where each pair contains two strings: an instruction and a sentence.

For example:

```json
{
    "input": [
        [
            "Represent the Fitness title:",
            "What is the easiest training plan for a newbie?"
        ]
    ]
}
```

A valid response will have the following structure:

```json
{
    "model": "hkunlp/instructor-large",
    "data": [embeddings]
}
```

`embeddings` is a list of arrays representing the embeddings for the given instruction-sentence pairs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Humanitec-Back-End-Assignment

## Problem description:
Build two Flask Microservices

We have two different entities (products & orders) and we need to create two microservices with externally accessible but authenticated APIs.

The first microservice provides endpoints to manipulate products. Products are stored in a JSON file with fields UUID, name, price.

The second microservice provides endpoints to manipulate orders. Orders are stored in another JSON file.

Orders can potentially reference several products.

Both Flask microservices depend on a common Python package that manages the JSON files with the stored data (let’s call it JSON storage manager).

The JSON storage manager should be written in Python and potentially support the use of multiple python frameworks.

You need to build and publish this package.

The JSON storage manager should act as an application core that is unique. The JSON storage manager package may use other packages internally to facilitate working with JSON files.

Considerations:
* Feel free to use any additional modules that you see fit.
* Choose the authentication method that you are more comfortable with.
* For publishing the package it’s not needed to do it on PyPi, but just having a separate repository for it.

To evaluate:
* Good, clean architecture
* Code reusability
* Testing coverage
* The application needs to build and run
* Clear documentation of how to build and run the microservices

Extra points:
* Concurrency control
* Asynchronous communication
* Efficiency (Memory concern)
* Handling JSON files
* Memory management: it’s good if the candidate asks what to do if the JSON does not fit in memory.
* Containerization

Related Repos:
* [JSON-storage-manage](https://github.com/myaser/JSON-storage-manager)

---
## Solution
TODO:
* limitations: tinyrecord do not support concurrency
* separate test database from production database
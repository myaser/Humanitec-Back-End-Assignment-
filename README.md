# Problem description:
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
* [JSON-storage-manager](https://github.com/myaser/JSON-storage-manager)

---

# Q&A

### Q1

what are the fields of order

### A1

UUID, quantity, product UUID

### Q2

what are the integrity roles between order and product (when a product is deleted, what happens to orders referencing it?)

### A2

Taking this decision is part of the task.

### Q3

what kind of operations are more frequent (read heavy / write heavy)

### A3

Consider 50/50. No operation is more frequent than the other one.

### Q4

what happens if JSON files did not fit in memory

### A4

Consider that it's gonna fit in memory and if you still have time, you can consider that it doesn't fit in memory.

---
# Solution
## operations
### install and run
in the project root:
```bash
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up
```
in your browser open ``http://localhost/``
you will find swagger documentation where you can test all end points of each microservice
(please note the upright corner)
![screenshot](https://raw.githubusercontent.com/myaser/microservices-with-json-storage/master/docs/screenshot.png "screenshot 1")

### run tests
```bash
./test.sh dev
```
a coverage report will be displayed after test is complete, and you can find coverage html report under:
```
services/orders/htmlcov
services/products/htmlcov
```
## design
### reverse proxy
nginx is used as reverse proxy.
client will have a single host to communicate with and a single open port

### swagger-ui
central place to display documentation of both micro-services

### micro-services
two micro-services communicating to each other using REST api

when user creates an order, orders micro-service sends a request to Products micro-service to validate that product already exist

when user removes a product, products micro-services sends a request to orders micro-service to validate is it not booked already

#### composition  of micro service
* flask micro web framework
* Flask-RESTPlus adds support for quickly building and documenting REST APIs
* flask-jwt-simple enables JWT authentication. we use RS256 signing algorithm with public and private keys
    * both micro-services are holding the public key
    * I made the assumption that there is another service in the system (users micro-service) holding the private key and handles authentication and token generation
    * orders and products micro-services can decrypt tokens signed by that micro-service, that's how we know user is logged-in
    * for testing you can generate a token using:
    ```bash
    docker-compose -f docker-compose-dev.yml run orders flask generate-test-token
    ```
* the micro-service is organized on [repository design pattern](https://code.tutsplus.com/tutorials/the-repository-design-pattern--net-35804)
    * the main benefit for that is to decouple business logic from persistence, so we can change the persistence dynamically in the runtime and still have the same logic applies
    * this is useful as the same data could be persisted into (SQL, NoSQL, MessageQueue, REST API, ... etc)
    * the same object could also be split into different persistence
* TinyDB:
    * I used TinyDB as json storage to quickly prototype the micro-services, then I will build a brand new database as asked in problem deffination
    * TinyDB has some limitations about concurrency:
        * TinyDB do not support concurrent access by itself, it uses an extension for that
        * tinyrecord (concurrency extension for TinyDB) [supports only thread concurrency](https://github.com/eugene-eeo/tinyrecord/issues/5)
        so the model of multi process execution will not be suitable <sup>*</sup>

\* we use synchronous gunicorn workers now, we need to change it to Async Workers with Greenlets

 
### TODO:

* create new JSON storage in replacement to tinydb with focus on concurrency
* write integration tests
* write docker-compose-prod.yml
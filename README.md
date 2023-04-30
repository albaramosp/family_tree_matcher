# Family Tree Matcher
Find your lost ancestors with Family Tree Matcher!
This is a TDD and an attempt to learn more about architectures & design patterns.

## Architecture & patterns
### Hexagonal architecture (ports & adapters)
Hexagonal architecture is also known as ports & adapters architecture. 
It is related to Clean Architecture.
According to this architecture, outer layers can access inner layers, but not the opposite. 
Therefore, inner layers should only know abstractions regarding the outer layers, not their implementation.
It establishes three layers:
- **Infrastructure**: The outermost layer. 
It stores everything related to external data sources. 
It stores specific implementations of repositories (known as adapters).
- **Application**: The use cases (everything that can be launched by an API call).
- **Domain**: The innermost layer. The models & business rules of our context are here. 
Repositories generic interfaces (or ports) are here. 
We will divide the ports into driver and driven contexts. 
Driver refers to the connection between presentation and application.
Driven refers to the connection between infrastructure and application.

### Vertical slicing architecture
When we have multiple models the hexagonal architecture structure may be difficult to escalate. 
If we combine it with vertical slicing, we can create a directory for each model (like person and matcher) and apply the hexagonal architecture inside each.

### Design patterns
#### Repository
This pattern will handle the creation and getting objects. 
We will have the generic interface and the concrete implementations, so that the usage of the repository doesn't depend on concrete implementations.

#### Factory
This patterns states that we should avoid directly creating concrete objects and use a factory method instead for their creation.


## Launch tests
To test with coverage, run the following commands:

    $ python -m unittest discover
    $ python -m coverage report
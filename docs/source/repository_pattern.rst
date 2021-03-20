##################
Repository Pattern
##################
Repository pattern is an abstraction layer which separates hides persisting, updating and retrieving our model objects from and to a certain repository.
By using this pattern we can treat the domain model independently from the data storing method.
We can also use multiple different storing mediums on our model just by passing the models to the repository objects.
Our Domain Model should not be aware of the repository objects - the role of translating domain to storage specificity is handled completely on the repository object side.

Port and adapters
-----------------
Particular repository types should share unified structure - they should all have the same set of operations accepting the same attributes.
To achieve that *port and adapter* pattern can be used.

.. mermaid::

    classDiagram
        AbstractRepository <|-- FakeRepository
        AbstractRepository <|-- SqlAlchemyRepository
        AbstractRepository <|-- RedisRepository
        SqlAlchemyRepository -- Session
        RedisRepository -- RedisClient
        FakeRepository o-- Batch
        class AbstractRepository{
            get(reference : str) Batch
            add(batch : Batch)
            }
        class SqlAlchemyRepository{
            session: sqlalchemy.orm.session.Session
            get(reference : str) Batch
            add(batch : Batch)
            list() List~Batch~
        }
        class RedisRepository{
            redis_store: RedisClient
            get(reference : str) Batch
            add(batch : Batch)
            list() List~Batch~
            clear()
        }
        class FakeRepository{
            _batches: Set~Batch~
            get(reference : str) Batch
            add(batch : Batch)
            list() List~Batch~
        }
        class Session{
            execute(command : str)
        }
        class RedisClient{
            add()
            get()
            keys()
            delete()
        }

Testing
-------
Separation of concerns which this pattern introduces shows its power in testing.
All the data repository operations doesn't have to be tested as a part of our app -
they should be tested as a part of their package, we should trust their creators.
The only thing that we have to test is how our models interact with them - without
this level of separation tester would have to use Mocking to for example fake db operations.

Having repository pattern implemented we just have to create FakeRepository class
which will just accumulate references to our domain objects:

.. code-block:: python

    class FakeRepository(AbstractRepository):
        def __init__(self, batches):
            self._batches = set(batches)

        def add(self, batch):
            self._batches.add(batch)

        def get(self, reference):
            return next(batch for batch in self._batches if batch.reference == reference)

        def list(self):
            return list(self._batches)

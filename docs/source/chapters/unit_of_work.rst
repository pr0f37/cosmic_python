####################
Unit of work pattern
####################
The unit of work pattern is used to completely separate the service layer from the orm details.
It encapsulates the repository object and controls its behavior.
For example *SqlAlchemyUnitOfWork* controls *SqlAlchemy* session.
If written in form of context manager it can automatically spawn new session instance and rollback session in case of exception. In some cases it can also be used to automatically commit the session although sqlalchemy creators suggest to close the session explicitly.

Model
-----

.. mermaid::

    flowchart TD
        subgraph SL["Service Layer"]
            subgraph Services
                SL1[/" "/];
                SL2[/" "/];
            end
            subgraph UOW["Unit of Work"]
                sqlUOW["SqlAlchemy UoW"] -.-> absUOW["Abstract UoW"]
            end
            Services --starts--> UOW
        end
        subgraph Repo[Repositories]
            AR["AbstractRepository"]
            SR["SQLAlchemyRepository"] -.-> AR
        end
        subgraph Domain
            id3((" "))
            id2[" "] --> id3
            id1[/" "/] --> id2
        end
        style SL stroke:#9cd, stroke-dasharray:  9
        style Domain stroke:#9cd, stroke-dasharray: 9 9
        style Repo stroke:#9cd, stroke-dasharray: 9 9
        Flask --> Services
        Flask --> UOW
        Repo --> Domain
        SR --> DB[("DB")]
        sqlUOW -->|provides| SR
        absUOW -->|provides| AR
        sqlUOW -->|instantiates db session| DB




Pros and cons
-------------

+---------------------------------------------------+--------------------------------------------+
|Pros                                               |Cons                                        |
+===================================================+============================================+
|* we have a nice abstraction over atomic operations|* might be an overkill for simple apps      |
|* text manager makes it easy to see, what blocks   |* SqlAlchemy offers session object which is |
|  of code are grouped                              |  unit of work already                      |
|* we have nice control over database transactions  |                                            |
|* makes it easier to mock the database connections |                                            |
|  in tests                                         |                                            |
+---------------------------------------------------+--------------------------------------------+

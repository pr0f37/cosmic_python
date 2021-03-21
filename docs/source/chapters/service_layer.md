# Service Layer

The service layer will become an entry point to the application.
Service layer will use repository class to get and save instances of the domain model objects.

```mermaid::

    flowchart TD
        subgraph Domain
            id3((" "))
            id2[" "] --> id3
            id1[/" "/] --> id2
        end
        subgraph SL["Service Layer"]
            allocate[/"services.allocate()"/]
            add_batch[/"services.add_batch()"/]
        end
        subgraph Repo[Repositories]
            AR["AbstractRepository"]
            FR["FakeRepository (In memory)"] -.-> AR
            SR["SQLAlchemyRepository"] -.-> AR
        end

        style SL stroke:#9cd, stroke-dasharray:  9
        style Domain stroke:#9cd, stroke-dasharray: 9 9
        style Repo stroke:#9cd, stroke-dasharray: 9 9

        Tests --invoke--> SL
        Flask --invoke--> SL
        Flask --instantiates--> SR
        Tests --instantiate--> FR
        Repo --retrieves--> Domain
        SL --"models.allocate()"--> Domain
        SL --"list/add batches"----> Repo
        SR --> DB[(Data Base)]

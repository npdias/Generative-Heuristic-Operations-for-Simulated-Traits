## **Abstract**

This project aims to develop a modular framework for the creation of dynamic digital personalities capable of evolving unique traits and behaviors over time. By combining memory management, logical reasoning, sensory integration, and decision-making, the system seeks to enable lifelike interactions, where each entity's personality and demeanor emerge organically based on its experiences. Drawing inspiration from iconic fictional robots such as C-3PO and Marvin the Paranoid Android, the framework will facilitate the development of distinct, context-aware assistants or robotic puppeteers tailored for specialized tasks.

The design prioritizes modularity, allowing seamless integration of diverse AI models to optimize computational efficiency and cost without sacrificing character consistency. While avoiding the ethical and philosophical complexities of true sentience, the system will focus on simulating believable, relatable personalities through adaptive memory and incremental personality evolution. This approach aims to provide a flexible foundation for constructing assistants and robotic interfaces with rich, individualized interactions, contributing to advancements in human-robot collaboration and digital character development.


### Possible Architectural Layout

1. **Domain Layer (Core Models and Logic)**
    
    **Purpose:** Define the core data structures, classes, and logic specific to your application’s “domain.”
    
    **Contents:**
    
    - Data models: `Person`, `Event`, `Fact`, `Conversation`, and `Memory` base class.
    - Core business logic that doesn’t depend on external APIs or I/O. For example, logic related to creating a new memory, updating a person’s attributes, or aggregating facts belongs here.
2. **Application Layer (Use Cases and Interaction Management)**
    
    **Purpose:** Coordinate between domain logic and external systems, implement the “use cases” of your application.
    
    **Contents:**
    
    - Functions and classes that orchestrate interactions between the domain layer, the LLM, and the memory store.
    - `interaction_scripts.py` could be refactored into something like `interactions.py` or `usecases.py`, focusing solely on handling chat sessions, sending messages to the LLM, updating chat logs, and retrieving summaries from memory.
    - This layer defines “what” needs to be done in response to user actions—e.g., “When the user says something, add it to chat history, get a response from the LLM, and log it.”
3. **Infrastructure Layer (I/O, Data Persistence, External APIs)**
    
    **Purpose:** Handle file operations, database access, and external service calls. These are “adapters” for your domain/application layers.
    
    **Contents:**
    
    - File I/O utilities: Reading/writing `chat.json` and `memories.json`.
    - `llm_functions.py` for LLM interaction, possibly renamed to `llm_client.py` or `services/llm_service.py`.
    - `mem_scripts.py` refactored into `memory_repository.py` or `memory_service.py` to load/save memories. The logic for summarizing memory could either stay in the application layer (by calling the LLM service) or remain here if well-structured.
    - A `utils.py` or `infrastructure/` directory to hold common utilities like JSON read/write functions, logging setup, and environment variable handling.
4. **Presentation Layer (Interface with the User)**
    
    **Purpose:** Provide the final interface that the user sees and interacts with (in this case, the console).
    
    **Contents:**
    
    - `console_app.py` handles all user input (prompting, reading) and output (printing responses).
    - The console layer should rely on the application layer to do the “work” and just present results.
    - If in the future you add a GUI or a web interface, you’d create a new layer here without changing your core logic.
5. **Configuration & Setup**
    
    **Purpose:** Centralize configuration, logging setup, and environment loading.
    
    **Contents:**
    
    - A `config.py` or `settings.py` module to load environment variables and provide them to other layers.
    - Logging configuration done once at the entry point of your application so that all layers benefit from a consistent logging setup.

### Example Directory Structure

```graphql
graphql
Copy code
project_root/
│
├─ config.py               # Environment loading, logging config
│
├─ domain/
│  ├─ __init__.py
│  ├─ models.py            # Person, Event, Fact, Conversation, Memory
│  └─ logic.py             # Core domain logic if needed
│
├─ application/
│  ├─ __init__.py
│  └─ interactions.py      # Orchestrates chat sessions, memory operations
│
├─ infrastructure/
│  ├─ __init__.py
│  ├─ memory_repository.py # Manages reading/writing memories.json
│  ├─ chat_repository.py   # Manages reading/writing chat.json
│  ├─ llm_service.py       # Interacts with OpenAI API
│  └─ utils.py             # JSON read/write helpers, other utilities
│
├─ presentation/
│  ├─ __init__.py
│  └─ console_app.py       # Handles console I/O and user prompting
│
└─ main.py                 # Entry point: sets up logging, config, starts console_app

```

### Workflow Example

- **User Input**: The user types a message in `console_app.py`.
- **Application Layer**:`console_app.py` calls a function in `application/interactions.py` that:
    - Saves the user’s message using `infrastructure/chat_repository.py`.
    - Requests a response from `infrastructure/llm_service.py`.
    - Logs the assistant’s response back to `infrastructure/chat_repository.py`.
    - Optionally updates or retrieves relevant data from `infrastructure/memory_repository.py`.
- **Domain Layer**:`interactions.py` or `memory_repository.py` might create or retrieve domain objects (`Person`, `Conversation`) and pass them around. Domain logic is applied as needed.
- **Back to Presentation**:
    
    Finally, `console_app.py` displays the result to the user.
    

### Benefits of This Structure

- **Separation of Concerns**: Each layer has a distinct responsibility, making the code easier to reason about, test, and maintain.
- **Flexibility & Scalability**: Want a new UI? Add it in the presentation layer. Changing storage from JSON to a database? Just swap out `infrastructure` repositories without changing domain logic.
- **Better Testability**: The domain and application layers can be tested independently using mock repositories or mock LLM services, facilitating robust unit tests.
- **Easier Maintenance & Onboarding**: New contributors can understand the codebase faster when each part of the system has a clear purpose.
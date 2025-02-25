# FastCamp Agentes - Atividade prática 3 

## Overview

LeadsAPI is a Python-based project that leverages Pydantic models for managing lead data. The project features various models for handling different lead types (e.g., hot, cold, warm) and provides built-in validations and post-initialization processes for data consistency.

## Features

- **Lead Models:** Utilize Pydantic's `BaseModel` to define and validate lead data.
- **Custom Types and Enums:** Includes custom enumerations for lead priorities, types, and products.
- **Automatic ID Generation:** Uses a custom `StringID` class that generates UUIDs for each lead.
- **Validation and Post-Initialization:** Custom model validators ensure that incoming data meets particular criteria before processing.
- **Unit tests:** Powered by pydantic validation and pytest.

## Project Structure

```
LeadsAPI/
├── pratica/
│   ├── api/
│   │   ├── models/
│   │   │   └── api_leads.py
│   │   └── routes/
│   │       └── leads.py
│   ├── models/
│   │   └── leads.py
│   └── tests/
│       └── tests.py
├── README.md
└── ...
```

## Installation

1. Ensure you have Python 3.9 or later installed.
2. Install the required packages:
   ```
   pip install pydantic
   ```
3. Clone the repository:
   ```
   git clone <repository_url>
   ```
4. Navigate to the project directory:
   ```
   cd LeadsAPI
   ```

## Usage

The models in this project allow you to create, validate, and process different types of leads. For example:
```python
from pratica.models.leads import HotLead

# Creating a hot lead example
hot_lead = HotLead(
    name="John Doe",
    email="john.doe@example.com",
    address="123 Main St",
    phone="+1234567890",
    interests=["two_room_apartment", "three_room_house"],
)
print(hot_lead)
```

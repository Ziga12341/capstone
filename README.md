# Shopping List Voting App

This is a simple voting app that allows users to vote on a shopping list.

## Features

### Accounts

- User registration
- User login
- User logout

### Core

- user can add an item on a shopping list
- users can delete their own item(s) from the shopping list
- users can view the shopping list
- users can vote on items on the shopping list
- users can remove their own vote from an item
- users can view the number of votes on items
- users can post comments on each item

###

- each time users open the page of an item, the comments are marked as already seen or new

### Posting new item

- useL can provide a link for the item, which can lead to the item's page on the web, where the user can buy the item
- for some links to external online stores (like spar-online, tuš, amazon, etc.) the backend will automatically add a
  link to the image of the product

### Optional features
  - a few different permissions (roles) for users:
  - permission to add items
  - permission to delete its own items
  - permission to delete any item
  - permission to see the number of votes on items
  - permission to see who voted on items

## Model diagram

```mermaid
erDiagram
    Suggestions }o--|| User : "suggestion author"
    Suggestions }o--|| Categorised_list : "has suggestions"
    Categorised_list }o--|| Category : "list category"
    Group ||--o{ Categorised_list : "group lists"

    User ||--o{ Group : "group owner"
    User }|--o{ Group : "group member"

    Suggestions ||--o{ Comment : "has comments"

    User ||--o{ Comment : "comment author"
    User }o--o{ Suggestions : "user likes"
    User }o--o{ Suggestions : "user opened suggestion"
```

## Model diagram

```mermaid
erDiagram
    Suggestions }o--|| User : "suggestion author"
    Suggestions }o--|| Categorised_list : "has suggestions"
    Categorised_list }o--|| Category : "list category"
    Group ||--o{ Categorised_list : "group lists"

    User ||--o{ Group : "group owner"
    User }|--o{ Group : "group member"

    Suggestions ||--o{ Comment : "has comments"

    User ||--o{ Comment : "comment author"
    User }o--o{ Suggestions : "user likes"

    Suggestions {
        string name
        date_time created_at
    }

    User {
        url email
    }

    Categorised_list {
        date_time created_at
    }

    Group {
        string name
        string description
        url image
        date_time created_at
    }

    Category {
        string name
        date_time created_at
    }

    Comment {
        string message
        date_time created_at
    }

```

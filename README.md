# a

## 花粉症
**課題**です。

## ER図
```mermaid
erDiagram
    account{
        char name
        varchar sex
        int age
        int po
        varchar place
    }
place_po{
    varchar place
    varchar sit
}

account ||--||place_po: ""


pollen{
    int po
    varchar sit
    date date
    int level
}

pollen }|--|| place_po:""

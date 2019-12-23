# SQL Database Data Model Specification

This document covers the data model of the SQL database. Bolded fields
are indexes.

## Competition
| Field  | Type     | Notes            |
| ------ | -------- | ---------------- |
| **ID** | Int      | Competition ID   |
| Name   | NVARCHAR | Competition name |
| Date   | Date     | Competition Date |

## Group
| Field  | Type     | Notes          |
| ------ | -------- | -------------- |
| **ID** | Int      | Group ID       |
| CID    | Int      | Competition ID |
| Name   | NVARCHAR | Group Name     |

## Category
| Field  | Type     | Notes         |
| ------ | -------- | ------------- |
| **ID** | Int      | Category ID   |
| Name   | NVARCHAR | Category Name |

## Competitor
| Field      | Type     | Notes                                         |
| ---------- | -------- | --------------------------------------------- |
| **ID**     | Int      | Competitor ID                                 |
| CategoryID | Int      | Category ID                                   |
| GroupID    | Int      | Group ID                                      |
| FirstNames | NVARCHAR | Competitor First Names (comma,separated,list) |
| LastName   | NVARCHAR | Competitor Last Name                          |
| BodyWeight | Int      | Competitor weight in grams                    |
| Sex        | Char     | M \| F                                        |

## Attempt
| Field        | Type     | Notes                                     |
| ------------ | -------- | ----------------------------------------- |
| **ID**       | Int      | Attempt ID                                |
| CompetitorID | Int      | Competitor ID                             |
| Status       | NVARCHAR | PASS\|FAIL\|NOTDONE                       |
| Number       | Int      | Trial number                              |
| Discipline   | NVARCHAR | Name of the discipline (Snatch, C&J, ...) |
| Result       | Int      | Result of the attempt                     |
| Unit         | NVARCHAR | Unit of the result (kg \| m \| ...)       |
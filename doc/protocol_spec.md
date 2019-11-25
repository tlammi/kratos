# Protocol Specification

The communication is implemented using *MQTT 3.1.1*.
The specification can be found in http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
MQTT is a publish-subscribe protocol where clients publish and subscribe different
topics and a server (broker) forwards these messages to the correct clients.

![](./graph/mqtt_simple_publish.png)

## Use Cases

### Generic

| Given | When | Then |
| --- | --- | --- |
| The system is operational | A client subscribes to a topic successfully | Following postings to the subject are passed to the client |
| Server is down | A client subscribes to a topic | The transaction fails |
| Server is down | A client posts to a topic | The transaction fails |
| The system is operational | The server fails | Clients notice the drop |
| The server has dropped earlier | The server comes up | Clients notice the server |


### Weightlifting / Power Lifting Specific

#### Judge Unit

| Given | When | Then |
| --- | --- | --- |
| Voting is enabled | One judge presses button | No messages are transmitted |
| Voting is enabled | One judge approves, other disapproves | No messages are transmitted |
| Voting is enabled | Two judges vote the same | Status is transmitted |
| Two judges have voted | 3rd judge votes | Status is transmitted |
| Voting is disabled | A judge presses a button | The press is ignored |
| Votes have been given | a timeout passes | The votes are cleared |
| Some votes are lost | The votes are given manually | The votes are cleared after a timeout automatically |


#### Platform Screen Unit
TBA


## Topic Hierarchy


### Weightlifting / Power Lifting Specific Topics

- CurLifter
  - Name
  - LiftNumber
- Clock
  - Start
  - Stop
  - Time
  - RefreshTime
- JudgeVote
  - JudgeL
  - JudgeM
  - JudgeR
  - VotingEnabled
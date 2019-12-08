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
Topics are organized in decreasing genertity. For example `log/<level>/<unit>`, where log is the most generic part,
then the log level and finally the unit from which the log originates from. Additionally topics matching filter
`$/SYS/#` are reserved for functionality abstracted by MqttEngine and should not be accessed from application level.

### Generic Topics

- `$SYS/log/<level>/<unit>` - Logs with log level \<level\> produced by unit \<unit\>
- `$SYS/heartbeat/<unit>` - Heartbeat (timestamp) of unit \<unit\>
- `$SYS/config/<unit>` - Configuration passed from another program to an unit, for MqttEngine
- `config/<unit>` - Configuration passed from another program to an unit, accessible for application

### Weightlifting / Power Lifting Specific Topics

- `clock/start` - Used for starting a clock unit
- `clock/stop` - Used for stopping a clock unit
- `clock/time/set`- Used for setting the current time
- `clock/time/current` - Used for getting the current time from the unit
- `clock/time/refresh` - Used to tell clock unit to publish the current time to `clock/time/current`
- `clock/expired` - Used for publishing clock expiriration event
- `lifter/current/name/first` - Used for storing the lifter's first name
- `lifter/current/name/family` - Used for storing the lifter's family name
- `lifter/current/barweight` - Weight loaded into the bar
- `lifter/current/liftnumber` - Number of the current lift
- `lifter/next/barweight`- Used for posting the next bar load for the loaders etc.
- `judge/vote/left` - Vote of the left judge (POV of lifter)
- `judge/vote/middle` - Vote of the middle judge (POV of lifter)
- `judge/vote/right` - Vote of the right judge (POV of lifter)
- `judge/vote/enable` - Used for enabling voting
- `judge/vote/disable` - Used for disabling voting

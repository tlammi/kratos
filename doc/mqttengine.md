# MQTT Engine Specification

MQTT engine is implemented by singleton *MqttEngine*. The engine provides
functionality common for all units in *kratos*. This includes support for:
- Connecting to and disconnecting from broker
- Units to register callbacks
- Automatic posting to unit status topics
- Handling all communication that is not unit specific
- (Possible) automatic system mode changes
    - This includes stuff like changing state from *init* to *operational*
      and from *operational* to *shutdown* or *sleep*
    - Implemented if there is a need

## Use Cases
| Given | When | Then |
|---|---|---|
| Topic handlers are registered | Connection is established | Messages to matching topics are received by the topic handlers |
| Connection is disconnected | Connection is reconnected multiple times | Messages matching to topics are received by the topic handlers |
| Connection is established | Connection is lost | Connection is automatically re-established |
| Connection is established | Publish is invoked | Publish is performed |
| Connection is disconnected | Publish is invoked | Error is raised |

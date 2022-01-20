# QueueTokenMicro
[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?https://github.com/jsonzilla/QueueTokenMicro

A small application to use tokens to restart Windows machines

## Deta docs
https://docs.deta.sh/

## Deta clone
deta clone --name queuetoken --project default

## Run local
python -m uvicorn main:app --reload

## Client
Consume tokens, get the machine domain name and use to send a reboot command to the machine.
```
client.py
```

## Tables

### Token (in memory)
Temporary token to consume
```
{ "key": "token" }
```

### Uses
Log the tokens dispatchs to the machines.
"timestamp": datetime,"user": string
```
{
  "timestamp": "2020-01-01T00:00:00.000Z",
  "user": "John Doe"}
```
### Machines:
Relation between tokens and machines.
"key": string, "machine": string, "user": string
```
{ "key": "token", "machine": "id", "user": "John Doe" },
```

## Default Timezone
Need to set your timezone.
'America/Sao_Paulo' set in convert_time.py line 13.

## Load Machines
```
machines_load.py
```
# Follower Maze
Follower Maze is a Socket cleint/server application. It listens on one port for a connection from an event server. On another port it listens on incoming client connections.

It event receiver, receives a CLRF stream of events, it process them and notifies the proper client of that event.

Here are the list of supported events:

* **Follow**: Only the `To User Id` should be notified.
* **Unfollow**: No clients should be notified. 
* **Broadcast**: All connected *user clients* should be notified.
* **Private Message**: Only the `To User Id` should be notified.
* **Status Update**: All current followers of the `From User ID` should be notified.

Enough said :) Now lets go to design.

# Solution
In `main.py` we create a new instance of `FollowerMaze` class.
`FolloweMaze` class gets event service and client listening ports and is responsible for creating two threads of SocketServers, one for EventServiceSocket and one for ClientSocket.

In `server.py` we use Python SocketServer builtin library to creat a new SocketServer which uses `EventHandler` to handle incoming events. EventHandler has a buffer and current sequence id. I've used python builtin heapq for buffer so I can always get the min sequence id from the list. We add item to heap using sequence id. After getting an event I call consume event method which pops from buffer and calls event manager to process the response.

`event_manager.py` holds EventManager which is core logic of FollowerMaze. It has a hash of current connected clients and has methods for add new client and remove them. Key of this hash is client user id and value is the actual ClientHandler object. It also has a follower hash which it's key is a user id and value is list of follower's user_ids.

EventManager receives events from event server and process them. Each supported event has a method which handles any action needed for event and returns list of affected users. And then sends the event to affected users. 

## Run
In order to start the app run the following:
```shell
python main.py
```
This will start both server and client sockets

## Configurations
Most of the configurations are in `config.py`, you can modify following
```python
CLIENT_PORT = 9099
SERVICE_PORT = 9090
EVENT_DELIMITER = "|"
LOG_LEVEL = logging.WARNING
```

## Tests
Currently I have tests for EventManager, you can run them by
```shell
python /tests/test-event-manager.py
```



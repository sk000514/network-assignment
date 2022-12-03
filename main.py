from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json
import time
from src.util import isword, word_generator

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.match_queue: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def getOpponent(self, websocket: WebSocket):
        try:
            index = self.match_queue.index(websocket)
            opponent_websocket = self.match_queue[index -
                                                    (index % 2 * 2 - 1)]
            return opponent_websocket
        except ValueError:
            return None
        except IndexError:
            return 0

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        try:
            tmp = self.match_queue.index(websocket)
            tmp_websocket = self.match_queue.pop(tmp-(tmp % 2*2-1))
            self.match_queue.remove(websocket)
            await tmp_websocket.close()
            await websocket.close()
        except ValueError:
            return 


    async def send_message(self, message: str, websocket: WebSocket):
        if websocket not in self.active_connections:
            websocket.close()
            return
        await websocket.send_text(message)


def generate_message(message_type: str, data: str):
    return {"type": message_type,
            "data": data}


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            json_string = await websocket.receive_text()
            print(json_string)
            json_object = json.loads(json_string)

            if json_object["type"] == 'match':
                manager.match_queue.append(websocket)
                opponent_websocket=manager.getOpponent(websocket)
                if opponent_websocket!=0:
                    message1 = generate_message("match", word_generator())
                    await manager.send_message(json.dumps(message1), websocket)
                    message2 = generate_message("match", word_generator())
                    await manager.send_message(json.dumps(message2), opponent_websocket)
                else:
                    message = generate_message("match", "")
                    await manager.send_message(json.dumps(message), websocket)
            elif json_object["type"] == "guess":
                if isword(json_object["data"]):
                    opponent_websocket = manager.getOpponent(websocket)
                    await manager.send_message(json_string, opponent_websocket)
                else:
                    message = generate_message("guess", "")
                    await manager.send_message(json.dumps(message), websocket)
            elif json_object["type"] == "result":
                opponent_websocket = manager.getOpponent(websocket)
                await manager.send_message(json_string, opponent_websocket)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        return


def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()

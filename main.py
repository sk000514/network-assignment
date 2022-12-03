from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json
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
            opponent_websocket = self.match_queue[index - (index % 2 * 2 - 1)]

            return opponent_websocket
        except ValueError:
            return None

    def disconnect(self, websocket: WebSocket):
        tmp = self.active_connections.index(websocket)
        tmp_websocket = self.active_connections.pop(tmp-(tmp % 2*2-1))
        tmp_websocket.close()
        self.active_connections.pop(tmp)
        websocket.close()

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket not in self.active_connections:
            websocket.close()
            return
        await websocket.send_text(message)


def generate_message(message_type: str, data: str):
    return {"type": message_type,
            "data": data}


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            json_string = await websocket.receive_text()
            json_object = json.loads(json_string)

            if json_object["type"] == 'match':
                manager.match_queue.append(websocket)
                # TODO: 단어 파일에서 임이의 단어 보내주기
                message = generate_message("match", word_generator())
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
        return


def run():
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()

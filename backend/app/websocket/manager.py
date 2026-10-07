from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, dict[int, WebSocket]] = {}

    async def connect(
        self,
        meeting_code: str,
        participant_id: int,
        websocket: WebSocket,
    ):
        await websocket.accept()

        if meeting_code not in self.connections:
            self.connections[meeting_code] = {}

        self.connections[meeting_code][participant_id] = websocket

    def disconnect(
        self,
        meeting_code: str,
        participant_id: int,
    ):
        if meeting_code not in self.connections:
            return

        self.connections[meeting_code].pop(
            participant_id,
            None,
        )

        if not self.connections[meeting_code]:
            del self.connections[meeting_code]

    async def send_to(
        self,
        meeting_code: str,
        participant_id: int,
        message: dict,
    ):
        connection = self.connections.get(
            meeting_code,
            {},
        ).get(participant_id)

        if connection:
            await connection.send_json(message)

    async def broadcast(
        self,
        meeting_code: str,
        message: dict,
        exclude: int | None = None,
    ):
        connections = self.connections.get(
            meeting_code,
            {},
        )

        for participant_id, websocket in connections.items():
            if participant_id == exclude:
                continue

            await websocket.send_json(message)

    def get_participants(
        self,
        meeting_code: str,
    ) -> list[int]:
        return list(
            self.connections.get(
                meeting_code,
                {},
            ).keys()
        )


manager = ConnectionManager()
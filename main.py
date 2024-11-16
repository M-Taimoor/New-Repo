# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from typing import List
# import asyncio

# app = FastAPI()

# # List to keep track of active WebSocket connections
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#         print("Client connected")

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#         print("Client disconnected")

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

# # Initialize the connection manager
# manager = ConnectionManager()

# @app.websocket("/ws/bid")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Broadcasting received bid updates to all clients
#             await manager.broadcast(f"New bid received: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

# # Sample HTML client for testing
# html = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>WebSocket Auction System</title>
# </head>
# <body>
#     <h1>Real-Time Auction Bid Updates</h1>
#     <div id="bids"></div>
#     <input type="text" id="bidInput" placeholder="Enter your bid">
#     <button onclick="sendBid()">Submit Bid</button>

#     <script>
#         const ws = new WebSocket("ws://localhost:8000/ws/bid");

#         ws.onmessage = function(event) {
#             const bids = document.getElementById("bids");
#             const message = document.createElement("p");
#             message.textContent = event.data;
#             bids.appendChild(message);
#         };

#         function sendBid() {
#             const input = document.getElementById("bidInput");
#             ws.send(input.value);
#             input.value = '';
#         }
#     </script>
# </body>
# </html>
# """

# @app.get("/")
# async def get():
#     return HTMLResponse(html)









# ... (other parts of the code remain unchanged)

# Define new message types
MESSAGE_TYPES = {
    "NEW_BID": "new_bid",
    "AUCTION_ENDED": "auction_ended",
    "USER_JOINED": "user_joined"
}

# ... (other parts of the code remain unchanged)

async def broadcast_message(message_type, data):
    message = json.dumps({"type": message_type, "data": data})
    for ws in manager.active_connections:
        await ws.send_text(message)

# ... (other parts of the code remain unchanged)

async def broadcast_summary():
    # Prepare summary data
    summary = {
        "type": MESSAGE_TYPES["AUCTION_ENDED"],
        "data": {
            "winner": auction_state["current_highest_bidder"],
            "winning_bid": auction_state["current_highest_bid"],
            "bid_history": get_bid_history()
        }
    }
    await broadcast_message(MESSAGE_TYPES["AUCTION_ENDED"], summary)

# ... (other parts of the code remain unchanged)

@app.websocket("/ws/bid")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while auction_state["is_active"]:
            data = await websocket.receive_text()
            bid_value = float(data)
            # ... (other parts of the code remain unchanged)
            # When the auction ends, broadcast summary
            if bid_value >= auction_state["minimum_bid"]:
                # ... (other parts of the code remain unchanged)
                await broadcast_summary()  # Broadcast summary at the end of the auction
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ... (other parts of the code remain unchanged)

# Add a function to retrieve bid history for the summary
def get_bid_history():
    cursor.execute("SELECT bidder, bid_amount FROM bid_history ORDER BY id DESC")
    return cursor.fetchall()

# ... (other parts of the code remain unchanged)

<!-- ... (other parts of the HTML remain unchanged -->
<script>
    // ... (other parts of the JavaScript remain unchanged)
    ws.onmessage = function(event) {
        // ... (other parts of the JavaScript remain unchanged)
        if (event.data.type === "NEW_BID") {
            // ... (handle new bids)
        } else if (event.data.type === "AUCTION_ENDED") {
            // Display summary of the auction results
            alert(`Auction ended! Winner: ${event.data.data.winner} with a bid of ${event.data.data.winning_bid}`);
            // Show bid history
            console.log(event.data.data.bid_history);
        } else if (event.data.type === "USER_JOINED") {
            // ... (handle new user joined)
        }
    };
    // ... (other parts of the JavaScript remain unchanged)
</script>
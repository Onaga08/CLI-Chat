# chat.py — Python CLI client using prompt_toolkit and rich for a responsive and styled experience

import asyncio
import websockets
import argparse
import json
import sys
import os
from prompt_toolkit import PromptSession
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

SERVER_URL = os.getenv("CHAT_SERVER_URL", "wss://chat-server-l047.onrender.com/ws")

exit_event = asyncio.Event()
console = Console()

async def send_loop(ws, nickname):
    session = PromptSession()
    console.print("\n[bold green]You can now use these commands:[/bold green]")
    console.print("  [cyan]list[/cyan]")
    console.print("  [cyan]send <user> \"<message>\"[/cyan]")
    console.print("  [cyan]global \"<message>\"[/cyan]")
    console.print("  [cyan]whoami[/cyan]")
    console.print("  [cyan]ping[/cyan]")
    console.print("  [cyan]clear[/cyan]")
    console.print("  [cyan]leave[/cyan]")
    console.print("  [cyan]help[/cyan]")
    while not exit_event.is_set():
        try:
            console.print("[bold red]/chat> [/bold red]", end="", highlight=False)
            command = await session.prompt_async()
            command = command.strip()
            if command == "list":
                await ws.send(json.dumps({"type": "get-users"}))
            elif command.startswith("send"):
                parts = command.split(" ", 2)
                if len(parts) < 3:
                    console.print("[yellow]Usage:[/] send <user> \"message\"")
                    continue
                to_user, msg = parts[1], parts[2].strip('"')
                await ws.send(json.dumps({
                    "type": "send",
                    "to": to_user,
                    "message": msg
                }))
            elif command.startswith("global"):
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    console.print("[yellow]Usage:[/] global \"message\"")
                    continue
                msg = parts[1].strip('"')
                await ws.send(json.dumps({
                    "type": "global",
                    "message": msg
                }))
            elif command == "ping":
                await ws.send(json.dumps({"type": "ping"}))
            elif command == "whoami":
                console.print(f"[green]You are:[/] {nickname}")
            elif command == "clear":
                os.system("cls" if os.name == "nt" else "clear")
            elif command == "leave":
                console.print("[red]Leaving chat...[/red]")
                await ws.close()
                exit_event.set()
                break
            elif command in ("help", "?"):
                console.print("[bold green]Commands:[/bold green] list, send <user> \"message\", global \"message\", whoami, ping, clear, leave")
            else:
                console.print("[red]Unknown command.[/] Type 'help' or '?' for options.")
        except Exception as e:
            console.print(f"[red]Error:[/] {e}")
            exit_event.set()
            break

async def keep_alive(ws):
    while not exit_event.is_set():
        try:
            await asyncio.sleep(30)
            await ws.send(json.dumps({"type": "ping"}))
        except:
            break

async def receive_loop(ws):
    try:
        async for message in ws:
            data = json.loads(message)
            if data["type"] == "message":
                console.print(f"\n[bold blue]{data['from']}[/bold blue]: [white]\"{data['message']}\"")
            elif data["type"] == "global":
                console.print(f"\n🌐 [bold magenta]{data['from']}[/bold magenta] [dim][global][/dim]: \"{data['message']}\"")
            elif data["type"] == "system":
                console.print(f"\n[dim cyan][system][/dim cyan] {data['message']}")
            elif data["type"] == "users":
                console.print("\n[green][users online][/green] " + ", ".join(data["users"]))
            elif data["type"] == "error":
                console.print(f"\n[red][error][/red] {data['message']}")
            elif data["type"] == "pong":
                pass  # hidden
    except websockets.ConnectionClosed:
        console.print("\n[red]Disconnected from server.[/red]")
        exit_event.set()

async def main(nickname, token):
    uri = f"{SERVER_URL}?nickname={nickname}&token={token}"
    try:
        async with websockets.connect(uri) as ws:
            console.print(f"[bold green]Connected as '{nickname}'[/bold green]")
            await asyncio.gather(
                send_loop(ws, nickname),
                receive_loop(ws),
                keep_alive(ws)
            )
    except Exception as e:
        console.print(f"[red]Failed to connect:[/] {e}")
        exit_event.set()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nickname", required=True, help="Your chat nickname")
    parser.add_argument("--token", required=True, help="Auth token")
    args = parser.parse_args()

    asyncio.run(main(args.nickname, args.token))

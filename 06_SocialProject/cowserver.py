import asyncio
import cowsay

NAMES = set(cowsay.list_cows())
accounts = {}

async def chat(reader, writer):
    while not reader.at_eof():
        data = (await reader.readline()).decode().strip().split(maxsplit=1)
        if data:
            match data[0]:
                case 'who':
                    writer.write(f'Logged users list:\n{"\n".join(list(accounts.keys()))}'.encode() + b'\n')
                case 'cows':
                    writer.write('\n'.join(list(sorted(NAMES - set(accounts.values())))).encode() + b'\n')
                case 'login':
                    if len(data) == 1:
                        writer.write('Error: login name is required\n\nusage: login <cow-name>\n'.encode())
                    elif len(data) > 2:
                        writer.write('Error: invalid arguments\n\nusage: login <cow-name>\n'.encode())
                    else:
                        if data[1] not in NAMES:
                            writer.write('Error: invalid cow name\n\nusage: login <cow-name>\n'.encode())
                        elif data[1] in accounts.values():
                            writer.write('Error: a cow with this name is already registered\n'.encode())
                        else:
                            accounts[data[1]] = writer
                            writer.write(f'You are logged in as {data[1]}\n'.encode())
                case 'say':
                    if user is None:
                        writer.write('Error: please register first\n\nusage: login <cow-name>\n'.encode())
                        return 0
                    if len(data) != 2:
                        writer.write('Error: invalid arguments\n\nusage: say <cow-name> <message>"\n'.encode())
                    else:
                        if ' ' in data[1]:
                            cow, msg = data[1].split(maxsplit=1)
                            if cow in accounts.values():
                                if user == accounts[cow]:
                                    writer.write('Error: you cannot send a message to yourself'.encode())
                                wrtr = accounts[cow]
                                wrtr.writer(cowsay.cowsay(msg, cow=accounts[me]).encode() + b'\n')
                                await wrtr.drain()
                            else:
                                writer.write(f'User with name {user} does not exist\n'.encode())
                        else:
                            writer.write('Error: missing message\n\nusage: say <cow-name> <message>\n'.encode())
                case 'yield':
                    if user is None:
                        writer.write('Please register first\n\nusage: login <cow-name>\n'.encode())
                    if len(data) != 2:
                        writer.write('Error: missing message\n\nusage: yield <message>\n'.encode())
                    else:
                        for i, j in accounts.items():
                            if j is not None:
                                writer.write(cowsay.cowsay(data[1], cow=accounts[me]).encode() + b'\n')
                                await writer.drain()
                case 'quit' | 'q':
                    if user is not None:
                        del accounts[user]
                    break
                case _:
                    writer.write('Invalid command\n'.encode())
            await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
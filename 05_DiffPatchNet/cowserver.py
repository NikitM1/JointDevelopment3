import asyncio
import cowsay
import shlex

NAMES = set(cowsay.list_cows())
clients = {}
accounts = {}

async def commandParser(data, me):
    if data:
        match data[0]:
            case 'who':
                await clients[me].put('Logged users list:',*(list(accounts.values())),sep='\n')
            case 'cows':
                await clients[me].put(sorted(NAMES - set(accounts.values())))
            case 'login':
                if len(data) == 1:
                    await clients[me].put('Error: login name is required\n\nusage: login <cow-name>')
                elif len(data) > 2:
                    await clients[me].put('Error: invalid arguments\n\nusage: login <cow-name>')
                else:
                    if data[1] not in NAMES:
                        await clients[me].put('Error: invalid cow name\n\nusage: login <cow-name>')
                    elif data[1] in accounts.values():
                        await clients[me].put('Error: a cow with this name is already registered')
                    else:
                        accounts[me] = data[1]
                        await clients[me].put('You are logged in as', data[1])
            case 'say':
                if me not in accounts.keys():
                    await clients[me].put('Error: please register first\n\nusage: login <cow-name>')
                    return 0
                if len(data) != 2:
                    await clients[me].put('Error: invalid arguments\n\nusage: say <cow-name> <message>')
                else:
                    if ' ' in data[1]:
                        user, msg = shlex.split(data[1])
                        if user in accounts.values():
                            if user == accounts[me]:
                                await clients[me].put('Error: you cannot send a message to yourself')
                            rec = [c for c, v in accounts.items() if v == user][0]
                            await clients[rec].put(cowsay.cowsay(msg, cow=accounts[me]))
                        else:
                            await clients[me].put('Error: user with name', user, 'does not exist')
                    else:
                        await clients[me].put('Error: missing message\n\nusage: say <cow-name> <message>')
            case 'yield':
                if me not in accounts.keys():
                    await clients[me].put('Please register first\n\nusage: login <cow-name>')
                    return 0
                if len(data) != 2:
                    await clients[me].put('Error: missing message\n\nusage: yield <message>')
                else:
                    for i, j in clients.items():
                        if i in accounts.keys() and j is not clients[me]:
                            await j.put(cowsay.cowsay(data[1], cow=accounts[me]))
            case 'quit' | 'q':
                if me in accounts:
                    del accounts[me]
                elif me in clients:
                    del clients[me]
                    return 1
            case _:
                await clients[me].put('Invalid command')

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                data = shlex.split(q.result().decode())
                answer = await commandParser(data, me)
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write((str(q.result())+'\n').encode())
                await writer.drain()
        if answer:
            break
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
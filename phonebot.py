import discord
from TOKENS import token

import asyncio
from mansion import id_to_room_name, room_name_to_id
#from characters import id_to_character_name

client = discord.Client()

@client.event
async def on_ready():
    sms_test_guild = client.get_guild(967113761049702400)
    global room_to_room_role
    room_to_room_role = {
        971367884766998598: discord.utils.get(sms_test_guild.roles, id=972030782405214208),
        971427909589958657: discord.utils.get(sms_test_guild.roles, id=972030947266555934),
    }
    print(f"\033[31mLogged in as {client.user}\033[39m")

class off: pass

"""
class Room:
    def __init__(self, room_id, room_name, role=None):
        self.id = room_id
        self.name = room_name
        self.role = role
        self.characters = set()
        
    def __repr__(self) -> str:
        return f"Room({self.id}, {self.name})"

    def __str__(self) -> str:
        return self.name
    
    def walk_in(self, character):
        self.characters.add(character)
        character.room = self
    
    def walk_out(self, character):
        self.characters.remove(character)
        character.room = None
"""

class Character:
    def __init__(self, id, name, member=None, in_room_id=None):
        self.id = id
        self.name = name
        self.member = member
        self.room_id = in_room_id
        self.phone = Phone(self)
        self._room_role = None
    
    def __repr__(self) -> str:
        return f"Character({self.id}, {self.name})"
    
    def __str__(self) -> str:
        return self.name

    def get_room(self):
        #get channel by id
        channel = clients.phone.get_channel(self.room_id)
        return channel
    
    async def switch_out_room_role(self, room_id):
        if self._room_role is not None:
            await self.member.remove_roles(self._room_role)
        self._room_role = room_to_room_role[room_id]
        await self.member.add_roles(self._room_role)

    def set_room(self, room):
        if self.room_id not in id_to_room_name.keys():
            self.room_id = room.id

class Phone:
    def __init__(self, owner):
        self.owner = owner
        self.in_a_call_with = None
        self.is_being_called_by = None
        self.is_on = True
        self.unanswered_calls_from = []
        self.testing = False

    def __repr__(self) -> str: return f"Phone({self.owner.name})"
    
    def __str__(self) -> str: return f"{self.owner.name}'s phone"

    class Busy(Exception): pass
    class IsOff(Exception): pass
    class NotRinging(Exception): pass
    class NotInCall(Exception): pass

    async def initiate_call(self, other_character, message):
        other_phone = other_character.phone
        if other_phone.in_a_call_with is None and other_phone.is_being_called_by is None:
            if other_phone.is_on:
                #await react_thumbs_up(message)
                other_phone.is_being_called_by = self
                await other_character.get_room().send(
                    f"{self.owner} is calling you!\n"
                    f"||(Use *.answers* or *.hangs up*)||"
                )
            else:
                other_phone.unanswered_calls_from.append(self.owner.name)
                raise Phone.Busy
        else:
            #await message.channel.send(f"*busy signal*")
            raise Phone.Busy
    
    """
    def is_in_a_call(self):
        if not self.is_on:
            raise Phone.IsOff
        elif not self.in_a_call_with is None:
            return True
    """

    def answer_call(self):
        if not self.is_being_called_by is None:
            #await react_thumbs_up(message)
            self.in_a_call_with = self.is_being_called_by
            self.is_being_called_by = None
            other_phone = self.in_a_call_with
            other_phone.in_a_call_with = self
        else:
            #await message_invalid(message)
            raise Phone.NotRinging
    
    def hang_up(self):
        if not self.in_a_call_with is None:
            self.in_a_call_with.in_a_call_with = None
            self.in_a_call_with = None
        elif not self.is_being_called_by is None:
            self.is_being_called_by.is_being_called_by = None
            self.is_being_called_by = None
        else:
            raise Phone.NotInCall

    def turn_off(self):
        if self.is_on:
            self.in_a_call_with = None
            self.is_being_called_by = None
            self.is_on = False
        else:
            raise Phone.IsOff

    def turn_on(self):
        self.is_on = True
    
    async def forward_message(self, message):
        if (not self.in_a_call_with is None) and (not self.in_a_call_with is off):
            await self.in_a_call_with.owner.get_room().send(
                f"{self.owner.name}> {message.content}"
            )
    
    async def forward_typing(self):
        if (not self.in_a_call_with is None) and (not self.in_a_call_with is off):
            await self.in_a_call_with.owner.get_room().trigger_typing()

"""
phone = Phone(Character(0, "test"))   
phone.testing = True     
import pdb; pdb.set_trace()
"""
"""
character_name_to_character_object = {
    "Roomba": Character(496709767914586112, "Roomba", in_room_id=967113761808859269),
    "Theo": Character(687974477312557097, "Theo", in_room_id=967113761808859269),
    "Paddy": Character(718094142428676126, "Paddy", in_room_id=971367884766998598),
}

id_to_character_name = {}
for character in character_name_to_character_object.values():
    id_to_character_name[character.id] = character.name
"""

id_to_character={}
tupper_id = 970719634015789096

"""
def get_character_by_member(member):
    if member.id in id_to_character.keys():
        return id_to_character[member.id]
    elif member.name in id_to_character.keys():
        return id_to_character[member.name]
    else:
        raise KeyError
"""

class characters:
    id_to_character = {}
    name_to_id = {}
    tupper_id = 970719634015789096

    def __init__(self, characters):
        for character in characters:
            self.id_to_character[character.id] = character
            self.name_to_id[character.name] = character.id
    
    def __repr__(self) -> str:
        return f"characters({list(self.id_to_character.values())})"

    def new_character(self, member, character_name):
        if character_name in self.name_to_id.keys():
            raise KeyError
        else:
            if not member.id == tupper_id:
                character_id = member.id
            else:
                character_id = member.name
            character = Character(character_id, character_name, member)
            self.id_to_character[character_id] = character
            self.name_to_id[character_name] = character_id
            return character

    def get_character_by_name(self, character_name):
        if character_name in self.name_to_id.keys():
            return self.id_to_character[self.name_to_id[character_name]]
        else:
            print(f"{character_name} not found")
            raise KeyError
        
    def get_character_by_member(self, member):
        if member.id in self.id_to_character.keys():
            return self.id_to_character[member.id]
        elif member.name in self.name_to_id.keys():
            return self.get_character_by_id(self.name_to_id[member.name])
        else:
            raise KeyError

"""
Character(496709767914586112, "Roomba", in_room_id=967113761808859269),
    "Theo": Character(687974477312557097, "Theo", in_room_id=967113761808859269),
    "Paddy": Character(718094142428676126, "Paddy", in_room_id=971367884766998598),
"""

characters = characters([
    Character(496709767914586112, "Roomba"),
    Character(687974477312557097, "Theo"),
    Character(718094142428676126, "Paddy"),
])

async def send_message_as(client, channel_id, message):
    #get channel
    channel = client.get_channel(channel_id)
    #send message
    await channel.send(message)

async def react_thumbs_up(message):
    await message.add_reaction("👍")

async def message_invalid(message):
    #delete an invalid message
    await message.delete()

async def parse_command(command, message):

    #get character
    try:
        self = characters.get_character_by_member(message.author)
    except KeyError:
        pass

    if ".calls" in command:
        callee_name = command.split(".calls")[1].split(" ")[1].strip().strip("*")
        callee = characters.get_character_by_name(callee_name)
        print(f"{self.name} is calling {callee.name}")
        try:
            await self.phone.initiate_call(callee, message)
        except Phone.Busy:
            await message.channel.send("*busy signal*")
        else:
            await react_thumbs_up(message)

    elif ".answers" in command:
        try:
            self.phone.answer_call()
        except Phone.NotRinging:
            await message_invalid(message)
            await message.channel.send("||(Not ringing)||")
        else:
            await react_thumbs_up(message)

    elif ".hangs up" in command:
        try:
            self.phone.hang_up()
        except Phone.NotInCall:
            await message_invalid(message)
            await message.channel.send("||(Not in a call)||")
        else:
            await react_thumbs_up(message)

    elif  any(x in command for x in [
        ".checks phone", ".checks the phone", ".checks messages"
    ]):
        if len(self.phone.unanswered_calls_from) == 1:
            calls = self.phone.unanswered_calls_from[0]
            await message.channel.send(
                f"*You have an unanswered call from {calls}*"
            )
            self.phone.unanswered_calls_from = []
        elif len(self.phone.unanswered_calls_from) > 1:
            number_of_calls = len(self.phone.unanswered_calls_from)
            calls = ", ".join(self.phone.unanswered_calls_from)
            await message.channel.send(
                f"*You have {number_of_calls} unanswered calls from {calls}*"
            )
            self.phone.unanswered_calls_from = []
        else:
            await message.channel.send("*You have no unanswered calls*")

    elif any(x in command for x in [".turns phone on", ".turns on phone"]):
        try:
            self.phone.turn_on()
        except Phone.IsOff:
            await message_invalid(message)
            await message.channel.send("||(Already on)||")
        else:
            await react_thumbs_up(message)

    elif any(x in command for x in [
        ".turns phone off", ".turns off phone", ".turns the phone off", ".turns off the phone"
    ]):
        try:
            self.phone.turn_off()
        except Phone.IsOff:
            await message_invalid(message)
            await message.channel.send("||(Already off)||")
        else:
            await react_thumbs_up(message)

async def parse_commands(message):
    commands = message.content.split(".")[1:]
    for command in commands:
        await parse_command(f".{command}", message)

@client.event
async def on_message(message):
    if message.author == clients.phone.user: return
    if ":" in message.content: return

    try:
        self = characters.get_character_by_member(message.author)
    except KeyError:
        # add x emoji if message contains a dot
        if "." in message.content:
            await message.add_reaction("❌")
    else:
        if self.member is None:
            self.member = message.author
        if not message.content.startswith("("):
            self.set_room(message.channel)
            await self.switch_out_room_role(message.channel.id)
        await self.phone.forward_message(message)

        if "." in message.content:
            try:
                await parse_commands(message)
            except Exception:
                import traceback
                error = traceback.format_exc()
                await message.channel.send(f"||{error}||")
        if message.content.startswith("!my name is"):
            await message.channel.send(f"*{self.name}*")

    if message.content.startswith("!add"):
        _, name, *_ = message.content.split(" ")
        characters.new_character(message.author, name)
        await message.add_reaction("✅")


    if message.content.startswith("!dump_characters"):
        await message.channel.send(str(characters)) 
    
    if message.content.startswith("%"):
        import io
        import sys
        import traceback

        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            request_str = message.content[1:]
            
            try:
                exec(
                    "async def request_funct(other_locals):\n"
                    "    locals().update(other_locals)\n"
                    f"    return_value = ({request_str})\n"
                    "    globals().update(locals())\n"
                    "    return return_value\n"
                    "globals().update(locals())\n"
                )
            except:
                request = request.replace('\n', '\n    ')
                exec(
                    "async def request_funct(other_locals):\n"
                    "    locals().update(other_locals)\n"
                    f"    {request_str}\n"
                    "    globals().update(locals())\n"
                    "    return return_value\n"
                    "globals().update(locals())\n"
                )
            return_value = await request_funct(locals())

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

            if return_value != None:
                output = str(return_value) + "\n" + output
        except Exception:
            error = traceback.format_exc()
            await message.channel.send(f"```\n{error}\n```")
        else:
            if not len(output) > 2000:
                await message.channel.send(output)
            else:
                await message.channel.send(
                    file=discord.File(io.BytesIO(output.encode()), 
                    filename="output.txt")
                )

    """
    print(message.content)
    global messages
    messages.append((message.content, message.author.id, message.channel.id, message.id, message.created_at, message.edited_at, message.attachments))
    if message.content.startswith("!dump_messages"):
        import io
        await message.channel.send(
            file=discord.File(io.BytesIO(str(messages).encode()), filename="messages.txt")
        )
    """

@client.event
async def on_typing(channel, user, when):
    if user == clients.phone.user:
        return
    #self = character_name_to_character_object[id_to_character_name[user.id]]
    #self.set_room(channel)
    #await self.phone.forward_typing()

        
        
if __name__ == "__main__":
    client.run(TOKEN)

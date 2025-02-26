import discord
import responses
import sys
sys.path.append('M:\VSCode Projects')
from discordbotconfig import TOKEN
import SmiteDataAPI
from discord.ui import Button, View
from SmiteAPIFrameFolder.smitedatabasetest import *
import fuzzyquarters
import fuzzygodnames
from ImageMasher import image_gen
from discord import application_command

from MainMudaeAutoScript import Auto_Roller
import re
from datetime import datetime, timedelta
import asyncio
import os
import random
# import asyncio
# import twitchlivechecker
from discord.ext import tasks,commands
from dhooks_lite import Webhook, Embed

from wikiimgtaker import auto_downloader_and_namer

guild_list = []
user_id_cache = set()

async def send_message (message, user_message, is_private):
    try: 
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

# async def twitch_live_notification():
#     channel = bot.get_channel(1040601561698684948)
#     button = Button(label="Smitegame", url="https://www.twitch.tv/smitegame")
#     view = View(button)
#     await channel.send("GET IN HERE!! @everyone", view=view)

async def twitch_live_notification():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Bot(intents=intents)

    channel = bot.get_channel(1040601561698684948)
    button = Button(label="Smitegame", url="https://www.twitch.tv/smitegame")
    view = View(button)
    await channel.send("GET IN HERE!! @everyone", view=view)
    return

def run_discord_bot():
    
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Bot(intents=intents)
    guild_list = []
    

    @bot.event
    async def on_ready():
        print (f'{bot.user} is now running!')
        channel = bot.get_channel(1040601561698684948)
        for guild in bot.guilds:
            global guild_list
            #guild_list.append(guild.id)
            print(f'Guild ID: {guild.id}')
            print(guild_list)
        await channel.send("The Normal on ready")
        # @tasks.loop(seconds=6.0)
        # async def twitch_live ():
        #     notification = twitchlivechecker.channel_checker("smitegame")
        #     if notification:
        #         button = Button(label="Smitegame", url="https://www.twitch.tv/smitegame")
        #         view = View(button)
        #         await channel.send("GET IN HERE!! @everyone", view=view)
        #         #print("we in there")
        #     else:
        #         print("not in there")
        
        # await twitch_live.start()


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        message_emoji_list = ["🎨", "🎩"]
        w = "🤠"
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        user_embed = (message.embeds)
        save_embed = {}
        #embed_content_in_dict = message.embeds[0].to_dict()
        for embeding in user_embed:
            print(f"This is the embedding: {embeding.to_dict()}")
            save_embed = embeding.to_dict()
        if save_embed:
            print(f'{username} said: "{user_message}" ({channel}) or said (Embed): {user_embed} / {save_embed["description"]}')
            pattern1 = re.compile(r'\*\*\s*\d+\s*\*\*')
            match = re.search (pattern=pattern1, string= (save_embed["description"]))
            pattern2 = re.compile(r'\*\*\s*517\s*\*\*')
            match2 = re.search (pattern=pattern2, string= (save_embed["description"]))
            if match:
                for emoji in message_emoji_list:
                    await message.add_reaction(emoji)
            if match2:
                await message.add_reaction(w)
        # if user_message[0] == '?':
        #     user_message = user_message[1:]
        #     await send_message(message, user_message, is_private=True)
        # else:
        #     await send_message(message, user_message, is_private=False)

    @bot.slash_command(name = "online", description = "See if this bot is on or off")
    async def work(ctx):
        print(guild_list)
        ctx.guild_ids = guild_list
        await ctx.respond(f'I am online pog! \n\nLatency: {bot.latency*1000} ms.')

    @bot.slash_command(description = "My current usage of Smite API")
    async def mydata(ctx):
        # sessionid = SmiteDataAPI.valid_session_check()
        # print(guild_list)
        # ctx.guild_ids = guild_list
        # data = SmiteDataAPI.MyData(sessionid)
        # await ctx.respond(data)
        data = MyData()
        await ctx.respond(data)

    @bot.slash_command(description = "Create my table")
    @discord.option(
    "daysago", 
    description="Getting data from (1-14) days prior. Default = 1",
    required=False,
    default = 1
    )
    async def createtable(ctx, daysago:int):
        #sessionid = SmiteDataAPI.valid_session_check()
        
        #ctx.guild_ids = guild_list
        if (daysago < 1) or (daysago > 14):
            await ctx.respond(f"Invalid entry.")
            return
        
        await ctx.defer()
        #await ctx.respond(f"Working its magic...")
        MatchIDTest(days_ago=daysago)
        #await ctx.respond(f"Completed")
        await ctx.followup.send("Completed Successfully")
    
    @bot.slash_command(description = "insert into database")
    @discord.option(
    "daysago", 
    description="Getting data from (1-14) days prior. Default = 1",
    required=False,
    default = 1
    )
    async def insertdailydatabase(ctx, daysago:int):
        #sessionid = SmiteDataAPI.valid_session_check()
        
        #ctx.guild_ids = guild_list

        if (daysago < 1) or (daysago > 14):
            await ctx.respond(f"Invalid entry.")
            return
        
        await ctx.defer()
        await databasetest(days_ago=daysago)
        await ctx.followup.send(f"Completed Successfully")
        
    @bot.slash_command(guild_ids = [173641386686414849], name = "cooldowns", description = "Gives a random god's cooldowns")
    async def cooldowns(ctx, godname: str):
        godIcon = SmiteDataAPI.findingGodURL(godname=godname)
        godCD = SmiteDataAPI.Cooldowns(godname=godname)
        await ctx.respond(f'{godIcon}')
        await ctx.respond(f'{godCD}')

    @bot.slash_command(guild_ids = [173641386686414849, 317496010584621056], name = "emojicheck", description = "checking emojis")
    async def emojicheck(ctx):
        await ctx.respond('A custom emoji: <:BryceNapkin:370673315552952330> /n also <:b:370673368543789056> <:emoji:370673368543789056>')

    





    prev_winrate_options = ["Weekly", "Monthly"]  
    prev_winrate_selection = discord.Option(str, autocomplete=discord.utils.basic_autocomplete(prev_winrate_options),
                            required=False,description=f"Change query from (1)day --> to (7)days or (31)days of stats")
    @bot.slash_command( description = "Shows the winrate of a god for the previous day.", 
                       integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        )
    @discord.option(
    "godname", 
    description="Enter the God's name",
    required=True
    )
    @discord.option(
    "daysback", 
    description="Enter how many days ago for the query. [Default = 1]",
    required=False,
    default = 1
    )
    # @discord.option(
    # "godname", 
    # description="Enter the God's name",
    # required=True
    # )
    # @discord.option(
    # "godname", 
    # description="Enter the God's name",
    # required=True
    # )
    async def daily_winrate(ctx, godname:str, calendar_unit: prev_winrate_selection, daysback:int): # type: ignore


        
        fuzzy_godname = None
        role_icon_dictionary = {
            "jungle" : "<:jungle_icon:1252763219861180488>",
            "support" : "<:support_icon:1252763222369636362>",
            "carry" : "<:adc_icon:1252763217080352789>",
            "mid" : "<:mid_icon:1252763220532527105>",
            "solo" : "<:solo_icon:1252763221622784161>",
            "fill" : "<:fill_icon:1252763218653352020>"
        }

        async def daily_winrate_main():
            test_list = ['jungle', 'mid', 'solo', 'carry', "support"]
            daily, weekly, monthly, special = None, None, None, None

            if calendar_unit is None:
                _, _, month, day = get_previous_day_month_name(days_ago=daysback)
                yesterdayday = f'{month} {day}'
                daily = 1 
            elif calendar_unit == 'Weekly':
                _, _, month, day = get_previous_day_month_name(days_ago=daysback)
                _, _, month_start, day_start = get_previous_day_month_name(days_ago=daysback + 6)
                yesterdayday = f'{month_start} {day_start} --> {month} {day}'
                weekly = 1
            elif calendar_unit == 'Monthly':
                _, _, month, day = get_previous_day_month_name(days_ago=daysback)
                _, _, month_start, day_start = get_previous_day_month_name(days_ago=daysback + 30)
                yesterdayday = f'{month_start} {day_start} --> {month} {day}'
                monthly = 1
            elif calendar_unit == "Me":
                _, _, month, day = get_previous_day_month_name(days_ago=daysback + 3)
                _, _, month_start, day_start = get_previous_day_month_name(days_ago=daysback +10)
                yesterdayday = f'{month_start} {day_start} --> {month} {day}'
                special = 1



            overall_wins, overall_losses, total_games, role_wins_list, role_losses_list, role_list, god_icon_daily = await daily_winrate_query(godname=fuzzy_godname, roles_queried=test_list, days_back=daysback, daily=daily, weekly=weekly, monthly=monthly, is_special=special)
            if not total_games:
                await ctx.respond(f"{fuzzy_godname} did not play any games yesterday. Trash god.")
                return
            #     await ctx.respond(f"{fuzzy_godname} won {wins} games and lost {losses} games out of {total_games} total games yesterday. \n\tWinrate-->{((wins/total_games)*100):.2f}%")
            # else:
                
            
            # print(f"1 {role_wins_list} AND {type(role_wins_list)}")
            # print(f"2 {role_losses_list} AND {type(role_losses_list)}")
            # print(f"3 {role_list} AND {type(role_list)}")
            # # Get today's date
            # today = datetime.now()

            # # Subtract one day
            # yesterday = today - timedelta(days=1)

            # # Print the result
            # #print(yesterday.strftime("%B %d"))
            # yesterdayday = yesterday.strftime('%B %d')

            


            
            embed = discord.Embed(title=f"{fuzzy_godname.upper()}", description=f"> Daily stats ", color=discord.Colour.from_rgb(25,150,25))
            #embed.set_thumbnail(url=f"{godIcon}")
            embed.set_thumbnail(url=f"{god_icon_daily}")
            #embed.set_image(url=f"{skin_URL_list[0]}")
            embed.set_footer(text=f"Based on completed games in Ranked Conquest\t\t\t\tDATE: {yesterdayday}")
            embed.add_field(name="Overall Win", value=f"{overall_wins}", inline=True)
            embed.add_field(name="Overall Loss",value=f"{overall_losses}", inline=True)

            int_overallwinrate = f"{((overall_wins/total_games)*100):.2f}"
            embed.add_field(name="Overall Winrate", value=f"{int_overallwinrate}%", inline=True)

            blueTUPLE = 0
            greenTUPLE = int((((overall_wins/total_games) - .40) / .2) * 255)
            if greenTUPLE < 0:
                greenTUPLE = 0
            if greenTUPLE > 255:
                greenTUPLE = 255
            redTUPLE = (255 - greenTUPLE)
            embed.color = embed.color.from_rgb(redTUPLE,greenTUPLE,blueTUPLE)

            embed.add_field(name="", value="\n\n\n", inline=False)



            embed.add_field(name="Win/Loss", value="", inline=True)
            embed.add_field(name="Winrate",value="", inline=True)
            embed.add_field(name="Role Queued",value="", inline=True)


            #There is so much shit i had to change here to get it to work, so you will have to rewrite it to make it look better next time
            #Just remember, if you get that set and set type error again, just have some dummy variable to hold the value
            #But we can make fields using for loops ayeee AND you dont need a name or value parameter (need 1 or the other though) 
            #Now that I got it to work, I think one of the problems is that I was using too many brackets, meaning it may be salvagable

            #for role_wins,role_losses,role_type in zip(role_wins_list,role_losses_list,role_list):
            for i in range (len(role_list)):
                if role_wins_list[i] is None:
                    role_wins_list[i] = 0
                if role_losses_list[i] is None:
                    role_losses_list[i] = 0
                role_total = int(role_wins_list[i])+int(role_losses_list[i])
                role_total = int(role_total)
                
                #print(f"role type: {role_list[i]} type {type(role_list[i])} | role wins: {role_wins_list[i]} type {type(role_wins_list[i])} | role losses: {role_losses_list[i]} type {type(role_losses_list[i])} | role total: {role_total} type {type(role_total)}")


        
                field1 = f'{role_wins_list[i]:3d}W | {role_losses_list[i]:3d}L'
                embed.add_field(name="",value=f"{field1}", inline=True)

                int_role_wins = int(role_wins_list[i])
                int_role_total = int (role_total)
                field2 = f'{((int_role_wins/int_role_total)*100):.2f}' if int(role_total) else f'N/A'
                if (field2 == 'N/A'):
                    embed.add_field(name="", value=f"{field2}",inline=True)
                #field2 = f'{((({role_wins_list[i]})/({int(role_total)}))*100):.2f}%' if int(role_total) else f'N/A'
                else:
                    embed.add_field(name="", value=f"{field2}%" if float(field2) < float(int_overallwinrate) else f'**{field2}%**',inline=True)

                field3 = f"{((int_role_total/total_games)*100):.2f}" if total_games else f'N/A'
                #field3 = f"{role_icon_dictionary[role_list[i]]} {((({int(role_total)})/({int(total_games)}))*100):.2f}%" if role_total else f'N/A'
                #embed.add_field(name="\u200B", value='\u200B')
                if (field3 == 'N/A'):
                    embed.add_field(name="",value=f"{role_icon_dictionary[role_list[i]]} {field3}%", inline=True)
                else:
                    embed.add_field(name="",value=f"{role_icon_dictionary[role_list[i]]} {field3}%" if float(field3) < 20.00 else f'**{role_icon_dictionary[role_list[i]]} {field3}%**',inline=True)
            # await ctx.respond( embed=embed)
            msg = await ctx.respond(f"Loading...")
            await asyncio.sleep(1)
            await msg.edit( content= None,embed=embed)
            
            
            


        #All 3 possible outcomes for the queried input (Max of 3 fuzz results)
        async def godselect1_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.defer()
            nonlocal fuzzy_godname
            #print(fuzzy_godname)
            fuzzy_godname = fuzzy_godname_list[0]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content = f"{fuzzy_godname}", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_godname.title()} Selected!", view=view)
            await daily_winrate_main()
        async def godselect2_callback(interaction):
            view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            #await interaction.response.defer()
            nonlocal fuzzy_godname
            #print(fuzzy_godname)
            fuzzy_godname = fuzzy_godname_list[1]
            #await interaction.response.defer()
            await interaction.response.edit_message(content = f"{fuzzy_godname.title()} Selected!", view=view)
            
            await daily_winrate_main()
        async def godselect3_callback(interaction):
            view = View()
            #await interaction.response.defer()
            nonlocal fuzzy_godname
            fuzzy_godname = fuzzy_godname_list[2]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content ="hello3", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_godname.title()} Selected!", view=view)
            await daily_winrate_main()

        #Processes which state name someone tries to input
        if godname:
            fuzzy_godname_list = await fuzzygodnames.fuzzysearch(str(godname))
            if len(fuzzy_godname_list) == 1:
                fuzzy_godname = fuzzy_godname_list[0]
                await daily_winrate_main()
            elif len(fuzzy_godname_list) == 2:
                name1 = Button(label=f"{fuzzy_godname_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_godname_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                view = View(name1, name2, timeout=30.0)
                name1.callback = godselect1_callback
                name2.callback = godselect2_callback
                await ctx.response.send_message("Which God were you refering to? (30s)", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
            elif len(fuzzy_godname_list) == 3:
                name1 = Button(label=f"{fuzzy_godname_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_godname_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                name3 = Button(label=f"{fuzzy_godname_list[2]}", style=discord.ButtonStyle.green, emoji="🥉")
                view = View(name1, name2, name3)
                name1.callback = godselect1_callback
                name2.callback = godselect2_callback
                name3.callback = godselect3_callback
                #await ctx.respond(data)
                await ctx.response.send_message("Which God were you refering to?", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
        else:
            fuzzy_godname_list = await fuzzygodnames.fuzzysearch(str(godname))
            await daily_winrate_main()

    @bot.slash_command(guild_ids = guild_list, name = "buttontest", description = "Tests my buttons")
    async def buttons(ctx, style: int):

        #
        button = Button(label="BALLS!!", style=discord.ButtonStyle.green, emoji="💋")
        button2 = Button(label="Yaaaaasssss", style=discord.ButtonStyle.red, emoji="💅")
        button3 = Button(label="Susano", url="https://webcdn.hirezstudios.com/smite/god-skins/susano_luminosity.jpg")

        async def button2_callback(interaction):
            #When this button is clicked, it sends a new message (replies to itself)
            await interaction.response.send_message("No idea what this means")

        async def button_callback(interaction):
            #When this button is clicked, it edits its original message (no replies), also can edit the button view. 
            #Use this for like a scroller, aka mudae
            view = View(button3)
            
            await interaction.response.defer()
            await interaction.edit_original_response(content = "Buttons changed", view=view)
            

            
        #Callback is basically what a button does when someone clicks it
        button2.callback = button2_callback
        button.callback = button_callback

        if style > 5:
            view = View(button3 ,button, button2)
        else:
            view = View(button2, button)
        await ctx.respond("ORIGINAL MESSAGE !!!", view=view)
    @bot.slash_command(name = "help", description = "Dms bot commands and other stuff")
    async def help_me(ctx):
        embed = discord.Embed(title="", description="Yea, I'll see if this works")
        user_id = int(ctx.author.id)
        the_user = await bot.fetch_user(user_id)
        await the_user.send(embed=embed)
        await ctx.respond("DM Sent, Enjoy the bot :)")
    @bot.slash_command(name = "returnuser", description = "testing")
    async def returnuser(ctx):
        author = (ctx.author)
        authorid = int(ctx.author.id)
        usercheck = str(ctx.user)
        
        for_me = await bot.fetch_user(authorid)
        for_streep = await bot.fetch_user(103266894953353216)
        #Mentioning only works using the value field, not Name field
        #embed.add_field(name = f"{for_me.mention}", value=f"",inline=False)
        embed = discord.Embed(title=f"")
        embed.add_field(name = "",value= f"{for_me.mention}",inline=False)
        embed.add_field(name = "",value= f"{for_me.avatar}",inline=False)
        embed.add_field(name = "",value= f"{for_streep.mention}",inline=False)
        embed.add_field(name = "",value= f"<@167754998376038400>",inline=False)

        avatar_getter_dict = {
            "ProfPickleRick" : 173314591118327808,
            "Richter_Cade" : 91391586537062400,
            "Nacrusia" : 141307225661505536,
            "Reaper" : 187740584838955008,
            "MrWoott" : 213864579774676992,
            "BiackEye" : 206256272641753088,
            "Rosy" : 145012681819160578,
            "Kylis" : 227122892016451584,
            "Nightl0ck9" : 248592469057339392,
            "nbright03" : 330253028416552960,
            "Jordanrey13" : 402287539119063051,
            "PrincesS" : 428481851129069570,
            "limbo_jimbo1" : 488535517043097600,
            "Strat" : 580555513213747200,
            "SYS_Bradmin" : 1264007881729245205,
            "Sheen" :287069418595549184,
            "Mujtabaa" : 167754998376038400,
            "Hawkeyez" : 332251639690035200,
            "SuspectJoey" : 329612070507249665,
            "tion" : 467086896263331840,
            "JMac" : 95395371471077376,
            "LokiDad" : 132356959864094720,
            "UpgradeOnly" : 371759295324356618,
            "Dakota_(Cop)" : 243173207694245889,
            "Full_Of_Soup" : 309092335571173376,
            "Jithins" : 122141060125163520,
            "Odd_But_God" : 329780711680638976,
            "Latent" : 90383066668736512,
            "Number1SonixFan_(Kyletheginger)" : 551865403052392449,
            "Tdog" : 105778729904525312,
            "Zoartasarr" : 481862270415142952,
            "Tempy" : 105116713535733760,
            "Lahthel" : 198813812051279872,
            "Jae_Kobra" : 252232299133796353,
            "fishdinnersh" : 468511156680654859,
            "Alandiamond1" : 707011771709522030,
            "Cal" : 184430099704184832



        }
        
        #path_list, path1=auto_downloader_and_namer(god_image_URL_list=["https://cdn.discordapp.com/avatars/167754998376038400/91fa61422c538a7c8aecc663d8fe0406.png?size=1024"],folder_name='discord_pfp')
        async def avatar_getter_main():
            avatar_url_list = []
            username_filename_list = []
            for username in avatar_getter_dict:
                current_user = await bot.fetch_user(avatar_getter_dict[username])
                avatar_url = current_user.avatar
                avatar_url_list.append(avatar_url)
                username_filename_list.append(username + '.png')

            for URL_link,img_name in zip(avatar_url_list,username_filename_list):
                headers = {'Accept': 'image/png'}
                response = requests.get(URL_link, headers=headers)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    current_script_path = os.path.dirname(os.path.abspath(__file__))
                    skins_folder_path = os.path.join(current_script_path, 'discord_pfp')
                    file_path = os.path.join(skins_folder_path, img_name)
                    
                    #filename = f'{icon_name}'  # You can specify the file name here

                    # Write the content of the response to a file
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image downloaded as {file_path}")
                else:
                    print("Failed to download image")
    
        
        await ctx.defer()
        await avatar_getter_main()
        # authorcreated = str(ctx.author.)
        await ctx.send_followup(embed =embed)
        #await ctx.respond (embed =embed)
        #await ctx.respond(f"You are {author}. And your ID is {authorid} and {usercheck}. Pinging {ctx.author.mention} , hoping not pinging {author.mention}, then testing {for_me.mention} and {for_streep.mention}", embed=embed)

        # def check(reaction, user):
        #     return user == message.author and str(reaction.emoji) == '👍'

        # try:
        #     reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        # except asyncio.TimeoutError:
        #     await channel.send('👎')
        # else:
        #     await channel.send('👍')

    @bot.slash_command( description = "Shows all of the cardarts for a god.", 
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    @discord.option(
    "godname", 
    description="Enter the God's name",
    required=True
    )

    async def cardarts(ctx, godname: str):
        global guild_list
        ctx.guild_ids = guild_list
        #startbutton = Button(label="Start", style=discord.ButtonStyle.green, emoji="⛳")
        nextbutton = Button(label="Next", style=discord.ButtonStyle.green, emoji="<:next_page:1255262063950041189>")
        prevbutton = Button(label="Prev", style=discord.ButtonStyle.green, emoji="<:prev_page:1254976225223381055>")
        fuzzy_godname = None
        special_border_dict = {
            "golden" : (255,215,0),
            "legendary" : (0,0,0),
            "diamond" : (17,107,250)
        }

        async def card_art_main():
            skin_id_list, skin_name_list, skin_URL_list, god_id_list, rarity_list, favor_cost_list, gem_cost_list, godIcon, cardart_list_len = await card_art_query(godname=fuzzy_godname)
            #cardart_list, skin_name_list = SmiteDataAPI.findingGodCardArts(godname=godname)
            if cardart_list_len == 0:
                await ctx.response.send_message("There were no results for your query.", ephemeral=True)
                return
            #godIcon = SmiteDataAPI.findingGodURL(godname=godname)
            # cardart_list_len = len(cardart_list)
            
            #embedbutton = Button(label="Embed", style=discord.ButtonStyle.green, emoji="💵")
            j = 0
            embed = discord.Embed(title=f"{skin_name_list[0].upper()}", description=f"> {fuzzy_godname}\n>\tUse _/cardarts_", color=discord.Colour.from_rgb(25,150,25))
            embed.set_thumbnail(url=f"{godIcon}")
            embed.set_image(url=f"{skin_URL_list[0]}")
            embed.set_author(name="Smite", icon_url="https://static.wikia.nocookie.net/smite_gamepedia/images/b/b7/SmiteTime.png/revision/latest?cb=20170926124921")
            embed.set_footer(text=f"{j+1}/{cardart_list_len}\t\t\t\t\tID: {god_id_list[0]}")

            embed.add_field(name="Favor", value=f"{':lock:' if not favor_cost_list[0] else f'{favor_cost_list[0]} <:favor_icon:1252128762829475911>'}", inline=True)
            embed.add_field(name="Gems", value=f"{':lock:' if not gem_cost_list[0] else f'{gem_cost_list[0]} <:gems_icon:1252128683498410077>'}", inline=True)
            #embed.add_field(name="\u200B", value='\u200B')
            embed.add_field(name="Skin No.", value=f"{skin_id_list[0]}", inline=False)
            embed.add_field(name="Rarity", value=f"{rarity_list[0]}", inline=True)
        
            view = View(prevbutton, nextbutton)

            def next_skin():
                nonlocal j
                j = j + 1
                if j >= cardart_list_len:
                    j = j % cardart_list_len
                print("we have called next")
            def prev_skin():
                nonlocal j
                j = j - 1
                if j < 0:
                    j = cardart_list_len - 1
                print("we have called prev")

            async def prevbutton_callback(interaction):

                view = View(prevbutton, nextbutton)
                await interaction.response.defer()
                prev_skin()
                embed.set_field_at(index=0, name="Favor",value=f"{':lock:' if not favor_cost_list[j] else f'{favor_cost_list[j]} <:favor_icon:1252128762829475911>'} ", inline=True)
                embed.set_field_at(index=1, name="Gems",value=f"{':lock:' if not gem_cost_list[j] else f'{gem_cost_list[j]} <:gems_icon:1252128683498410077>'} ", inline=True)
                embed.set_field_at(index=2, name="Skin No.", value=f"{skin_id_list[j]}", inline=False)
                embed.set_field_at(index=3, name="Rarity", value=f"{rarity_list[j]}", inline=True)
                embed.set_image(url=f"{f'{skin_URL_list[j]}' if skin_URL_list[j] else f'{skin_URL_list[0]}'}")
                embed.set_footer(text=f"{j+1}/{cardart_list_len}\t\t\t\t\tID: {god_id_list[j]}")
                embed.title = f"{skin_name_list[j].upper()}"
                redTUPLE,greenTUPLE,blueTUPLE = special_border_dict.get(skin_name_list[j].lower(), (25,150,25))
                embed.color = embed.color.from_rgb(redTUPLE,greenTUPLE,blueTUPLE)
                # if str(skin_name_list[j].lower()) == "legendary":
                #     embed.color= embed.color.from_rgb(250,149,17)
                # elif str(skin_name_list[j].lower()) == "legendary":
                #     embed.color= embed.color.from_rgb(250,149,17)
                # elif str(skin_name_list[j].lower()) == "diamond":
                #     embed.color = embed.color.from_rgb(17,107,250)
                # else:
                #    embed.color = embed.color.from_rgb(25,150,25) 
                await interaction.edit_original_response(view=view, embed=embed)

            async def nextbutton_callback(interaction):

                view = View(prevbutton, nextbutton)
                await interaction.response.defer()
                next_skin()
                embed.set_field_at(index=0, name="Favor",value=f"{':lock:' if not favor_cost_list[j] else f'{favor_cost_list[j]} <:favor_icon:1252128762829475911>'} ", inline=True)
                embed.set_field_at(index=1, name="Gems",value=f"{':lock:' if not gem_cost_list[j] else f'{gem_cost_list[j]} <:gems_icon:1252128683498410077>'} ", inline=True)
                embed.set_field_at(index=2, name="Skin No.", value=f"{skin_id_list[j]}", inline=False)
                embed.set_field_at(index=3, name="Rarity", value=f"{rarity_list[j]}", inline=True)
                embed.set_image(url=f"{f'{skin_URL_list[j]}' if skin_URL_list[j] else f'{skin_URL_list[0]}'}")
                embed.set_footer(text=f"{j+1}/{cardart_list_len}\t\t\t\t\tID: {god_id_list[j]}")
                embed.title = f"{skin_name_list[j].upper()}"
                redTUPLE,greenTUPLE,blueTUPLE = special_border_dict.get(skin_name_list[j].lower(), (25,150,25))
                embed.color = embed.color.from_rgb(redTUPLE,greenTUPLE,blueTUPLE)
                # if skin_name_list[j].lower() == "legendary":
                #     embed.color.from_rgb(250,149,17)
                # elif skin_name_list[j].lower() == "diamond":
                #     embed.color.from_rgb(17,107,250)
                await interaction.edit_original_response(view=view, embed=embed)
            # async def prevbutton_callback(interaction):

            #     view = View(nextbutton, prevbutton)
            #     await interaction.response.defer()
            #     next_skin()
            #     embed.set_image(url=f"{cardart_list[j]}")
            #     embed.set_footer(text=f"{j+1}/{cardart_list_len}")
            #     embed.description = f"> {skin_name_list[j]}"
            #     await interaction.edit_original_response(view=view, embed=embed)
            #     #await interaction.edit_original_response(content = f"{cardart_list[j]} We are on skin #{j} after pressing **next!**", view=view, embed=embed)
            #     #next_skin()
                    
            #     # if next(cardart_iterate, -1) == -1:
            #     #     view = View()
            #     #     await interaction.edit_original_response(content = f"BROKE", view=view)
            #     # else:
            #     #     await interaction.edit_original_response(content = f"{next(cardart_iterate)}", view=view)
            #     #await interaction.followup.send(content = next(cardart_iterate), view=view)
            # async def nextbutton_callback(interaction):

            #     view = View(nextbutton, prevbutton)
            #     await interaction.response.defer()
            #     prev_skin()
            #     embed.set_image(url=f"{cardart_list[j]}")
            #     embed.set_footer(text=f"{j+1}/{cardart_list_len}")
            #     embed.description = f"> {skin_name_list[j]}"
            #     await interaction.edit_original_response(view=view, embed=embed)
            #     #await interaction.edit_original_response(content = f"{cardart_list[j]} We are on skin #{j} after pressing **prev!**", view=view)
            #     #prev_skin()

            # async def startbutton_callback(interaction):
            #     view = View(nextbutton, prevbutton)
            #     await interaction.response.defer()
            #     await interaction.edit_original_response(content = f"{cardart_list[0]}", view=view)

            prevbutton.callback = prevbutton_callback
            nextbutton.callback = nextbutton_callback
            #startbutton.callback = startbutton_callback
            #embedbutton.callback = embed_callback
            
            await ctx.respond(view=view, embed=embed)
    
    #All 3 possible outcomes for the queried input (Max of 3 fuzz results)
        async def godselect1_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.defer()
            nonlocal fuzzy_godname
            #print(fuzzy_godname)
            fuzzy_godname = fuzzy_godname_list[0]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content = f"{fuzzy_godname}", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_godname.title()} Selected!", view=view)
            await card_art_main()
        async def godselect2_callback(interaction):
            view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            #await interaction.response.defer()
            nonlocal fuzzy_godname
            #print(fuzzy_godname)
            fuzzy_godname = fuzzy_godname_list[1]
            #await interaction.response.defer()
            await interaction.response.edit_message(content = f"{fuzzy_godname.title()} Selected!", view=view)
            
            await card_art_main()
        async def godselect3_callback(interaction):
            view = View()
            #await interaction.response.defer()
            nonlocal fuzzy_godname
            fuzzy_godname = fuzzy_godname_list[2]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content ="hello3", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_godname.title()} Selected!", view=view)
            await card_art_main()

        #Processes which state name someone tries to input
        if godname:
            fuzzy_godname_list = await fuzzygodnames.fuzzysearch(str(godname))
            if len(fuzzy_godname_list) == 1:
                fuzzy_godname = fuzzy_godname_list[0]
                await card_art_main()
            elif len(fuzzy_godname_list) == 2:
                name1 = Button(label=f"{fuzzy_godname_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_godname_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                view = View(name1, name2, timeout=30.0)
                name1.callback = godselect1_callback
                name2.callback = godselect2_callback
                await ctx.response.send_message("Which God were you refering to? (30s)", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
            elif len(fuzzy_godname_list) == 3:
                name1 = Button(label=f"{fuzzy_godname_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_godname_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                name3 = Button(label=f"{fuzzy_godname_list[2]}", style=discord.ButtonStyle.green, emoji="🥉")
                view = View(name1, name2, name3)
                name1.callback = godselect1_callback
                name2.callback = godselect2_callback
                name3.callback = godselect3_callback
                #await ctx.respond(data)
                await ctx.response.send_message("Which God were you refering to?", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
        else:
            fuzzy_godname_list = await fuzzygodnames.fuzzysearch(str(godname))
            await card_art_main()
        ###################
        #Take input, fuzzy search
        #optional confirmation if multiple top matches
        #take result, send it to "state_name=" parameter
        ###################































    @bot.slash_command(name = "stateupdate", description = "Updates DB on the quarters that you have")
    @discord.option(
    "statename", 
    description="Enter the state name",
    required=True
    )
    # @discord.option(
    # "mintyear", 
    # description="Enter year the quarter was minted",
    # required=False,
    # default=None
    # )
    @discord.option(
    "dmint", 
    description="Denver mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    @discord.option(
    "pmint", 
    description="Philadelphia mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    async def quarter_update(ctx, statename: str, dmint: int, pmint: int):
        if (dmint is None) and (pmint is None):
            #await ctx.respond("Need to tell me which mint to update :^)")
            await ctx.response.send_message("Update failed. No mint specified.", ephemeral=True)
            return
        async def stateupdate_main():
            success = state_quarter_update(state_name=fuzzy_statename, D_mint=dmint, P_mint=pmint)
            if success:
                if (dmint is not None) and (pmint is not None):
                    await ctx.respond(f":white_check_mark: {fuzzy_statename}'s Denver mint has been set to {dmint}, and the Philadelphia has been set to {pmint}.", ephemeral=True)
                elif (dmint is not None):
                    await ctx.respond(f":white_check_mark: {fuzzy_statename}'s Denver mint has been set to {dmint}.", ephemeral=True)
                else:
                    await ctx.respond(f":white_check_mark: {fuzzy_statename}'s Philadelphia mint has been set to {pmint}.", ephemeral=True)
            else:
                await ctx.response.send_message("<:x:>", ephemeral=True) 
                
        #All 3 possible outcomes for the queried input (Max of 3 fuzz results)
        async def stateselect1_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[0]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content = f"{fuzzy_statename}", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            await stateupdate_main()
        async def stateselect2_callback(interaction):
            view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[1]
            #await interaction.response.defer()
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            
            await stateupdate_main()
        async def stateselect3_callback(interaction):
            view = View()
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            fuzzy_statename = fuzzy_statename_list[2]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content ="hello3", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            await stateupdate_main()

        #Processes which state name someone tries to input
        if statename:
            fuzzy_statename_list = fuzzyquarters.fuzzysearch(str(statename))
            if len(fuzzy_statename_list) == 1:
                fuzzy_statename = fuzzy_statename_list[0]
                await stateupdate_main()
            elif len(fuzzy_statename_list) == 2:
                name1 = Button(label=f"{fuzzy_statename_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                view = View(name1, name2, timeout=30.0)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                await ctx.response.send_message("Which State were you refering to? (30s)", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
            elif len(fuzzy_statename_list) == 3:
                name1 = Button(label=f"{fuzzy_statename_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                name3 = Button(label=f"{fuzzy_statename_list[2]}", style=discord.ButtonStyle.green, emoji="🥉")
                view = View(name1, name2, name3)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                name3.callback = stateselect3_callback
                #await ctx.respond(data)
                await ctx.response.send_message("Which State were you refering to?", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
        else:
            fuzzy_statename = statename
            await stateupdate_main()

    @bot.slash_command(name = "statequery", description = "Shows current DB on the quarters that you have")
    @discord.option(
    "statename", 
    description="Enter the state name",
    required=False,
    default=None
    )
    @discord.option(
    "mintyear", 
    description="Enter year the quarter was minted",
    required=False,
    default=None
    )
    @discord.option(
    "dmint", 
    description="Denver mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    @discord.option(
    "pmint", 
    description="Philadelphia mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    async def statequarter_query(ctx, statename: str, mintyear: int, dmint: int, pmint: int):
        prevbutton = Button(label="Prev", style=discord.ButtonStyle.green, emoji="👈")
        nextbutton = Button(label="Next", style=discord.ButtonStyle.green, emoji="👉")
        fuzzy_statename = None

        #The Main function, had to throw it in an async so it didn't automatically run
        async def dumbtest():
            Q_statenamelist, mintyearlist, linklist, p_mintlist, d_mintlist, max_len= await state_quarter_query(state_name=fuzzy_statename, mint_year=mintyear, P_mint=pmint, D_mint=dmint)
            if max_len == 0:
                await ctx.response.send_message("There were no results for your query.", ephemeral=True)
                return
            j = 0
            #embed = discord.Embed(title=f"{Q_statenamelist[0].upper()}", description=f"> Denver {':ballot_box_with_check:' if d_mintlist[0] else ':lock:'} \n> Philly{':ballot_box_with_check:' if p_mintlist[0] else ':lock:'}", color=discord.Colour.red())
            embed = discord.Embed(title=f"\t__QUARTERS__", description=f"> {Q_statenamelist[0].title()}", color=discord.Colour.dark_orange())
            #embed.set_thumbnail(url=f"{linklist[0]}")
            embed.set_image(url=f"{linklist[0]}")
            embed.set_footer(text=f"{j+1}/{max_len}")

            embed.add_field(name="Denver Mint", value=f"{':ballot_box_with_check:' if d_mintlist[0] else ':lock:'}", inline=True)
            embed.add_field(name="Philadelphia Mint", value=f"{':ballot_box_with_check:' if p_mintlist[0] else ':lock:'}", inline=True)
            #embed.add_field(name="\u200B", value='\u200B')
            embed.add_field(name="Mint Year", value=f"{mintyearlist[0]}", inline=False)
            view = View(prevbutton, nextbutton)

            def next_quarter():
                nonlocal j
                j = j + 1
                if j >= max_len:
                    j = j % max_len
                print("we have called next")
            def prev_quarter():
                nonlocal j
                j = j - 1
                if j < 0:
                    j = max_len - 1
                print("we have called prev")

            async def prevbutton_callback(interaction):

                view = View(prevbutton, nextbutton)
                await interaction.response.defer()
                prev_quarter()
                embed.set_field_at(index=0, name="Denver Mint",value=f"{':ballot_box_with_check:' if d_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=1, name="Philadelphia Mint",value=f"{':ballot_box_with_check:' if p_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=2, name="Mint Year", value=f"{mintyearlist[j]}", inline=False)
                embed.set_image(url=f"{linklist[j]}")
                embed.set_footer(text=f"{j+1}/{max_len}")
                embed.description =f"> {Q_statenamelist[j].title()}"
                await interaction.edit_original_response(view=view, embed=embed)

            async def nextbutton_callback(interaction):

                view = View(prevbutton, nextbutton)
                await interaction.response.defer()
                next_quarter()
                embed.set_field_at(index=0, name="Denver Mint",value=f"{':ballot_box_with_check:' if d_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=1, name="Philadelphia Mint",value=f"{':ballot_box_with_check:' if p_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=2, name="Mint Year", value=f"{mintyearlist[j]}", inline=False)
                embed.set_image(url=f"{linklist[j]}")
                embed.set_footer(text=f"{j+1}/{max_len}")
                embed.description =f"> {Q_statenamelist[j].title()}"
                await interaction.edit_original_response(view=view, embed=embed)

            prevbutton.callback = prevbutton_callback
            nextbutton.callback = nextbutton_callback
            
            await ctx.respond(view=view, embed=embed)




        #All 3 possible outcomes for the queried input (Max of 3 fuzz results)
        async def stateselect1_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[0]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content = f"{fuzzy_statename}", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            await dumbtest()
        async def stateselect2_callback(interaction):
            view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[1]
            #await interaction.response.defer()
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            
            await dumbtest()
        async def stateselect3_callback(interaction):
            view = View()
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            fuzzy_statename = fuzzy_statename_list[2]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content ="hello3", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            await dumbtest()

        #Processes which state name someone tries to input
        if statename:
            fuzzy_statename_list = fuzzyquarters.fuzzysearch(str(statename))
            if len(fuzzy_statename_list) == 1:
                fuzzy_statename = fuzzy_statename_list[0]
                await dumbtest()
            elif len(fuzzy_statename_list) == 2:
                name1 = Button(label=f"{fuzzy_statename_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                view = View(name1, name2, timeout=30.0)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                await ctx.response.send_message("Which State were you refering to? (30s)", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
            elif len(fuzzy_statename_list) == 3:
                name1 = Button(label=f"{fuzzy_statename_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                name3 = Button(label=f"{fuzzy_statename_list[2]}", style=discord.ButtonStyle.green, emoji="🥉")
                view = View(name1, name2, name3)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                name3.callback = stateselect3_callback
                #await ctx.respond(data)
                await ctx.response.send_message("Which State were you refering to?", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
        else:
            fuzzy_statename = statename
            await dumbtest()
        ###################
        #Take input, fuzzy search
        #optional confirmation if multiple top matches
        #take result, send it to "state_name=" parameter
        ###################
        
        

    @bot.slash_command(name = "parkupdate", description = "Updates DB on the quarters that you have")
    @discord.option(
    "statename", 
    description="Enter the state name",
    required=True
    )
    # @discord.option(
    # "mintyear", 
    # description="Enter year the quarter was minted",
    # required=False,
    # default=None
    # )
    @discord.option(
    "dmint", 
    description="Denver mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    @discord.option(
    "pmint", 
    description="Philadelphia mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    async def parkquarter_update(ctx, statename: str, dmint: int, pmint: int):
        # if (dmint is None) and (pmint is None):
        #     await ctx.respond("Need to tell me which mint to update :^)")
        # else:
        #     success = park_quarter_update(state_name=statename, D_mint=dmint, P_mint=pmint)
        #     if success:
        #         await ctx.respond(":white_check_mark:")
        #     else:
        #         await ctx.respond("<:x:>") 


        if (dmint is None) and (pmint is None):
            #await ctx.respond("Need to tell me which mint to update :^)")
            await ctx.response.send_message("Update failed. No mint specified.", ephemeral=True)
            return
        if (dmint is not None) and (dmint not in [0, 1]):
            await ctx.response.send_message("Update failed. Improper input for Denver mint. [Use: 0|1 for un|collected]", ephemeral=True)
            return
        if (pmint is not None) and (pmint not in [0, 1]):
            await ctx.response.send_message("Update failed. Improper input for Philadelphia mint. [Use: 0|1 for un|collected]", ephemeral=True)
            return
        async def parkupdate_main():
            success = park_quarter_update(state_name=fuzzy_statename, D_mint=dmint, P_mint=pmint)
            if success:
                if (dmint is not None) and (pmint is not None):
                    await ctx.respond(f":white_check_mark: {fuzzy_statename}'s Denver mint has been set to {dmint}, and the Philadelphia has been set to {pmint}.", ephemeral=True)
                elif (dmint is not None):
                    await ctx.respond(f":white_check_mark: {fuzzy_statename}'s Denver mint has been set to {dmint}.", ephemeral=True)
                else:
                    await ctx.respond(f":white_check_mark: {fuzzy_statename}'s Philadelphia mint has been set to {pmint}.", ephemeral=True)
            else:
                await ctx.response.send_message("<:x:>", ephemeral=True) 
                
        #All 3 possible outcomes for the queried input (Max of 3 fuzz results)
        async def stateselect1_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[0].title()
            #await interaction.response.defer()
            #await interaction.edit_original_response(content = f"{fuzzy_statename}", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename} Selected!", view=view)
            await parkupdate_main()
        async def stateselect2_callback(interaction):
            view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[1].title()
            #await interaction.response.defer()
            await interaction.response.edit_message(content = f"{fuzzy_statename} Selected!", view=view)
            
            await parkupdate_main()
        async def stateselect3_callback(interaction):
            view = View()
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            fuzzy_statename = fuzzy_statename_list[2].title()
            #await interaction.response.defer()
            #await interaction.edit_original_response(content ="hello3", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename} Selected!", view=view)
            await parkupdate_main()

        #Processes which state name someone tries to input
        if statename:
            fuzzy_statename_list = fuzzyquarters.fuzzysearch(str(statename))
            if len(fuzzy_statename_list) == 1:
                fuzzy_statename = fuzzy_statename_list[0].title()
                await parkupdate_main()
            elif len(fuzzy_statename_list) == 2:
                name1 = Button(label=f"{fuzzy_statename_list[0].title()}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1].title()}", style=discord.ButtonStyle.green, emoji="🥈")
                view = View(name1, name2, timeout=30.0)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                await ctx.response.send_message("Which State were you refering to? (30s)", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
            elif len(fuzzy_statename_list) == 3:
                name1 = Button(label=f"{fuzzy_statename_list[0].title()}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1].title()}", style=discord.ButtonStyle.green, emoji="🥈")
                name3 = Button(label=f"{fuzzy_statename_list[2].title()}", style=discord.ButtonStyle.green, emoji="🥉")
                view = View(name1, name2, name3)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                name3.callback = stateselect3_callback
                #await ctx.respond(data)
                await ctx.response.send_message("Which State were you refering to?", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
        else:
            fuzzy_statename = statename
            await parkupdate_main()










    @bot.slash_command(name = "parkquery", description = "Shows current DB on the quarters that you have")
    @discord.option(
    "statename", 
    description="Enter the state name",
    required=False,
    default=None
    )
    @discord.option(
    "statefeature", 
    description="Enter the state's feature name",
    required=False,
    default=None
    )
    @discord.option(
    "mintyear", 
    description="Enter year the quarter was minted",
    required=False,
    default=None
    )
    @discord.option(
    "dmint", 
    description="Denver mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    @discord.option(
    "pmint", 
    description="Philadelphia mint, 0|1 for un|collected",
    required=False,
    default=None
    )
    async def parkquarter_query(ctx, statename: str, statefeature: str, mintyear: int, dmint: int, pmint: int):


        prevbutton = Button(label="Prev", style=discord.ButtonStyle.green, emoji="👈")
        nextbutton = Button(label="Next", style=discord.ButtonStyle.green, emoji="👉")
        fuzzy_statename = None

        #The Main function, had to throw it in an async so it didn't automatically run
        async def parkdumbtest():
            #Q_statenamelist, mintyearlist, linklist, p_mintlist, d_mintlist, max_len= await state_quarter_query(state_name=fuzzy_statename, mint_year=mintyear, P_mint=pmint, D_mint=dmint)
            Q_statenamelist, statefeaturelist, mintyearlist, linklist, p_mintlist, d_mintlist, max_len = await park_quarter_query(state_name=fuzzy_statename, mint_year=mintyear, P_mint=pmint, D_mint=dmint)
            if max_len == 0:
                await ctx.response.send_message("There were no results for your query.", ephemeral=True)
                return
            j = 0
            #embed = discord.Embed(title=f"{Q_statenamelist[0].upper()}", description=f"> Denver {':ballot_box_with_check:' if d_mintlist[0] else ':lock:'} \n> Philly{':ballot_box_with_check:' if p_mintlist[0] else ':lock:'}", color=discord.Colour.red())
            embed = discord.Embed(title=f"\t__QUARTERS__", description=f"> {statefeaturelist[0].title()}, {Q_statenamelist[0].title()}", color=discord.Colour.dark_red())
            #embed = discord.Embed(title=f"\t__QUARTERS__", description=f"> {Q_statenamelist[0].title()}", color=discord.Colour.dark_orange())
            #embed.set_thumbnail(url=f"{linklist[0]}")
            embed.set_image(url=f"{linklist[0]}")
            embed.set_footer(text=f"{j+1}/{max_len}")

            embed.add_field(name="Denver Mint", value=f"{':ballot_box_with_check:' if d_mintlist[0] else ':lock:'}", inline=True)
            embed.add_field(name="Philadelphia Mint", value=f"{':ballot_box_with_check:' if p_mintlist[0] else ':lock:'}", inline=True)
            #embed.add_field(name="\u200B", value='\u200B')
            embed.add_field(name="Mint Year", value=f"{mintyearlist[0]}", inline=False)
            view = View(prevbutton, nextbutton)

            def next_quarter():
                nonlocal j
                j = j + 1
                if j >= max_len:
                    j = j % max_len
                print("we have called next")
            def prev_quarter():
                nonlocal j
                j = j - 1
                if j < 0:
                    j = max_len - 1
                print("we have called prev")

            async def prevbutton_callback(interaction):

                view = View(prevbutton, nextbutton)
                await interaction.response.defer()
                prev_quarter()
                embed.set_field_at(index=0, name="Denver Mint",value=f"{':ballot_box_with_check:' if d_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=1, name="Philadelphia Mint",value=f"{':ballot_box_with_check:' if p_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=2, name="Mint Year", value=f"{mintyearlist[j]}", inline=False)
                embed.set_image(url=f"{linklist[j]}")
                embed.set_footer(text=f"{j+1}/{max_len}")
                embed.description =f"> {statefeaturelist[j].title()}, {Q_statenamelist[j].title()}"
                #embed.description =f"> {Q_statenamelist[j].title()}"
                await interaction.edit_original_response(view=view, embed=embed)

            async def nextbutton_callback(interaction):

                view = View(prevbutton, nextbutton)
                await interaction.response.defer()
                next_quarter()
                embed.set_field_at(index=0, name="Denver Mint",value=f"{':ballot_box_with_check:' if d_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=1, name="Philadelphia Mint",value=f"{':ballot_box_with_check:' if p_mintlist[j] else ':lock:'}", inline=True)
                embed.set_field_at(index=2, name="Mint Year", value=f"{mintyearlist[j]}", inline=False)
                embed.set_image(url=f"{linklist[j]}")
                embed.set_footer(text=f"{j+1}/{max_len}")
                embed.description =f"> {statefeaturelist[j].title()}, {Q_statenamelist[j].title()}"
                #embed.description =f"> {Q_statenamelist[j].title()}"
                await interaction.edit_original_response(view=view, embed=embed)

            prevbutton.callback = prevbutton_callback
            nextbutton.callback = nextbutton_callback
            
            await ctx.respond(view=view, embed=embed)




        #All 3 possible outcomes for the queried input (Max of 3 fuzz results)
        async def stateselect1_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[0]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content = f"{fuzzy_statename}", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            await parkdumbtest()
        async def stateselect2_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            #print(fuzzy_statename)
            fuzzy_statename = fuzzy_statename_list[1]
            #await interaction.response.defer()
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            
            await parkdumbtest()
        async def stateselect3_callback(interaction):
            view = View(timeout=30.0)
            #await interaction.response.defer()
            nonlocal fuzzy_statename
            fuzzy_statename = fuzzy_statename_list[2]
            #await interaction.response.defer()
            #await interaction.edit_original_response(content ="hello3", view=view)
            await interaction.response.edit_message(content = f"{fuzzy_statename.title()} Selected!", view=view)
            await parkdumbtest()

        #Processes which state name someone tries to input
        if statename:
            fuzzy_statename_list = fuzzyquarters.fuzzysearch(str(statename))
            if len(fuzzy_statename_list) == 1:
                fuzzy_statename = fuzzy_statename_list[0]
                await parkdumbtest()
            elif len(fuzzy_statename_list) == 2:
                name1 = Button(label=f"{fuzzy_statename_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                view = View(name1, name2, timeout=30.0)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                await ctx.response.send_message("Which State were you refering to? (30s)", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
            elif len(fuzzy_statename_list) == 3:
                name1 = Button(label=f"{fuzzy_statename_list[0]}", style=discord.ButtonStyle.green, emoji="🥇")
                name2 = Button(label=f"{fuzzy_statename_list[1]}", style=discord.ButtonStyle.green, emoji="🥈")
                name3 = Button(label=f"{fuzzy_statename_list[2]}", style=discord.ButtonStyle.green, emoji="🥉")
                view = View(name1, name2, name3)
                name1.callback = stateselect1_callback
                name2.callback = stateselect2_callback
                name3.callback = stateselect3_callback
                #await ctx.respond(data)
                await ctx.response.send_message("Which State were you refering to?", ephemeral=True, view=view)
                #await ctx.respond("Which State were you refering to?", view=view)
        else:
            fuzzy_statename = statename
            await parkdumbtest()








        # prevbutton = Button(label="Prev", style=discord.ButtonStyle.green, emoji="👈")
        # nextbutton = Button(label="Next", style=discord.ButtonStyle.green, emoji="👉")
        # Q_statenamelist, statefeaturelist, mintyearlist, linklist, p_mintlist, d_mintlist, max_len = park_quarter_query(state_name=statename, mint_year=mintyear, P_mint=pmint, D_mint=dmint)
        # j = 0
        # #embed = discord.Embed(title=f"{Q_statenamelist[0].upper()}", description=f"> Denver {':ballot_box_with_check:' if d_mintlist[0] else ':lock:'} \n> Philly{':ballot_box_with_check:' if p_mintlist[0] else ':lock:'}", color=discord.Colour.red())
        # embed = discord.Embed(title=f"\t__QUARTERS__", description=f"> {statefeaturelist[0].upper()}, {Q_statenamelist[0]}", color=discord.Colour.dark_red())
        # #embed.set_thumbnail(url=f"{linklist[0]}")
        # embed.set_image(url=f"{linklist[0]}")
        # embed.set_footer(text=f"{j+1}/{max_len}")

        # embed.add_field(name="Denver Mint", value=f"{':ballot_box_with_check:' if d_mintlist[0] else ':lock:'}", inline=True)
        # embed.add_field(name="Philadelphia Mint", value=f"{':ballot_box_with_check:' if p_mintlist[0] else ':lock:'}", inline=True)
        # #embed.add_field(name="\u200B", value='\u200B')
        # embed.add_field(name="Mint Year", value=f"{mintyearlist[0]}", inline=False)
        # view = View(prevbutton, nextbutton)

        # def next_quarter():
        #     nonlocal j
        #     j = j + 1
        #     if j >= max_len:
        #         j = j % max_len
        #     print("we have called next")
        # def prev_quarter():
        #     nonlocal j
        #     j = j - 1
        #     if j < 0:
        #         j = max_len - 1
        #     print("we have called prev")

        # async def prevbutton_callback(interaction):

        #     view = View(prevbutton, nextbutton)
        #     await interaction.response.defer()
        #     prev_quarter()
        #     embed.set_field_at(index=0, name="Denver Mint",value=f"{':ballot_box_with_check:' if d_mintlist[j] else ':lock:'}", inline=True)
        #     embed.set_field_at(index=1, name="Philadelphia Mint",value=f"{':ballot_box_with_check:' if p_mintlist[j] else ':lock:'}", inline=True)
        #     embed.set_field_at(index=2, name="Mint Year", value=f"{mintyearlist[j]}", inline=False)
        #     embed.set_image(url=f"{linklist[j]}")
        #     embed.set_footer(text=f"{j+1}/{max_len}")
        #     embed.description =f"> {statefeaturelist[j].upper()}, {Q_statenamelist[j]}"
        #     await interaction.edit_original_response(view=view, embed=embed)


            

        # async def nextbutton_callback(interaction):

        #     view = View(prevbutton, nextbutton)
        #     await interaction.response.defer()
        #     next_quarter()
        #     embed.set_field_at(index=0, name="Denver Mint",value=f"{':ballot_box_with_check:' if d_mintlist[j] else ':lock:'}", inline=True)
        #     embed.set_field_at(index=1, name="Philadelphia Mint",value=f"{':ballot_box_with_check:' if p_mintlist[j] else ':lock:'}", inline=True)
        #     embed.set_field_at(index=2, name="Mint Year", value=f"{mintyearlist[j]}", inline=False)
        #     embed.set_image(url=f"{linklist[j]}")
        #     embed.set_footer(text=f"{j+1}/{max_len}")
        #     embed.description =f"> {statefeaturelist[j].upper()}, {Q_statenamelist[j]}"
        #     await interaction.edit_original_response(view=view, embed=embed)

        # prevbutton.callback = prevbutton_callback
        # nextbutton.callback = nextbutton_callback
        
        # await ctx.respond(view=view, embed=embed)
    @bot.slash_command(name = "dressupgame", description = "testing")
    async def dressup_test(ctx):
        embed = discord.Embed(title=f"\t__DRESS UP GAME TEST__", description=f"> Testing for Dress Up Game", color=discord.Colour.dark_red())
        
        file_link, max_hairlen, max_shirtlen, max_pantslen = await image_gen(need_max=True)
        file = discord.File(file_link, filename="image.png")
        embed.set_image(url="attachment://image.png")

        hair = 0
        shirt = 0
        pants = 0
        Prev_button_hair = Button(label=f"Prev Hair", style=discord.ButtonStyle.green, emoji="🎩", row=0)
        Prev_button_shirt = Button(label=f"Prev Shirt", style=discord.ButtonStyle.green, emoji="👕", row=1)
        Prev_button_pants = Button(label=f"Prev Pants", style=discord.ButtonStyle.green, emoji="👖", row=2)

        Colorhair_button = Button (label = f"Hair Color", style=discord.ButtonStyle.blurple, emoji="🎨", row = 0)
        Colorshirt_button = Button (label = f"Shirt Color", style=discord.ButtonStyle.blurple, emoji="🎨", row = 1)
        Colorpants_button = Button (label = f"Pants Color", style=discord.ButtonStyle.blurple, emoji="🎨", row = 2)

        Next_button_hair = Button(label=f"Next Hair", style=discord.ButtonStyle.green, emoji="🎩", row=0)
        Next_button_shirt = Button(label=f"Next Shirt", style=discord.ButtonStyle.green, emoji="👕", row=1)
        Next_button_pants = Button(label=f"Next Pants", style=discord.ButtonStyle.green, emoji="👖", row=2)
        
        #await ctx.respond(file=discord.File(file_link))

        def next_hair():
                nonlocal hair
                hair = hair + 1
                if hair >= max_hairlen:
                    hair = hair % max_hairlen
                #print(f"we have called next hair : {hair}")
        def prev_hair():
                nonlocal hair
                hair = hair - 1
                if hair < 0:
                    hair = max_hairlen - 1
               #print("we have called prev")

        def next_shirt():
                nonlocal shirt
                shirt = shirt + 1
                if shirt >= max_shirtlen:
                    shirt = shirt % max_shirtlen
                #print(f"we have called next shirt : {shirt}")
        def prev_shirt():
                nonlocal shirt
                shirt = shirt - 1
                if shirt < 0:
                    shirt = max_shirtlen - 1
               #print("we have called prev")

        def next_pants():
                nonlocal pants
                pants = pants + 1
                if pants >= max_pantslen:
                    pants = pants % max_pantslen
                #print(f"we have called next pants : {pants}")
        def prev_pants():
                nonlocal pants
                pants = pants - 1
                if pants < 0:
                    pants = max_pantslen - 1
               #print("we have called prev")


        async def prevbutton_hair_callback(interaction):
            #view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            nonlocal hair, shirt, pants
            prev_hair()
            file_link_edit = await image_gen(hair_current=hair, shirt_current=shirt, pants_current=pants)
            file = discord.File(file_link_edit, filename="image.png")
            embed.set_image(url="attachment://image.png")
            #await interaction.response.defer()
            await interaction.response.edit_message(file= file, embed=embed, view=view)

        async def nextbutton_hair_callback(interaction):
            #view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            nonlocal hair, shirt, pants
            next_hair()
            file_link_edit = await image_gen(hair_current=hair, shirt_current=shirt, pants_current=pants)
            file = discord.File(file_link_edit, filename="image.png")
            embed.set_image(url="attachment://image.png")
            #await interaction.response.defer()
            await interaction.response.edit_message(file= file, embed=embed, view=view)
        
        async def prevbutton_shirt_callback(interaction):
            #view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            nonlocal hair, shirt, pants
            prev_shirt()
            file_link_edit = await image_gen(hair_current=hair, shirt_current=shirt, pants_current=pants)
            file = discord.File(file_link_edit, filename="image.png")
            embed.set_image(url="attachment://image.png")
            #await interaction.response.defer()
            await interaction.response.edit_message(file= file, embed=embed, view=view)

        async def nextbutton_shirt_callback(interaction):
            #view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            nonlocal hair, shirt, pants
            next_shirt()
            file_link_edit = await image_gen(hair_current=hair, shirt_current=shirt, pants_current=pants)
            file = discord.File(file_link_edit, filename="image.png")
            embed.set_image(url="attachment://image.png")
            #await interaction.response.defer()
            await interaction.response.edit_message(file= file, embed=embed, view=view)

        async def prevbutton_pants_callback(interaction):
            #view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            nonlocal hair, shirt, pants
            prev_pants()
            file_link_edit = await image_gen(hair_current=hair, shirt_current=shirt, pants_current=pants)
            file = discord.File(file_link_edit, filename="image.png")
            embed.set_image(url="attachment://image.png")
            #await interaction.response.defer()
            await interaction.response.edit_message(file= file, embed=embed, view=view)

        async def nextbutton_pants_callback(interaction):
            #view = View(timeout=10.0)
            #await interaction.response.send_message("1", ephemeral=True, view=view)
            nonlocal hair, shirt, pants
            next_pants()
            file_link_edit = await image_gen(hair_current=hair, shirt_current=shirt, pants_current=pants)
            file = discord.File(file_link_edit, filename="image.png")
            embed.set_image(url="attachment://image.png")
            #await interaction.response.defer()
            await interaction.response.edit_message(file= file, embed=embed, view=view)

        Prev_button_hair.callback = prevbutton_hair_callback
        Prev_button_shirt.callback = prevbutton_shirt_callback
        Prev_button_pants.callback = prevbutton_pants_callback

        Next_button_hair.callback = nextbutton_hair_callback
        Next_button_shirt.callback = nextbutton_shirt_callback
        Next_button_pants.callback = nextbutton_pants_callback
        view = View(Prev_button_hair,Prev_button_shirt,Prev_button_pants,Colorhair_button,Colorshirt_button,Colorpants_button,Next_button_hair,Next_button_shirt, Next_button_pants)
        await ctx.respond(file=file, embed=embed, view=view)
        # buttons_list = []
        # for i in range (3):
        #     Next_button = Button(label=f"Next{i}", style=discord.ButtonStyle.green, emoji="🤜", row = i)
        #     ColorChange_button = Button (label = f"Change{i}", style=discord.ButtonStyle.blurple, emoji="🎨", row = i)
        #     Prev_button = Button(label=f"Prev{i}", style=discord.ButtonStyle.green, emoji="🤛", row=i)

        #     buttons_list.append(
        #         {
        #             'next' : Next_button,
        #             'color' : ColorChange_button,
        #             'prev' : Prev_button
        #         }
        #     )
        # async def stateselect1_callback(interaction):
        # view = View(name1, name2, timeout=30.0)
        # name1.callback = stateselect1_callback
        # name2.callback = stateselect2_callback
    # async def get_animal_types(ctx: discord.AutocompleteContext):
    #     """
    #     Here we will check if 'ctx.options['animal_type']' is a marine or land animal and return respective option choices
    #     """
    #     animal_type = ctx.options['animal_type']
    #     if animal_type == 'Marine':
    #         return ['Whale', 'Shark', 'Fish', 'Octopus', 'Turtle']
    #     else: # is land animal
    #         return ['Snake', 'Wolf', 'Lizard', 'Lion', 'Bird']

    # @bot.slash_command(name="animal")
    # async def animal_command(
    # ctx: discord.ApplicationContext,
    # animal_type: discord.Option(str, choices=['Marine', 'Land']),
    # animal: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_animal_types))):
    #     await ctx.respond(f'You picked an animal type of `{animal_type}` that led you to pick `{animal}`!')

    # @bot.slash_command(name = "rolling", description = "testing")
    # async def rolling(interaction: discord.Interaction,
    #                   item: str):
    #     await interaction.response.send_message(f"{item}", ephemeral=True)
    # @rolling.autocomplete("item")
    # async def mudae_autocompletion(
    #         interaction: discord.Interation,
    #         current: str
    # ):
    #     data = []
    #     for roll_choice in ['wa', 'wx', 'wg', 'mx']:
    #         if current.lower() in roll_choice.lower():
    #             data.append(application_command.Choice(name=roll_choice, value=roll_choice))
    #         return data
    # @discord.OptionChoice(
    # name ="type", 
    # # description="Which one to roll",
    # # required=True,
    
    # value=["wa","wx","wg"]
    # )
    # @discord.option(
    # "rolls", 
    # description="How many to roll",
    # required=True,
    
    # choices=[10,15,20]
    # )
    
    # @bot.slash_command(name = "autoroll", description = "testing")
    # async def autoroll(ctx, type:str, rolls:int):
    #     await ctx.respond(f"Your results show {rolls} rolls for {type}")

    number_rolls_choices = ['5', '10', '20', '40']  # list of breed types to autocomplete   
    roll_type_choices=["wa","wx","wg"]
    here_or_togo = ['Main', 'Kek']

    rolling = discord.Option(str, autocomplete=discord.utils.basic_autocomplete(number_rolls_choices),
                            required=True)  # create options using autocomplete util
    type_of_roll = discord.Option(str, autocomplete=discord.utils.basic_autocomplete(roll_type_choices),
                            required=True)  # create options using autocomplete util
    yay_or_nay = discord.Option(str, autocomplete=discord.utils.basic_autocomplete(here_or_togo),
                            required=True)  # create options using autocomplete util
    @bot.slash_command(name = "autoroll", description = "Rolling for mudae")
    async def autoroll(ctx, numrolls: rolling, gatchatype :type_of_roll, server: yay_or_nay ): # type: ignore
        await ctx.respond(f"🎩 Rolling {gatchatype} {numrolls} times in the {server} server.")
        if server == 'Main':
            mainserver = True
        else:
            mainserver = False
        numrolls_int = int(numrolls)
        completed = await Auto_Roller(type_roll=gatchatype, number_rolls=numrolls_int, main_server=mainserver)
        if completed:
            await ctx.respond(f"Done rolling")
        else:
            await ctx.respond(f"something went wrong :(")




    class MyView1(discord.ui.View):
        @discord.ui.select( # the decorator that lets you specify the properties of the select menu
            placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
            min_values = 1, # the minimum number of values that must be selected by the users
            max_values = 2, # the maximum number of values that can be selected by the users
            options = [ # the list of options from which users can choose, a required field
                discord.SelectOption(
                    label="Vanilla",
                    value = "1",
                    description="Pick this if you like vanilla!"
                ),
                discord.SelectOption(
                    label="Chocolate",
                    value = "2",
                    description="Pick this if you like chocolate!"
                ),
                discord.SelectOption(
                    label="Strawberry",
                    value = "3",
                    description="Pick this if you like strawberry!"
                )
            ]
        )
        async def select_callback(self, select: discord.ui.Select, interaction): # the function called when the user is done selecting options
            if select.values[0] == "1":
                select.append_option(discord.SelectOption(
                    label="Sprinkles",
                    value = "1",
                    description="Pick this if you like Sprinkles!"
                ))
                
            await interaction.response.send_message(f"Awesome! I like {', '.join([val for val in select.values])} too!")

    @bot.command()
    async def flavor(ctx):
        await ctx.respond("Choose a flavor!", view=MyView1())




    @bot.slash_command(guild_ids = [173641386686414849], name = "matchinfo", description = "Gives winrates of matches using certain params")
    @discord.option(
    "region", 
    description="Enter: 'NA', 'EU','NA-W' or 'Unkn' ",
    required=False,
    default=None
    )
    @discord.option(
    "duration", 
    description="Enter # of mins; Neg# for less than [<], Pos# for Greater than [>]",
    required=False,
    default=0
    )
    @discord.option(
    "surrender", 
    description="Enter '0' for no surrenders, enter '1' for only surrenders",
    required=False,
    default=None
    )
    @discord.option(
    "orderwin", 
    description="Enter '1' for Order side wins, enter '2' for Chaos side wins",
    required=False,
    default=None
    )
    async def matchinfo(ctx, region: str, duration: int, surrender: int, orderwin: int):
        query_num, query_total = databasematches(region=region, surrender=surrender, duration=(duration*60), order_side_win=orderwin)
        await ctx.respond(f"Your results show {query_num} out of {query_total} recorded matches; or {((query_num/query_total)*100):.2f}%")


    #CHATGPT Helped
    class DynamicView(discord.ui.View):
        def __init__(self, options, placeholder, min_values=1, max_values=1, disabled=False, duplicate_check_list = None, result_values_list = None, query_time = 1):
            super().__init__()
            self.query_time = query_time
            self.duplicate_check_list = duplicate_check_list or []
            self.result_values_list = result_values_list or []
            self.select_menu = discord.ui.Select(
                placeholder=placeholder,
                min_values=min_values,
                max_values=max_values,
                disabled=disabled,
                options=options
            )
            self.select_menu.callback = self.select_callback
            self.add_item(self.select_menu)
        
        async def select_callback(self, interaction: discord.Interaction):


            """This is written as:
                dictionary[keyword][options][min/max]

                dictionary = {
                    option : [ [option labels], [min_val int, max_val int] ]
                }
            """

            options_dict = {
                "region" : [
                    [
                    discord.SelectOption(label="NA", value="NA", description="North America"),
                    discord.SelectOption(label="EU", value="EU", description="Europe"),
                    discord.SelectOption(label="NA-West", value="NA-W", description="North America-West"),
                    discord.SelectOption(label="Misc", value="Unkn", description="Other regions")
                    ], 
                    [1, 1]
                ],
                "surrender" : [
                    [
                    discord.SelectOption(label="Surrendered", value="1", description="Filtered for ONLY surrenders"),
                    discord.SelectOption(label="Not Surrendered", value="0", description="Filtered for ONLY no surrenders")
                    ],
                    [1, 1]
                ],
                "duration_length_greater_than" : [
                    [
                    discord.SelectOption(label="5", value="5", description="Longer than 5 mins"),
                    discord.SelectOption(label="10", value="10", description="Longer than 10 mins"),
                    discord.SelectOption(label="15", value="15", description="Longer than 15 mins"),
                    discord.SelectOption(label="20", value="20", description="Longer than 20 mins"),
                    discord.SelectOption(label="25", value="25", description="Longer than 25 mins"),
                    discord.SelectOption(label="30", value="30", description="Longer than 30 mins"),
                    discord.SelectOption(label="35", value="35", description="Longer than 35 mins"),
                    discord.SelectOption(label="40", value="40", description="Longer than 40 mins"),
                    discord.SelectOption(label="45", value="45", description="Longer than 45 mins"),
                    discord.SelectOption(label="50", value="50", description="Longer than 50 mins")
                    ], 
                    [1, 1]
                ],
                "duration_length_less_than" : [
                    [
                    discord.SelectOption(label="10", value="10", description="Shorter than 10 mins"),
                    discord.SelectOption(label="15", value="15", description="Shorter than 15 mins"),
                    discord.SelectOption(label="20", value="20", description="Shorter than 20 mins"),
                    discord.SelectOption(label="25", value="25", description="Shorter than 25 mins"),
                    discord.SelectOption(label="30", value="30", description="Shorter than 30 mins"),
                    discord.SelectOption(label="35", value="35", description="Shorter than 35 mins"),
                    discord.SelectOption(label="40", value="40", description="Shorter than 40 mins"),
                    discord.SelectOption(label="45", value="45", description="Shorter than 45 mins"),
                    discord.SelectOption(label="50", value="50", description="Shorter than 50 mins"),
                    discord.SelectOption(label="55", value="55", description="Shorter than 55 mins")
                    ], 
                    [1, 1]
                ],
                "OrderChaos" : [
                    [
                    discord.SelectOption(label="Order", value="1", description="For ONLY Order wins [1st ban/pick - Higher avg. MMR]"),
                    discord.SelectOption(label="Chaos", value="2", description="For ONLY Chaos wins [Last ban/pick - Lower avg. MMR]")
                    ],
                    [1, 1]
                ],
                #Main Page
                "options" : [
                    [
                    discord.SelectOption(label="Region", value="region", description="Select this to filter by region."),
                    discord.SelectOption(label="Surrender", value="surrender", description="Select this to filter by surrenders."),
                    discord.SelectOption(label="MatchTime (>)", value="duration_length_greater_than", description="Select this to filter by match length (longer than 'x')."),
                    discord.SelectOption(label="MatchTime (<)", value="duration_length_less_than", description="Select this to filter by match length (shorter than 'x')."),
                    #discord.SelectOption(label="Order/Chaos", value="OrderChaos", description="Select this to filter by Order/Chaos wins."),
                    discord.SelectOption(label="Order/Chaos", value="OrderChaos", description="Select this to filter by Order/Chaos wins."),
                    discord.SelectOption(label="Done", value="specify", description="Select this to get results.")
                    ], 
                    [1, 1]
                ],
                "limit_to": [
                    [
                    discord.SelectOption(label="From Same Region", value="query_now_same", description="Limits overall matches to same region as selected."),
                    discord.SelectOption(label="From All Regions", value="query_now", description="Does not limit overall matches to a specific region")
                    ], 
                    [1, 1]
                ],
                "limit_to_no_choice": [
                    [
                    discord.SelectOption(label="From All Regions", value="query_now", description="Does not limit overall matches to a specific region")
                    ], 
                    [1, 1]
                ],
                
                "duplicate": [
                    [
                    discord.SelectOption(label="Go Back", value="options", description="You've already selected this, click here to go back.")
                    ], 
                    [1, 1]
                ],
                
                

            }
            value = self.select_menu.values[0]

            dupe_list = self.duplicate_check_list
            result_list = self.result_values_list
            
            # if value == "region":
                
            #     new_view = DynamicView(options_dict[value][0], f"Choose a {value} to filter by", min_values=options_dict[value][1][0], max_values=options_dict[value][1][1]) #Shows the message on the clickable bar
            #     await interaction.response.edit_message(content=f"Filtering by {value}...", view=new_view)
            # elif value == "surrender":
            #     new_view = DynamicView(options_dict[value][0], f"Choose a {value} to filter by", options_dict[value][1][0], options_dict[value][1][1]) #Shows the message on the clickable bar
            #     await interaction.response.edit_message(content=f"Filtering by {value}...", view=new_view)
            # elif value == "duration_length_less_than":
            #     new_view = DynamicView(options_dict[value][0], f"Choose a {value} to filter by", options_dict[value][1][0], options_dict[value][1][1]) #Shows the message on the clickable bar
            #     await interaction.response.edit_message(content=f"Filtering by {value}...", view=new_view)
            # elif value == "OrderChaos":
            #     new_view = DynamicView(options_dict[value][0], f"Choose a {value} to filter by", options_dict[value][1][0], options_dict[value][1][1]) #Shows the message on the clickable bar
            #     await interaction.response.edit_message(content=f"Filtering by {value}...", view=new_view)
            # else:
            #     await interaction.response.send_message(f"Awesome! You chose {', '.join([val for val in self.select_menu.values])}!", ephemeral=True)

            

            if value in options_dict:

                if value in dupe_list:
                    print("test 1")
                    new_view = DynamicView(options_dict["duplicate"][0], f"Choose a new option to filter by", options_dict[value][1][0], options_dict[value][1][1],duplicate_check_list=dupe_list, result_values_list=result_list) #Shows the message on the clickable bar
                    await interaction.response.edit_message(content=f"Go Back.", view=new_view)

                elif (value == "options"):
                    print("test 2")
                    new_view = DynamicView(options_dict[value][0], f"Choose a new option to filter by", options_dict["duplicate"][1][0], options_dict["duplicate"][1][1],duplicate_check_list=dupe_list, result_values_list=result_list) #Shows the message on the clickable bar
                    await interaction.response.edit_message(content=f"Filtering by Options...", view=new_view)
                

                else:
                    print("test 3")
                    dupe_list.append(value)
                    new_view = DynamicView(options_dict[value][0], f"Choose a {value} to filter by", options_dict[value][1][0], options_dict[value][1][1],duplicate_check_list=dupe_list, result_values_list=result_list) #Shows the message on the clickable bar
                    await interaction.response.edit_message(content=f"Filtering by {value}: Current dupe list {', '.join([results for results in dupe_list])}...", view=new_view)
            else:
                

                if (value == "query_now") or (value == "query_now_same"):
                    print("test 4")
                    same = ""
                    zipped_filter_lists = zip(self.duplicate_check_list,self.result_values_list)
                    zipped_filter_lists2 = zip(self.duplicate_check_list,self.result_values_list)
                    Final_Query_Text = []
                    emoji_dictionary = {
                        "NA-W" : "<:NA_West:1253468293902368848>",
                        "NA" : ":flag_us:",
                        "EU" : ":flag_eu:",
                        "UNKN" : ":grey_question:",
                        "1" : "<:order_fountain:1253468294476861573>", #Order
                        "2": "<:chaos_fountain:1253468291041591459>", #Chaos
                        0: "<:F7_icon:1253468292807524554>", #Not Surrendered
                        1: "<:F6_icon:1253468291901554770>"  #Surrendered
                        
                    }
                    embed = discord.Embed(title=f"Daily Match Stats", description=f"> Using the _/daily_stats_matches_ command", color=discord.Colour.from_rgb(25,150,25))
                    embed.add_field(name="", value="", inline=False)
                    embed.add_field(name="", value="", inline=True)
                    embed.add_field(name="__Current Filters__", value="", inline=True)
                    embed.add_field(name="", value="", inline=True)
                    embed.add_field(name="", value="", inline=False)

                    for zip_tuple in zipped_filter_lists:

                        match zip_tuple:
                            case ("region", result):
                                Final_Query_Text.append(f"Region = {result.upper()}")
                                if value == "query_now_same":
                                    same = str(result)
                                embed.add_field(name="Region", value=f"{emoji_dictionary[result.upper()]}", inline=True)
                            case ("surrender", result):
                                Final_Query_Text.append(f"Surrenders Only = {'True' if int(result) else 'False'}")
                                embed.add_field(name="Surrender", value=f"{emoji_dictionary[int(result)]}", inline=True)
                            case ("duration_length_greater_than", result):
                                Final_Query_Text.append(f"Match Time > {result} Minutes")
                                embed.add_field(name="Match Duration (>)", value=f"[Match Time > {result} Minutes]", inline=True)
                            case ("duration_length_less_than", result):
                                Final_Query_Text.append(f"Match Time < {result} Minutes")
                                embed.add_field(name="Match Duration (<)", value=f"[Match Time < {result} Minutes]", inline=True)
                            case ("OrderChaos", result):
                                Final_Query_Text.append(f"Order/Chaos = {'Order' if result == '1' else 'Chaos'}")
                                embed.add_field(name="Order/Chaos", value=f"{emoji_dictionary[result]}", inline=True)
                            case _:
                                print(f"We got to a broken case, where the current tuple is: {zip_tuple}")

                        
                    # daily, weekly, monthly, special = None, None, None, None

                    # if self.query_time is None:
                    #     _, _, month, day = get_previous_day_month_name(days_ago=1)
                    #     yesterdayday = f'{month} {day}'
                    #     daily = 1 
                    # elif self.query_time == 'Weekly':
                    #     _, _, month, day = get_previous_day_month_name(days_ago=1)
                    #     _, _, month_start, day_start = get_previous_day_month_name(days_ago=7)
                    #     yesterdayday = f'{month_start} {day_start} --> {month} {day}'
                    #     weekly = 1
                    # elif self.query_time == 'Monthly':
                    #     _, _, month, day = get_previous_day_month_name(days_ago=1)
                    #     _, _, month_start, day_start = get_previous_day_month_name(days_ago=30)
                    #     yesterdayday = f'{month_start} {day_start} --> {month} {day}'
                    #     monthly = 1
                    # elif self.query_time == "Me":
                    #     _, _, month, day = get_previous_day_month_name(days_ago=3)
                    #     _, _, month_start, day_start = get_previous_day_month_name(days_ago=10)
                    #     yesterdayday = f'{month_start} {day_start} --> {month} {day}'
                    #     special = 1

                    embed.add_field(name="", value="", inline=False)
                    new_view = DynamicView(disabled=True, options=options_dict['options'][0], placeholder=f"Filtering by {', '.join([val for val in Final_Query_Text])}. Query now starting!")
                    #await interaction.response.edit_message(content=f"Filtering by {value}...", view=new_view)
                    #await interaction.response.send_message(f"Awesome! You chose {', '.join([val for val in self.select_menu.values])}, query beginning!", ephemeral=True, view=new_view)
                    print(f"before: {same}")
                    query_num, total_matches = await databasematches(ziplist=zipped_filter_lists2, same_region=same)
                    print(f"after: {same}")

                    
                    embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/smite_gamepedia/images/b/b7/SmiteTime.png/revision/latest?cb=20170926124921")
                    # embed.set_image(url=f"{skin_URL_list[0]}")
                    #embed.set_author(name="SMITE", icon_url="https://static.wikia.nocookie.net/smite_gamepedia/images/9/9f/Ward_Lightning.png/revision/latest?cb=20140611103051")
                    
                    
                    embed.set_footer(text=f"Smite by Hirez", icon_url="https://webcdn.hirezstudios.com/smite/v3/img/smite-logo.png")
                    #embed.set_footer(text=f"Based on completed games in Ranked Conquest\t\t\t\t\tDATE: {yesterdayday}")

                    # embed.add_field(name="Favor", value=f"{':lock:' if not favor_cost_list[0] else f'{favor_cost_list[0]} <:favor_icon:1252128762829475911>'}", inline=True)
                    # embed.add_field(name="Gems", value=f"{':lock:' if not gem_cost_list[0] else f'{gem_cost_list[0]} <:gems_icon:1252128683498410077>'}", inline=True)
                    # #embed.add_field(name="\u200B", value='\u200B')
                    # embed.add_field(name="Skin No.", value=f"{skin_id_list[0]}", inline=False)
                    # embed.add_field(name="Rarity", value=f"{rarity_list[0]}", inline=True)




                    end_view = View()


                    
                    embed.add_field(name="Query Results", value=(f"\nYour results show **{query_num}** out of **{total_matches}** recorded matches with your filters.\n\nThis is **{((query_num/total_matches)*100):.2f}%** {f'of games in {same}.' if same else 'of all games.'}"), inline=False)
                    await interaction.response.edit_message(content= f"Loading...", view=end_view)
                    # msg = await interaction.respond(f"Loading...", view=new_view)
                    await asyncio.sleep(1)
                    await interaction.edit( content= None,embed=embed, view=end_view)
                    # msg = await interaction.response.edit_message(content= f"Loading...", view=end_view)
                    # await asyncio.sleep(1)
                    # await msg.response.edit_message( content= None,embed=embed, view=end_view)

                elif value == "specify":
                    print("test 4.5")
                    if "region" in self.duplicate_check_list:
                        new_view = DynamicView(options_dict['limit_to'][0], f"Choose a new option to filter by", options_dict["limit_to"][1][0], options_dict["limit_to"][1][1],duplicate_check_list=dupe_list, result_values_list=result_list)
                        await interaction.response.edit_message(content=f"Continue.", view=new_view)
                    else:
                        new_view = DynamicView(options_dict['limit_to_no_choice'][0], f"Choose a new option to filter by", options_dict["limit_to_no_choice"][1][0], options_dict["limit_to_no_choice"][1][1],duplicate_check_list=dupe_list, result_values_list=result_list)
                        await interaction.response.edit_message(content=f"Continue.", view=new_view)

                    
                else:
                    print("test 5")
                    result_list.append(value)
                    new_view = DynamicView(options_dict['options'][0], f"Choose an option to filter by", options_dict['options'][1][0], options_dict['options'][1][1],duplicate_check_list=dupe_list, result_values_list=result_list) #Shows the message on the clickable bar
                    await interaction.response.edit_message(content=f"Filtering by Options...", view=new_view)


    @bot.slash_command(description = "Gives statistics of daily matches using certain filters",
                 integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    #async def daily_stats_matches(ctx, prev_days: prev_winrate_selection): # type: ignore
    async def daily_stats_matches(ctx):

        #if 
        options = [
            discord.SelectOption(label="Region", value="region", description="Select this to filter by region."),
            discord.SelectOption(label="Surrender", value="surrender", description="Select this to filter by surrenders."),
            discord.SelectOption(label="MatchTime (>)", value="duration_length_greater_than", description="Select this to filter by match length (longer than 'x')."),
            discord.SelectOption(label="MatchTime (<)", value="duration_length_less_than", description="Select this to filter by match length (shorter than 'x')."),
            discord.SelectOption(label="Order/Chaos", value="OrderChaos", description="Select this to filter by Order/Chaos wins."),
            discord.SelectOption(label="Done", value="query_now", description="Select this to get results.")
        ]
        view = DynamicView(options, "Select your filters, then press done.") #Shows the message on the clickable bar
        await ctx.respond("Click this button", view=view)




    gacha_roll_num_types = [1, 5, 10]  # num of times to roll  
    gacha_rolls = discord.Option(int, autocomplete=discord.utils.basic_autocomplete(gacha_roll_num_types),
                            required=True,description=f"Select the # of pulls you want to do")
    hidden_pull_options = ["On", "Only 5*'s"]  # num of times to roll 
    hidden_pull_gacha = discord.Option(str, autocomplete=discord.utils.basic_autocomplete(hidden_pull_options),
                            required=False,description=f"Buttons don't show pull rarities beforehand")

    @bot.event
    async def on_application_command_error (ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(error, ephemeral=True)
        else: 
            raise error
        
    @bot.slash_command( description = "ROLL THE GACHA, GAIN AN ADDICTION", 
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    # @discord.option(
    # "rolls", 
    # description="Enter the God's name",
    # required=True
    # )
    # @discord.option(
    # "hidden_pulls", 
    # description="Buttons don't show pull rarities beforehand",
    # required=False
    #  )

    async def gacharoll(ctx, num_rolls: gacha_rolls, hidden_pulls: hidden_pull_gacha): # type: ignore
        # global guild_list
        # ctx.guild_ids = guild_list
        #authorid = int(ctx.author.id)
        username = ctx.author.name
        #startbutton = Button(label="Start", style=discord.ButtonStyle.green, emoji="⛳")
        
        caching = int(ctx.author.id)
        if caching not in user_id_cache:
            await users_gacha_insert(user_id=str(caching))
            #if not is_user:
                #insert_user_database(caching)
            user_id_cache.add(caching)
        else:
            print(f"Already cache'd")

        available_rolls, success = await users_gacha_rolls(user_id=str(caching),use_rolls=int(num_rolls))
        if not success:
            await ctx.response.send_message(f"Insufficient pack rolls. Current remaining rolls: {available_rolls}", ephemeral=True)

        embed = discord.Embed(title=f"You Pulled A", color=discord.Colour.from_rgb(25,0,25))
        #embed.set_image(url=f"{skin_URL_list[0]}")
        #await ctx.respond(f"You are {author}. And your ID is {authorid} and {usercheck}")
        # embed.add_field(name="Overall Win", value=f"{overall_wins}", inline=True)
        # embed.add_field(name="Overall Loss",value=f"{overall_losses}", inline=True)
        rarity_description_dict = {
            1 : "```ansi\n[2;32m[2;36m[2;32m[2;33m[2;30m[1;30m[Mortal][0m[2;30m[0m[2;33m[0m[2;32m[0m[2;36m[0m[2;32m[0m Rarity Card\n```",
            2 : "```ansi\n[2;37m[1;37m[Blessed][0m[2;37m[0m Rarity Card\n```",
            3 : "```ansi\n[2;37m[1;37m[1;33m[1;35m[1;33m[Demigod][0m[1;35m[0m[1;33m[0m[1;37m[0m[2;37m[0m Rarity Card\n```",
            4 : "```ansi\n[2;31m[2;36m[1;36m[Divine][0m[2;36m[0m[2;31m[0m Rarity Card\n```",
            5 : "```ansi\n[2;31m[1;31m[Titan][0m[2;31m[0m Rarity Card\n```",
            6 : "```ansi\n[2;37m[1;37m[1;33m[1;35m[1;33m[1;34m[1;34m[Celestial][0m[1;34m[0m[1;33m[0m[1;35m[0m[1;33m[0m[1;37m[0m[2;37m[0m Rarity Card\n```"
        }
        rarity_emoji_dict = {
            1 : "<:common_rarity:1256687795439669439>",
            2 : "<:common_rarity:1256687795439669439>",
            3 : "<:gold_rarity:1256687791644082298>",
            4 : "<:primal_rarity:1256687794017796147>",
            5 : "<:oni_rarity:1256687792369569883>",
            6 : "❓"
        }
        rarity_button_dict = {
            1 : discord.ButtonStyle.grey,
            2 : discord.ButtonStyle.grey,
            3 : discord.ButtonStyle.blurple,
            4 : discord.ButtonStyle.green,
            5 : discord.ButtonStyle.red,
            6 : discord.ButtonStyle.red

        }
        three_star_pity = 1
        rarity_rolls_list = []
        button_list = []
        for num in range(num_rolls):
            if (num == (num_rolls - 1)) and three_star_pity and (num_rolls == 10):
                print (f"pity hit")
                pity_roll = random.randint(1,200)
                match pity_roll:
                    case _ if pity_roll <= 184:
                        rarity_rolls_list.append(3)
                    case _ if pity_roll <= 195:
                        rarity_rolls_list.append(4)
                    case _ if pity_roll <= 200:
                        rarity_rolls_list.append(5)
            
            else:
                rand_rarity = random.randint(1,10000)
                match rand_rarity:
                    case 69:
                        rarity_rolls_list.append(6)
                        print(f"Someone rolled it, insane!")
                    case _ if rand_rarity <= 5500: #55%
                        rarity_rolls_list.append(1)
                    case _ if rand_rarity <= 8000: #25%
                        rarity_rolls_list.append(2)
                    case _ if rand_rarity <= 9200: #12%
                        rarity_rolls_list.append(3)
                        three_star_pity = 0
                    case _ if rand_rarity <= 9750: #5.5%
                        rarity_rolls_list.append(4)
                        three_star_pity = 0
                    case _:
                        rarity_rolls_list.append(5) #2.5%
                        three_star_pity = 0
        
        
            #rarity_rolls_list.append(rand_rarity)
        card_id_list, card_image_list = await gacha_query(real_rarity_list=rarity_rolls_list,user_id=str(caching))
        async def create_button_callback(roll_number, rarity):
            async def button_callback(interaction):
                # Your callback logic here, using roll_number
                embed.description= f"{rarity_description_dict[rarity]}"
                embed.set_image(url=f"{card_image_list[roll_number]}")
                embed.set_footer(text=f"Card no.{card_id_list[roll_number]}\t\t\t\tRemaining Rolls: {available_rolls}")
                await interaction.response.edit_message(content = None,view=view,embed=embed)
            return button_callback
        for roll in range(num_rolls):
            current_rarity_roll = rarity_rolls_list[roll]
            if not hidden_pulls:
                my_button = Button(style=rarity_button_dict[current_rarity_roll], emoji=f"{rarity_emoji_dict[current_rarity_roll]}")
            elif hidden_pulls == "On":
                my_button = Button(style=rarity_button_dict[1], emoji="❔")
            elif hidden_pulls == "Only 5*'s":
                my_button = Button(style=(rarity_button_dict[1] if ((current_rarity_roll == 5) or (current_rarity_roll == 6)) else rarity_button_dict[current_rarity_roll]), emoji=(f"{rarity_emoji_dict[1]}" if ((current_rarity_roll == 5) or (current_rarity_roll == 6)) else f"{rarity_emoji_dict[current_rarity_roll]}"))
            my_button.callback = await create_button_callback(roll, current_rarity_roll)
            button_list.append(my_button)
        # prevbutton = Button(label="Prev", style=discord.ButtonStyle.green, emoji="<:prev_page:1254976225223381055>")
        view = View(*button_list)

        await ctx.response.send_message(f"Here are your rolls, {username.title()}", view=view) #<@{caching}>


    breed_types = ['German Shepherd', 'Bulldog', 'etc', 'testers']  # list of breed types to autocomplete   
    dog_breeds = discord.Option(str, autocomplete=discord.utils.basic_autocomplete(breed_types),
                            required=False)  # create options using autocomplete util
    @bot.slash_command(name="dog", description="Random dog picture", )
    async def dog(ctx, breed: dog_breeds): # type: ignore
        
        await ctx.respond(breed)
    bot.run(TOKEN)

import json
pip install discord
from discord.ext import commands
import asyncio

TOKEN = "OTI4NzQxNTMxMTkwNDQ4MTk4.YddL9A.F6N_ArblXIub6KZDt-C6_lZsfTk"

intents=discord.Intents.default()
bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")

# comando help per i comandi dello staff
@bot.group(invoke_without_command=True, aliases=["staffhelp"])
async def shelp(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="Comandi e categorie disponibili (Staff)", description="Utilizza `?help <comando>` per avere piu' informazini su ciascun comando ;)", color=0xff8ff7)
    embed.add_field(name="Points management", value="`add`, `subtract`")
    embed.add_field(name="Matches management", value="`match`, `win`, `deletechannel`")
    await ctx.send(embed=embed)

@shelp.command(aliases=["m"])
async def match(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title=f"{bot.command_prefix}match", color=0xff8ff7)
    embed.add_field(name="Descrizione", value="Questo comando permette di creare un match tra due capitani. Viene automaticamente creato un canale testuale dove possono accedere solamente i capitani in cui potranno parlare senza intasare la chat principale.", inline=False)
    embed.add_field(name="Utilizzo", value=f"`{bot.command_prefix}match <@capitanoTeam1> <@capitanoTeam2> <team size> <game mode>`\n• Team size: grandezza del team, questo parametro deve essere un numero che indica da quanti membri e' formato ciascun team (in caso di 1v1 sara' 1, in caso di 2v2 sara' 2 ecc.)\n• Game mode: modalita' di gioco, questo parametro dovra' contenere la modalita' che si andra' a giocare: `real` per realistic, `box` per box fight, `zone` per zone wars e `build` per build fight. Le lettere possono essere sia maiuscole che minuscole (case insensitive) ma la parola deve essere corretta, non devono esserci ne' lettere in piu' ne' lettere in meno ecc.", inline=False)
    embed.add_field(name="Abbreviazioni", value=f"`{bot.command_prefix}m`", inline=False)
    await ctx.send(embed=embed)

@shelp.command()
async def deletechannel(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title=f"{bot.command_prefix}deletechannel", color=0xff8ff7)
    embed.add_field(name="Descrizione", value="Questo comando permette di eliminare un canale privato dalla categoria `matches`. L'azione viene anche registrata in un log preciso con autore del comando e canale eliminato in caso di problemi.", inline=False)
    embed.add_field(name="Utilizzo", value=f"`{bot.command_prefix}deletechannel`", inline=False)
    embed.add_field(name="Abbreviazioni", value="Non sono disponibili abbreviazioni per questo comando.", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='European Wager Cord', url='https://www.twitch.tv/gabrihi_fn'))

    print("Il bot è connesso")

# menzione del ruolo moderatore nel canale privato
@bot.event
async def on_reaction_add(reaction: discord.Reaction, user:discord.Member):
    if user.id != 928741531190448198:
        mod = discord.utils.get(user.guild.roles, name="Moderator")
        message = mod.mention
        channel = reaction.message.channel
        if channel.category.id == 928739130593136720:
            if reaction.emoji == "❓":
                await channel.send(f"{message} ({user.mention})")

# apertura dell'account
async def openAccount(user):
    users = await getData()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["name"] = user.name
        users[str(user.id)]["mention"] = user.mention
        users[str(user.id)]["id"] = str(user.id)

        users[str(user.id)]["points"] = 0
    with open("users.json", "w") as file:
        json.dump(users,file)
    return True

# prelevare i dati dall'account
async def getData():
    with open("users.json", "r") as file:
        users = json.load(file)
    return users

@bot.command(aliases=["m"])
async def match(ctx, t1_head: discord.Member, t2_head:discord.Member, team_size:int, game_mode:str, total_price:str):
    await ctx.message.delete()

    channel = bot.get_channel(855898039792042024)
    matches = discord.utils.get(ctx.guild.categories, name="matches")
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    mm = discord.utils.get(ctx.guild.roles, name="Middleman")
    admin = discord.utils.get(ctx.guild.roles, name="Admin")
    if mod in ctx.author.roles or mm in ctx.author.roles or admin in ctx.author.roles:
     if game_mode.lower() == "real":
        game_mode="Realistic"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0xff1332)
     elif game_mode.lower() == "box":
        game_mode="Box Fight"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0x04e654)
     elif game_mode.lower() == "zone":
        game_mode="Zone Wars"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0x00e0ff)
     elif game_mode.lower() == "build":
        game_mode="Build Fight"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0xffe5002)

    matches = discord.utils.get(ctx.guild.categories, name="matches")
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    mm = discord.utils.get(ctx.guild.roles, name="Middleman")
    admin = discord.utils.get(ctx.guild.roles, name="Admin")

    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    mm: discord.PermissionOverwrite(read_messages=True),
    admin: discord.PermissionOverwrite(read_messages=True),
    mod: discord.PermissionOverwrite(read_messages=True),
    t1_head: discord.PermissionOverwrite(read_messages=True),
    t2_head: discord.PermissionOverwrite(read_messages=True)
}
    private_channel = await ctx.guild.create_text_channel("{}-vs-{}".format(t1_head.display_name.strip(), t2_head.display_name.strip()), category=matches, overwrites=overwrites)

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/884124476411887717/934770564894175242/IMG_20220117_005129_612.jpg")  
    embed.add_field(name="Team 1 vs Team 2", value="{} vs {}".format(t1_head.mention, t2_head.mention), inline=False) 
    embed.set_footer(text="European Wager Cord | Invoked by {}".format(ctx.author))
    await channel.send(embed=embed)

    dm1 = await t1_head.create_dm()
    dm2 = await t2_head.create_dm()

    dm1_embed=discord.Embed(title=f"Match {team_size}vs{team_size} creato", color=0x2d80fa)
    dm1_embed.set_author(name=f"{bot.user.display_name}", icon_url=f"{bot.user.avatar_url}")
    dm1_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/884124476411887717/934770564894175242/IMG_20220117_005129_612.jpg")  
    dm1_embed.add_field(name="Avversario", value=f"{t2_head.mention}", inline=False)
    dm1_embed.add_field(name="Canale privato", value=f"Usa questo canale per comunicare con il tuo avversario: <#{private_channel.id}>", inline=False)
    dm1_embed.set_footer(text="European Wager Cord | Made with ❤ by Gabrihi", icon_url=f"{bot.user.avatar_url}")
    await dm1.send(embed=dm1_embed)

    dm2_embed=discord.Embed(title=f"Match {team_size}vs{team_size} creato", color=0x2d80fa)
    dm2_embed.set_author(name=f"{bot.user.display_name}", icon_url=f"{bot.user.avatar_url}")
    dm2_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/884124476411887717/934770564894175242/IMG_20220117_005129_612.jpg")  
    dm2_embed.add_field(name="Avversario", value=f"{t1_head.mention}", inline=False)
    dm2_embed.add_field(name="Canale privato", value=f"• Usa questo canale per comunicare con il tuo avversario: <#{private_channel.id}>", inline=False)
    dm2_embed.set_footer(text="European Wager Cord | Made with ❤ by Gabrihi", icon_url=f"{bot.user.avatar_url}")
    await dm2.send(embed=dm2_embed)

    private=discord.Embed(title=f"Match {team_size}vs{team_size}", color=0x2d80fa)
    private.set_author(name=f"{bot.user.display_name}", icon_url=f"{bot.user.avatar_url}")
    private.set_thumbnail(url="https://cdn.discordapp.com/attachments/884124476411887717/934770564894175242/IMG_20220117_005129_612.jpg")  
    private.add_field(name="Capitani", value=f"• Team 1: {t1_head.mention} \n• Team 2: {t2_head.mention}", inline=False)
    private.add_field(name="Regole", value="• Regolamento completo: <#878247198041722890>", inline=False)
    private.add_field(name="A cosa serve questa chat?", value="• Questa chat e' stata creata per evitare di intasare la chat principale delle wager. Vi preghiamo di utilizzare questa chat per comunicare tra di voi e/o comunicare con i middleman, grazie.",inline=False)
    private.add_field(name="Assistenza", value="• Se avete bisogno urgentemente dello staff, reagite con :question:",inline=False)
    private.set_footer(text="European Wager Cord | Made with ❤ by Gabrihi", icon_url=f"{bot.user.avatar_url}")

    private_message = await private_channel.send(embed=private)
    await private_channel.send(f"{t1_head.mention} {t2_head.mention}")
    await private_message.add_reaction(emoji="❓")

@bot.command(aliases=["db"])
async def double(ctx, t1_head: discord.Member, t2_head:discord.Member, team_size:int, game_mode:str, total_price:str):
    await ctx.message.delete()

    channel = bot.get_channel(855898039792042024)

    if game_mode.lower() == "real":
        game_mode="Realistic"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0xff1332)
    elif game_mode.lower() == "box":
        game_mode="Box Fight"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0x04e654)
    elif game_mode.lower() == "zone":
        game_mode="Zone Wars"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0x00e0ff)
    elif game_mode.lower() == "build":
        game_mode="Build Fight"
        embed=discord.Embed(title=f"Nuova wager {team_size}v{team_size} {game_mode} per €{total_price}", color=0xffe5002)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/884124476411887717/934770564894175242/IMG_20220117_005129_612.jpg")  
    embed.add_field(name="Team 1 vs Team 2", value="{} vs {}".format(t1_head.mention, t2_head.mention), inline=False) 
    embed.set_footer(text="European Wager Cord | Invoked by {}".format(ctx.author))
    await channel.send(embed=embed)

@bot.command()
async def deletechannel(ctx):
    await ctx.message.delete()
    channel = ctx.channel
    matches = discord.utils.get(ctx.guild.categories, name="matches")
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    mm = discord.utils.get(ctx.guild.roles, name="Middleman")
    admin = discord.utils.get(ctx.guild.roles, name="Admin")
    if mod in ctx.author.roles or mm in ctx.author.roles or admin in ctx.author.roles:
        if channel.category.id == matches.id:
            channel_logs = bot.get_channel(928757705739481088)
            entry = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
            embed=discord.Embed(title="Log rilevato", color=0xff1332)
            embed.add_field(name="Eliminazione di un canale", value="• Utente: {} \n• Canale eliminato: {}".format(ctx.author, channel.name))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/884124476411887717/934770564894175242/IMG_20220117_005129_612.jpg")  
            await channel_logs.send(embed=embed)
            await channel.delete()

@bot.command()
async def documentazione(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="Documentazione", color=0x000001)
    embed.add_field(name="Importante", value="Queste sono alcune cose importantissime che dovete tenere a mente per evitare che il bot smetta di andare: \n• **NON** modificate per nessun motivo i **nomi** dei seguenti ruoli: `Admin`, `Moderator`, `Middleman`,; \n• **NON** eliminate per nessun motivo il canale `#partite` e la categoria `Matches`; \n• **NON** espellete per nessun motivo il bot dal server (cosa scontata ma la metto comunque)")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/884124476411887717/934770564894175242/IMG_20220117_005129_612.jpg")  
    await ctx.send(embed=embed)

bot.run(TOKEN)

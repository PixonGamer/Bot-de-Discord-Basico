import discord
import asyncio
import sqlite3

from discord import app_commands, NotFound, Forbidden, HTTPException
from discord.ext import tasks
from typing import Optional
import random

#//////////////////////////////////#


token = '0' # Token del Bot
MY_GUILD = discord.Object(id=0) # ID de tu guild ("servidor")

class MyClient(discord.Client):
	def __init__(self, *, intents: discord.Intents):
		super().__init__(intents=intents)
		self.tree = app_commands.CommandTree(self)

	async def setup_hook(self):
		self.tree.copy_global_to(guild=MY_GUILD)
		await self.tree.sync(guild=MY_GUILD)        

		
intents = discord.Intents.default()
client = MyClient(intents=intents)
intents.members = True
intents.message_content = True

@client.event
async def on_ready():
	print('——————————————————————')
	print(f'Iniciado cómo: {client.user}')
	print(f'ID: {client.user.id}')
	print('——————————————————————')



@client.tree.command()
async def hola(interaction: discord.Interaction):
	"Dile hola al bot!"
	await interaction.response.send_message(f'¡Hola, {interaction.user.mention}!')

@client.tree.command()
@app_commands.describe(miembro='El miembro del que deseas obtener la información')
async def info_user(interaction: discord.Interaction, miembro: Optional[discord.Member] = None):
	'Obten información sobre un miembro'
	member = miembro or interaction.user
	member_roles = " , ".join(role.mention for role in member.roles if not role.is_default()).replace(',' , ' ')
	
	embed = discord.Embed(title=f' ', color = member.color, timestamp=interaction.created_at)
	embed.set_author(name=f'Información sobre {member}', icon_url= member.avatar)
	embed.set_thumbnail(url= member.avatar)
	embed.add_field(name=' ', value=' ', inline=False)

	embed.add_field(name='Se unió el', value=f'{discord.utils.format_dt(member.joined_at)}', inline=True)
	embed.add_field(name='Registrado el', value=f'{discord.utils.format_dt(member.created_at)}', inline=True)

	"""embed.add_field(name=' ', value=' ', inline=False)
  # Si quieres agregar campos que contengan el "Tag" y "color" del miembro, remueve los """ """
	embed.add_field(name='Tag', value=f'{member}', inline=True)
	embed.add_field(name='Color', value=f'{member.color}', inline=True)

	embed.add_field(name=' ', value=' ', inline=False)"""

	embed.add_field(name=f'Roles', value=f'{member_roles}', inline=False)
	embed.set_footer(text=f'ID: {member.id} ')

	await interaction.response.send_message(embed = embed)

"""/////////////////////////////////////////////////////////////////////////////// """
@client.tree.context_menu(name='Información')
async def info(interaction: discord.Interaction, member: discord.Member):
	member = member or interaction.user
	member_roles = " , ".join(role.mention for role in member.roles if not role.is_default()).replace(',' , ' ')
	
	embed = discord.Embed(title=f' ', color = member.color, timestamp=interaction.created_at)
	embed.set_author(name=f'Información sobre {member.name}', icon_url= member.avatar)
	embed.set_thumbnail(url= member.avatar)
	embed.add_field(name=' ', value=' ', inline=False)

	embed.add_field(name='Se unió el', value=f'{discord.utils.format_dt(member.joined_at)}', inline=True)
	embed.add_field(name='Registrado el', value=f'{discord.utils.format_dt(member.created_at)}', inline=True)

	"""embed.add_field(name=' ', value=' ', inline=False)

	embed.add_field(name='Tag', value=f'{member}', inline=True)
	embed.add_field(name='Color', value=f'{member.color}', inline=True)
  # Si quieres agregar campos que contengan el "Tag" y "color" del miembro, remueve los """ """
	embed.add_field(name=' ', value=' ', inline=False)"""

	embed.add_field(name=f'Roles', value=f'{member_roles}', inline=False)
	embed.set_footer(text=f'ID: {member.id}')

	await interaction.response.send_message(embed = embed)

#//////////////////////////////////////////////////////////////////////////////////////////////#

@client.tree.command()
async def info_server(interaction: discord.Interaction):
	"Muestra información sobre este servidor"
	guild = interaction.guild

	embed=discord.Embed(title = 'Información sobre este servidor', color = 0x29db47, timestamp = interaction.created_at)
	embed.set_author(name =f'{guild.name}',icon_url= guild.icon)
	embed.set_thumbnail(url= guild.icon)
	embed.add_field(name = 'Owner', value =f'<@{guild.owner_id}>', inline = True)
	embed.add_field(name = 'Categorias', value=f'{len(guild.categories)}', inline = True)	
	embed.add_field(name = ' ', value =' ', inline = True)			
	embed.add_field(name = 'Canales', value=f'{len(guild.channels)}', inline = True)	
	embed.add_field(name = 'Canales de Texto', value=f'{len(guild.text_channels)}', inline = True)	
	embed.add_field(name = 'Canales de Voz', value=f'{len(guild.voice_channels)}', inline = True)	
	embed.add_field(name = ' ', value =' ', inline = False)
	embed.add_field(name = 'Creado el', value=f'{discord.utils.format_dt(guild.created_at)}', inline = True)
	embed.add_field(name = 'Roles', value=f'{len(guild.roles)}', inline = True)
	embed.add_field(name = 'Miembros', value=f'{len(guild.members)	}', inline = True)			



	embed.set_footer(text =f'ID: {guild.id}')

	await interaction.response.send_message(embed = embed)

#////////////////////////////////////////////////////////////////////////////////////////#	

@client.tree.command()
async def roles(interaction: discord.Interaction):
	"Muestra una lista de los roles del servidor"

	roles = discord.Role
	guild = interaction.guild

	list_roles = [roles.mention for roles in guild.roles if not roles.is_default()]


	embed=discord.Embed(title =f'Roles [{len(guild.roles)}]', color = 0x29db47, timestamp = interaction.created_at)
	embed.set_author(name =f'{guild.name}', icon_url = guild.icon)
	embed.add_field(name = '', value ='\n'.join(list_roles[::-1]).replace(',',' '), inline = False)

	await interaction.response.send_message(embed = embed)

#///////////////////////////////////////////////////////////////////////////////////////#

@client.tree.command()
@app_commands.describe(rol='Rol del que deseas obtener información')
async def info_rol(interaction: discord.Interaction, rol: discord.Role):
	"Información sobre un rol"

	role = rol
	guild = interaction.guild
	key_permissions = ["administrator", "manage_guild", "manage_roles", "manage_channels", "manage_messages",
						"manage_webhooks", "manage_nicknames", "manage_emojis", "kick_members", "mention_everyone"]
	list_permissions = (Perm for Perm, value in role.permissions if value)
	filter_permissions = [i for i in list_permissions if i in key_permissions]


	embed=discord.Embed(color=role.color, timestamp = interaction.created_at)
	embed.set_author(name =f'{guild.name}',icon_url= guild.icon)	
	embed.set_thumbnail(url= guild.icon)	
	embed.add_field(name='Nombre', value=f'{role.name}', inline=True)
	embed.add_field(name='Color', value=f'{role.color}', inline=True)
	embed.add_field(name='Creado el', value=f'{discord.utils.format_dt(role.created_at)}', inline=True)	
		
	if role.icon != None:
		embed.add_field(name='Icono', value=f'{role.icon}', inline=True)
	elif role.unicode_emoji != None:		
		embed.add_field(name='Icono', value=f'{role.icon}', inline=True)
	else:
		embed.add_field(name='Icono', value=f'Ninguno', inline=True)	

	embed.add_field(name='Posición', value=f'{role.position}', inline=True)
	
	embed.add_field(name = ' ', value =' ', inline = True)		

	if role.hoist == True:
		embed.add_field(name='Separado', value=f'ㅤ✅', inline=True)
	else:
		embed.add_field(name='Separado', value=f'ㅤ❌', inline=True)

	if role.managed == True:
		embed.add_field(name='Gestionado', value=f'ㅤㅤ✅', inline=True)
	else:
		embed.add_field(name='Gestionado', value=f'ㅤㅤ❌', inline=True)	

	if role.mentionable == True:
		embed.add_field(name='Mencionable', value='ㅤㅤ✅', inline=True)
	else:
		embed.add_field(name='Mencionable', value='ㅤㅤ❌', inline=True)								
					
	if len(filter_permissions) != 0:	
		embed.add_field(name='Permisos', value=f'{",  " .join(filter_permissions).title().replace("_"," ")}', inline=False)

	embed.set_footer(text =f'ID: {role.id}')
	

	await interaction.response.send_message(embed = embed)




@client.tree.command()
async def seguridad_cuenta(interaction: discord.Interaction):
	"Algunos consejos para la seguridad de tu cuenta en Discord"

	tips = ['**Activa la autenticación de dos factores (A2F)**, en dado caso que tu contraseña sea comprometida, aun tendrían que sobrepasar la A2F para acceder a tu cuenta.',
			'Algo muy básico: **usa tu sentido común.**',
			'¿Ingresaste a un servidor y te piden que escanees un código QR con la aplicación de Discord para "verificarte"? están tratando de ingresar a tu cuenta, ningún BOT te pedirá que escanees un código QR en Discord. https://dat.place/content/images/2022/07/image-34.png',
			'Revisa frecuentemente tus **Ajustes del Usuario** > **Dispositivos** y **Aplicaciones Autorizadas**',
			'Verifica si el bot de verficación tiene el simbolo de verificado, hay algunos "dueños" que crean un bot para hacerse pasar por otro (Dyno, Wick, etc)',
			'Discord o cualquier otra compañia nunca 1te contactará por medio de un MD en Discord, los mensajes de Discord Oficiales aparecerán en tu MD con la etíqueta de **"Sistema"**. https://dat.place/content/images/size/w1000/2022/07/image-3.png',
			'No existe Nitro Gratis.',
			'Para los Dueños de servidores: es muy recomendado utilizar bots Anti Raid y Anti Nuke cómo Wick, Beemo, etcétera.',
			'No descargues cosas de dudosa procedencia, al creador del bot le hackearon la cuenta de Discord por tener desactivado el 2FA y descargarse un .APK :(',
			'Un sitio recomendado que tiene más sugerencias para mejorar tu seguridad en Discord: https://dat.place/scams/',
			'Asegurate que el canal de registros del bot solamente sea visible para tí, el dueño.'
			'Evita utilizar/activar el permiso "Administrador" en Roles.']


	await interaction.response.send_message( random.choice(tips), ephemeral = True)	
	
@client.tree.command()
@app_commands.default_permissions(ban_members=True)
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(usuario='Usuario al que quieres banear')
@app_commands.describe(razon="Razón del baneo (Opcional)")
async def ban(interaction: discord.Interaction, usuario: discord.Member, razon: Optional[str]):
    """Manda de vacaciones a un usuario de tu Discord"""
    guild = interaction.guild

    try:
        if razon is not None:
            await guild.ban(usuario, reason=f'{razon} (Ejecutado por {interaction.user})')
        else:
            await guild.ban(usuario, reason=f'Sin razón especificada. (Ejecutado por {interaction.user})')
    except NotFound:
        await interaction.response.send_message("No se ha encontrado al miembro específicado.", ephemeral=True)
    except Forbidden:
        await interaction.response.send_message("No tengo los permisos necesarios para banear a este miembro.", ephemeral=True)
    except HTTPException:
        await interaction.response.send_message("Error HTTP desconocido.", ephemeral=True)

    if razon is not None:
        embed = discord.Embed(description=f"**{usuario}** ha sido baneado por el siguiente motivo: **{razon}**",color=0x2dc854, timestamp=interaction.created_at)
        embed.set_author(name=f'{guild.name}', icon_url=guild.icon)
        await interaction.response.send_message(f"Acabas de banear a **{usuario}** por el siguiente motivo: **{razon}**", ephemeral=True)
    else:
        embed = discord.Embed(description=f"**{usuario}** ha sido baneado.", color=0x2dc854, timestamp=interaction.created_at)
        embed.set_author(name=f'{guild.name}', icon_url=guild.icon)
        await interaction.response.send_message(f"Acabas de banear a **{usuario}** sin razón especificada.", ephemeral=True)

    await interaction.channel.send(embed=embed)
	
@client.tree.command()
@app_commands.default_permissions(kick_members=True)
@app_commands.checks.has_permissions(kick_members=True)
@app_commands.describe(usuario='Usuario al que quieres expulsar')
@app_commands.describe(razon="Razón de la expulsión (Opcional)")
async def kick(interaction: discord.Interaction, usuario: discord.Member, razon: Optional[str]):
    """Expulsa a un usuario de tu Discord"""
    guild = interaction.guild

    try:
        # color = member.color, timestamp = interaction.created_at)
        if razon is not None:
            await guild.kick(usuario, reason=f'{razon} (Ejecutado por {interaction.user})')
        else:
            await guild.kick(usuario, reason=f'Sin razón especificada. (Ejecutado por {interaction.user})')
    except NotFound:
        await interaction.response.send_message("No se ha encontrado al miembro específicado.", ephemeral=True)
    except Forbidden:
        await interaction.response.send_message("No tengo los permisos necesarios para expulsar a este miembro.", ephemeral=True)
    except HTTPException:
        await interaction.response.send_message("Error HTTP desconocido.", ephemeral=True)

    if razon is not None:
        embed = discord.Embed(description=f"**{usuario}** ha sido expulsado por el siguiente motivo: **{razon}**",color=0x2dc854, timestamp=interaction.created_at)
        embed.set_author(name=f'{guild.name}', icon_url=guild.icon)
        await interaction.response.send_message(f"Acabas de expulsar a **{usuario}** por el siguiente motivo: **{razon}**", ephemeral=True)
    else:
        embed = discord.Embed(description=f"**{usuario}** ha sido expulsado del Discord.", color=0x2dc854, timestamp=interaction.created_at)
        embed.set_author(name=f'{guild.name}', icon_url=guild.icon)
        await interaction.response.send_message(f"Acabas de expulsar a **{usuario}** sin razón especificada.", ephemeral=True)

    await interaction.channel.send(embed=embed)	
  
	
########################################################################

@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.describe(canal='Canal al que quieres enviar el mensaje')
@app_commands.describe(texto='Texto a enviar')
@app_commands.describe(menciones='Si quieres mencionar algún rol en específico')
async def say(interaction: discord.Interaction, canal: discord.TextChannel, texto: str, menciones: Optional[discord.Role]):
	"""Envia un mensaje usando el Bot"""

	guild = interaction.guild

	try:
		if menciones is not None:
			await canal.send(f"{texto} \n {menciones.mention} {imagen}",)
		else:
			await canal.send(texto)
	except Forbidden:
		await interaction.response.send_message("No tengo los permisos para acceder a este canal!", ephemeral=True)
	except HTTPException:
		await interaction.response.send_message("Error HTTP desconocido", ephemeral=True)

	await interaction.response.send_message(f"Haz enviado un anuncio al canal <#{canal.id}>", ephemeral=True)

	if log_channel is not None and menciones is not None:
		embed1 = discord.Embed(description=f"<@{interaction.user.id}> acaba de mandar un anuncio al canal <#{canal.id}>: \n **{texto}** \n mencionando el rol {menciones.mention}", color=interaction.user.color, timestamp=interaction.created_at)
		embed1.set_author(name=f'{guild.name}', icon_url=guild.icon)
		await log_channel.send(embed=embed1)
	elif log_channel is not None:
		embed1 = discord.Embed(description=f"<@{interaction.user.id}> acaba de mandar un anuncio al canal <#{canal.id}>: \n **{texto}**", color=interaction.user.color, timestamp=interaction.created_at)
		embed1.set_author(name=f'{guild.name}', icon_url=guild.icon)
		await log_channel.send(embed=embed1)	
	
# //////////////////////////////////////////////////////////////////// #

@client.event
async def on_message(message):
	user = message.author.id
	id_guild = message.guild.id
	channel = message.channel
	conn = sqlite3.connect('Database BOT.db', timeout=20)
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS level_system (guild_id, user_id,xp INTEGER NOT NULL, target_xp INTEGER NOT NULL, level INTEGER NOT NULL)')
	#cur.execute('INSERT OR IGNORE INTO level_system (guild_id, user_id, xp, target_xp, level) VALUES (?, ?, 0, 25, 0)', (id_guild, user) )
	

	cur.execute('SELECT guild_id, user_id, xp, target_xp, level FROM level_system WHERE user_id = ? AND guild_id = ?', (user, id_guild) )
	results1 = cur.fetchone()

	if results1 is not None and message.author.bot is False:

		old_xp = results1[2]
		new_xp = old_xp + 5
		xp_to_level = results1[3]
		old_level = results1[4]

		if new_xp >= xp_to_level:

			new_level = old_level + 1
			new_xp_to_level = xp_to_level + 25
			embed = discord.Embed(title=f'¡Nuevo nivel!',description=f"¡Felicidades <@{user}>! acabas de alcanzar el nivel **{new_level}**", color=message.author.color)
			embed.set_thumbnail(url=message.author.display_avatar)			
			embed.set_footer(text=f'{message.guild.name}')
			await channel.send(embed=embed)

		else:
			new_level = old_level
			new_xp_to_level = xp_to_level

		cur.execute('UPDATE level_system SET xp = ?,target_xp = ? , level = ? WHERE user_id = ? AND guild_id = ?', (new_xp, new_xp_to_level, new_level, user, id_guild) )
		conn.commit()
		
	elif message.author.bot is False:

		cur.execute('INSERT OR IGNORE INTO level_system (guild_id, user_id, xp, target_xp, level) VALUES (?, ?, 1, 25, 0)', (id_guild, user) )
		conn.commit()
		
	conn.commit()
	conn.close()	
	
########################################################################
	
@client.tree.command()
async def leaderboard(interaction: discord.Interaction):
	"""Muestra quienes tienen el nivel más alto"""
	id_guild = interaction.guild.id

	conn = sqlite3.connect('Database BOT.db', timeout=30)
	cur = conn.cursor()
	cur.execute('SELECT user_id, xp, level FROM level_system WHERE guild_id = ? ORDER BY level DESC, xp DESC LIMIT 10', (id_guild,) )
	results = cur.fetchall()

	
	embed = discord.Embed(title=f'{interaction.guild.name}', color=0x4be25d, timestamp=interaction.created_at)

	for i, pos in enumerate(results, start=1):
		user_id, xp, level = pos

		embed.add_field(name=' ', value=f'**{i}.** <@{user_id}> \n `Nivel:` **{level}** \n `Experiencia:` **{xp}**', inline=False)
		embed.add_field(name=' ', value=' ', inline=False)			

	embed.set_author(name='Tabla de niveles')
	embed.set_thumbnail(url=interaction.guild.icon)			
	#embed.set_footer(text=f'{interaction.guild.name}')

	await interaction.response.send_message(embed=embed)
	conn.close()
		
  client.run(token)

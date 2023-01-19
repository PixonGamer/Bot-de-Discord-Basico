import discord
import asyncio

from discord import app_commands
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
  
  client.run(token)

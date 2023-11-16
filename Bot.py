import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, CommandOnCooldown
from discord.voice_client import VoiceClient
from discord import Intents
import random
import json
import os

#os.chdir("C:\\Users\\samir\\Music\\Discord Bot")
client = commands.Bot(command_prefix="g!",intents=Intents.all())

@client.event                                                #Status
async def on_ready():
  print("BOT IS NOW RUNNING")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="g!help"))

@client.event																		#Error Handling
async def on_command_error(ctx,error):
	if isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("Kindly `@mention` the user as well \n 	**USER ID also works**")
	elif isinstance(error,commands.MissingPermissions):
		await ctx.send("U do not have **Permission** to do that")
		await ctx.message.delete()
	elif isinstance(error,commands.CommandOnCooldown):
		await ctx.send(f"**{error}**")
	else:
		print(error)


@client.command(name="say",hidden=True)                                 			#Miscellaneous
async def say(ctx,*,arg):
	await ctx.message.delete()
	await ctx.send(f"**{arg}**")

@client.command(hidden=True)														#Miscellaneous
async def test(ctx):
  await ctx.send(ctx.author.name)

@client.command(name="ping",help="Check ping")
async def ping(ctx):
	await ctx.send(f"**Pong!!** {round(client.latency *1000)}ms. *SAB MOH MAYA HAI!!*")

@client.command(name="version",help="Get BOT Version",aliases=["Version","ver","Ver"])
async def version(ctx):
	await ctx.send("**Current Bot Version** : **0.1.5 Beta** \n ***DEV : SINISTER69#1665***")

@client.command(name="Credits",help="To Contact Dev",aliases=["credits","creds","Creds","Cred","cred"])
async def Credits(ctx):
	await ctx.send("***DEV : SINISTER69#1665*** \n **Kindly report all Bugs to Dev via Dm!! :pray:\n ** UR Suggestions are always Welcome!!** :v:")


@client.command(name="DESI",aliases=["desi","Desi"])
async def DESI(ctx,mem : discord.Member):
	D=random.randrange(0,101)
	Desi_em=discord.Embed(title="DESI RATE MACHINE",color=discord.Color(0xcf721a),description=f"**{mem.name} is {D}% DESI :flag_in:!!**")
	Desi_em.set_thumbnail(url=mem.avatar_url)
	Desi_em.set_footer(icon_url=ctx.author.avatar_url,text="VERIFIED")

	await ctx.send(embed=Desi_em)

@client.command(name="calculate",aliases=["maths","calc"],help="Basic Maths!! Kindly leave space between numbers and sign")
async def calculate(ctx, a : int, sign: str, b: int):						#Basic calculator
 	if sign=="x" or sign=="*":
 		await ctx.send(a*b)
 	elif sign=="+":
 		await ctx.send(a+b)
 	elif sign=="-":
 		await ctx.send(a-b)
 	elif sign=="/":
 		await ctx.send(a//b)
 	else:
 		await ctx.send("Invalid Sign")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<MODERATOR COMMANDS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#

@client.command(name="purge",aliases=["clear","p","Purge","PURGE"],hidden=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, mess=None):
	if mess==None:
		await ctx.send("Kindly specify the number of messages to be purged")
		await ctx.message.delete()
		return
	mess=int(mess)
	await ctx.channel.purge(limit= mess+1)

@client.command(name="kick",aliases=["k","Kick","KICK"],hidden=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, mem : discord.Member,*,reason="Reason not given"):
	await ctx.send(f"**{mem}** was Kicked by **{ctx.author.name}** \n Reason: {reason}")
	await ctx.message.delete()
	await member.kick(reason=reason)

@client.command(name="ban",aliases=["b","Ban","BAN"],hidden=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, mem : discord.Member,*,reason="Reason not given"):
	await ctx.send(f"**{mem}** was Banned by **{ctx.author.name}** \n Reason: {reason}")
	await ctx.message.delete()
	await member.ban(reason=reason)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Help Functions Start>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
async def start_bank(user):											#function for creating bank account
	users= await get_bank()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] ={}
		users[str(user.id)]["Wallet"]=1000
		users[str(user.id)]["Bank"]=1000
	with open("BANK.json","w") as f:
		json.dump(users,f)
	return True

Shop=[{"name":"DESI","price":100000,"brief":"UNCOMMON TAG" },				#The Shop
		{"name":"NEWBIE","price":10000,"brief":"BASIC TAG"}]

async def buy_process(user,item_n,amt=1):								#FUNCTION FOR Buying STUFF
	item_n=item_n.upper()
	n= None
	for item in Shop:
		name=item["name"].upper()
		if name==item_n:
			n=name
			price=item["price"]
			break
	if n==None:
		return [False,1]
	Total=price*amt
	
	users= await get_bank()
	
	bal= await update_bank(user)
	if bal[0]<Total:
		return[False,2]

	try:
		index=0
		t=None
		for things in users[str(user.id)]["bag"]:
			n=things["item"]
			if n==item_n:
				old_amt = things["amount"]
				new_amt = old_amt+ amt
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t=1
				break
			index+=1
		if t==None:
			obj={"item":item_n, "amount": amt}
			users[str(user.id)]["bag"].append(obj)
	except:
		obj={"item":item_n, "amount": amt}
		users[str(user.id)]["bag"] = [obj]

	with open("BANK.json","w") as f:
		json.dump(users,f)

	await update_bank(user,-1*Total,"Wallet")

	return[True,Total]

async def sell_process(user,item_n,Amt=1,price=None):									#Function for Selling Items
	item_n=item_n.upper()
	n=None
	for item in Shop:
		name=item["name"].upper()
		if name==item_n:
			n=name
			if price==None:
				price=item["price"]//2
			break
	if n==None:
		return [False,1]

	Total=price*Amt
	users=await get_bank()
	bal =await update_bank(user)

	try:
		index=0
		t=None
		for things in users[str(user.id)]["bag"]:
			n=things["item"]
			if n==item_n:
				old_amt = things["amount"]
				new_amt= old_amt - Amt
				if new_amt<0:
					return[False,2]
				users[str(user.id)]["bag"][index]["amount"] = new_amt
				t=1
				break
			index+=1
		if t==None:
			return [False,3]
	except:
		return [False,3]
	

	with open("BANK.json","w") as f:
		json.dump(users,f)

	await update_bank(user,Total,"Wallet")

	return [True,Total]
		


async def get_bank():												#short function to open BANK.json file
	with open("BANK.json","r") as f:
		users=json.load(f)
	
	return users

async def update_bank(user, change=0, mode="Wallet"):				#Function to Update money in Bank/Wallet
	users= await get_bank()

	users[str(user.id)][mode]+=change

	with open("BANK.json","w") as f:
		json.dump(users,f)

	bal=[users[str(user.id)]["Wallet"], users[str(user.id)]["Bank"]]

	return bal
 #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<HELP FUNCTION ENDS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#

 #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<CURRENCY COMMANDS START>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
																	
@client.command(name="balance",aliases=["bal"], help="Check Balance \n @mention the user whose balance u wanna view")#Command for Balance
async def balance(ctx,mem : discord.Member):
	await start_bank(ctx.author)
	await start_bank(mem)

	bal= await update_bank(mem)

	bal_em=discord.Embed(title=f"{mem.name}'s Balance",color=discord.Color(0x4b93d5))
	bal_em.add_field(name="***In Wallet***",value=f"**₹{bal[0]}**",inline= False)
	bal_em.add_field(name="***In Bank***",value=f"**₹{bal[1]}**",inline= False)
	bal_em.set_footer(icon_url=mem.avatar_url, text=f"ID : {mem.id}")

	await ctx.send(embed=bal_em)
    

@client.command(name="withdraw",aliases=["with"], help="Withdraw Cash from Bank")			 #Command to withdraw money from bank
async def withdraw(ctx, Amt = None):
	await start_bank(ctx.author)
	if Amt==None:
		await ctx.send("Kindly **specify the amount** U wanna Withdraw")
		return

	bal = await update_bank(ctx.author)
	if Amt=="all" or Amt=="max":
		Amt=bal[1]
	Amt=int(Amt)
	if Amt > bal[1]:
		await ctx.send("U don't have that much cash **Gareeb!!**")
		return
	if Amt<0:
		await ctx.send("**ERROR!!** Negative Value entered")
		return
	
	await update_bank(ctx.author,Amt)
	await update_bank(ctx.author,-1*Amt,"Bank")

	await ctx.send(f"**₹{Amt}** were Withdrawn from {ctx.author.name}'s Bank!! :thumbsup:")


@client.command(name="deposit",aliases=["dep"],help="Deposit cash in Bank ")	#Command to deposit money into bank
async def deposit(ctx, Amt = None):
	await start_bank(ctx.author)
	if Amt==None:
		await ctx.send("Kindly **specify the amount** U wanna Deposit")
		return

	bal = await update_bank(ctx.author)
	if Amt=="all" or Amt=="max":
		Amt=bal[0]
	Amt=int(Amt)
	if Amt > bal[0]:
		await ctx.send("U don't have that much money **Gareeb!!**")
		return
	if Amt<0:
		await ctx.send("**ERROR!!** Negative Value entered")
		return
	
	await update_bank(ctx.author,-1*Amt)
	await update_bank(ctx.author,Amt,"Bank")

	await ctx.send(f"**₹{Amt}** were Deposited in {ctx.author.name}'s Bank!! :thumbsup:")

@client.command(name="share",aliases=["give"],help="For sharing money with others \n Eg- `c!share @mention Amount`")
async def share(ctx, member : discord.Member, Amt = None):							#Command to share money with others
	await start_bank(ctx.author)
	await start_bank(member)

	if Amt==None:
		await ctx.send("Kindly **Specify the Amount** U wanna Give")
		return

	bal = await update_bank(ctx.author)
	if Amt=="all" or Amt=="Max":
		Amt=bal[0]
	Amt=int(Amt)
	if Amt > bal[0]:
		await ctx.send("U don't have that much Cash in Wallet")
		return
	if Amt<0:
		await ctx.send("**ERROR!!** Negative Value entered")
		return
	
	await update_bank(ctx.author,-1*Amt,"Wallet")
	await update_bank(member,Amt,"Wallet")

	await ctx.send(f"***Paisa Transfer Successful!!*** :thumbsup: \n **₹{Amt}** were given to **{member.mention}** by **{ctx.author.mention}**")

@client.command(name="leaderboard", aliases=["lb","rich"],help="Access the Global DESI Leaderboard")
async def leaderboard(ctx):
	users = await get_bank()
	lb={}
	total=[]
	for user in users:
		name = int(user)
		total_a=users[user]["Wallet"]+users[user]["Bank"]
		lb[total_a] = name
		total.append(total_a)
	total=sorted(total,reverse=True)

	lb_em=discord.Embed(title=f"DESI LEADERBOARD",description="Includes members of all servers | Based on NET WORTH",color=discord.Color(0x4dedff))
	c=1
	for amt in total:
		id_ =lb[amt]
		member = client.get_user(id_)
		lb_em.add_field(name=f"{c}. {member}",value=f"**₹{amt}**",inline=False)
		c+=1
		if c==10:
			break
	lb_em.set_footer(icon_url= ctx.author.avatar_url , text="ANDHA PAISAA! XD")
	await ctx.send(embed=lb_em)

@client.command(name="poorboard", aliases=["pb","poor"],help="Access the Global GAREEB Leaderboard")
async def leaderboard(ctx):
	users = await get_bank()
	pb={}
	total=[]
	for user in users:
		name = int(user)
		total_a=users[user]["Wallet"]+users[user]["Bank"]
		pb[total_a] = name
		total.append(total_a)
	total=sorted(total)

	pb_em=discord.Embed(title=f"DESI LEADERBOARD",description="Includes members of all servers | Based on NET WORTH",color=discord.Color(0x4dedff))
	c=1
	for amt in total:
		id_ =pb[amt]
		member = client.get_user(id_)
		pb_em.add_field(name=f"{c}. {member}",value=f"**₹{amt}**",inline=False)
		c+=1
		if c==10:
			break
	pb_em.set_footer(icon_url= ctx.author.avatar_url , text="GAREEBI OP! XD")
	await ctx.send(embed=pb_em)


@client.command(name="steal",hidden=True,aliases=["rob"] ,help="U know what this does don't U?! \n Eg- `c!steal @mention`")	#Command for Stealing
async def steal(ctx, member : discord.Member):
	await start_bank(ctx.author)
	await start_bank(member)

	bal = await update_bank(member)
	bal2= await update_bank(ctx.author)

	if bal2[0]<1000:
		await ctx.send("U need at least **₹1000** to rob others")
		return
	if bal[0]<=1000:
		await ctx.send(f"U should not steal from the **POOR**! :joy: ")
		return
	Steal=random.randrange(1,2)
	Stolen_Amt=random.randrange(0,bal[0])
	if Steal==1:
		await update_bank(ctx.author,Stolen_Amt,"Wallet")
		await update_bank(member,-1*Stolen_Amt,"Wallet")
		await ctx.send(f" **{ctx.author.name}'s** Robbery was Successful!! \n **{ctx.author.name}** stole **₹{Stolen_Amt}** from ***{member.name}'s*** Wallet!")
	elif Steal==2:
		await update_bank(ctx.author,-1000,"Wallet")
		ctx.send(f"**{ctx.author.name}'s** Robbery Failed!! \n **{ctx.author.name}** had to pay **₹1000** to stay out of JAIL!")

@client.command(name="work",help="Work Hourly to make Money")
@cooldown(1,3600,commands.BucketType.default)								#currency command - WORK
async def work(ctx):																				#Old style
	await start_bank(ctx.author)
	users= await get_bank()
	user=ctx.author

	salary= random.randrange(500,5000)

	await ctx.send(f"U earned ** ₹{salary} ** for working ")

	users[str(user.id)]["Wallet"]+= salary

	with open("BANK.json","w") as f:
		json.dump(users,f)

@client.command(name="beg",help="Beg for Coins XD")
@cooldown(1,5,commands.BucketType.default)
async def beg(ctx):
	await start_bank(ctx.author)
	Bheek=random.randrange(100,1000)
	await update_bank(ctx.author,Bheek)
	await ctx.send(f"DESI BOT gave **₹{Bheek}** to {ctx.author.name}")

@client.command(name="shop",aliases=["market"],help="View Shop")
async def shop(ctx):
	await start_bank(ctx.author)
	shop_em=discord.Embed(title="DESI SHOP",color=discord.Color.red())

	for item in Shop:
		Name=item["name"]
		Price=item["price"]
		Brief=item["brief"]
		shop_em.add_field(name= Name, value=f"₹{Price} | {Brief}")
	shop_em.set_footer(icon_url= ctx.author.avatar_url , text="No TAXES Enjoy!!")
	await ctx.send(embed=shop_em)

@client.command(name="buy",help="Buy stuff")
async def buy(ctx,item,Amt=1):
	await start_bank(ctx.author)

	Result= await buy_process(ctx.author,item,Amt)

	if not Result[0]:
		if Result[1]==1:
			await ctx.send(f"We don't sell **{item}** here!!")
		elif Result[1]==2:
			await ctx.send("**ERROR!!** Insufficient Funds in Wallet!")
		return
	if Result[0]:
		await ctx.send(f"***Transaction Successful!!*** \n **BILL** *-- {item} - {Amt} -- ₹{Result[1]}*")


@client.command(name="sell",help="Sell Stuff")
async def sell(ctx,item,Amt=1):
	await start_bank(ctx.author)

	Result= await sell_process(ctx.author,item,Amt)
	item=item.upper()
	if not Result[0]:
		if Result[1]==1:
			await ctx.send(f"**{item}** does not exist!!")
		elif Result[1]==2:
			await ctx.send(f"U don't have that many **{item} TAGS**")
		elif Result[1]==3:
			await ctx.send(f"U don't own **ANY** ***{item} TAG***!!")
		return
	if Result[0]:
		if Amt==1:
			await ctx.send(f"***Transaction Successful!!*** \n **{item} TAG** was sold for **₹{Result[1]}**")
		elif Amt>1:
			await ctx.send(f"***Transaction Successful!!*** \n **{Amt} {item} TAGS** were sold for **₹{Result[1]}**")



@client.command(name="inventory",aliases=["inv"],help="To check Inventory")
async def inventory(ctx):
	await start_bank(ctx.author)
	user=ctx.author
	users=await get_bank()

	try:
		bag = users[str(user.id)]["bag"]
	except:
		bag=[]

	inv_em=discord.Embed(title=f"{ctx.author.name}'s Inventory",color=discord.Color.blue())
	for item in bag:
		name=item["item"]
		amount=item["amount"]

		inv_em.add_field(name= name, value= amount)
	inv_em.set_footer(icon_url=ctx.author.avatar_url, text=f"ID : {ctx.author.id}")
	await ctx.send(embed=inv_em)


@client.command(name="toss",aliases=["flip"],help="Coin flip game \n Eg.- d!toss Heads/Tails Bet")	#Coin flipping Game
async def toss(ctx ,choice=None , Amt=None ):
	await start_bank(ctx.author)
	if choice==None or choice.isdigit():
		await ctx.send("**Heads** or **Tails**??")
		return
	if Amt==None:
		await ctx.send("How much do wanna Bet??")
		return
	Outcomes=("Heads","Tails")
	choice=str(choice)
	if choice not in  Outcomes:
		await ctx.send("**Invalid Choice!!** \n Try typing **Heads**/**Tails** instead. :wink:")
		return

	bal = await update_bank(ctx.author)

	if Amt=="all" or Amt=="max":
		Amt=bal[0]
	Amt=int(Amt)
	if Amt > bal[0]:
		await ctx.send("U don't have that much Cash in Wallet rn **Gareeb!!**")
		return
	if Amt<0:
		await ctx.send("**ERROR!!** Negative Value entered")
		return
	
	for i in range(1):
		Out=random.choice(Outcomes)
		if Out==choice:
			toss_em=discord.Embed(title="**DESI COIN FLIPPING GAME**",description=f"**{ctx.author.name} Won ₹{Amt}**",color=discord.Color.green())
			toss_em.set_thumbnail(url="https://justflipacoin.com/img/share-a-coin.png")
			toss_em.add_field(name=f"***{ctx.author.name}'s Call***",value=f"**{choice}**")
			toss_em.add_field(name=f"***RESULT***",value=f" :coin: **{choice}**")
			toss_em.set_footer(icon_url=ctx.author.avatar_url,text="CONGO!!")
			await update_bank(ctx.author,Amt,"Wallet")
		else:
			toss_em=discord.Embed(title="**DESI COIN FLIPPING GAME**",description=f"**{ctx.author.name} Lost ₹{Amt}**",color=discord.Color.red())
			toss_em.set_thumbnail(url="https://justflipacoin.com/img/share-a-coin.png")
			toss_em.add_field(name=f"***{ctx.author.name}'s Call***",value=f"**{choice}**")
			toss_em.add_field(name=f"***RESULT***",value=f" :coin: **{Out}**")
			toss_em.set_footer(icon_url=ctx.author.avatar_url,text="BETTER LUCK NEXT TIME!!")
			await update_bank(ctx.author,-1*Amt,"Wallet")
	await ctx.send(embed=toss_em)

@client.command(name="Slots",aliases=["slots","slot","Slot"],help="Try ur luck ")
async def Slots(ctx,bet=None):
	await start_bank(ctx.author)
	if bet==None:
		await ctx.send("How much do U wanna bet??")
		return
	bal=await update_bank(ctx.author)
	if bet=="all" or bet=="max":
		bet=bal[0]
	bet=int(bet)
	if bet>bal[0]:
		await ctx.send("U don't have that much Cash in Wallet rn **Gareeb!!**")
		return
	if bet<0:
		await ctx.send("**ERROR!!** Negative Value entered")
		return
	
	Result=[]
	Char=[":dart:",":sparkles:",":blue_heart: ",":skull_crossbones:",":biohazard:",":beer: ",":japanese_ogre:",":dollar:"]
	for i in range(3):
		Out=random.choice(Char)
		Result.append(Out)
	if Result[0]==Result[1] or Result[1]==Result[2] or Result[2]==Result[0]:
		await update_bank(ctx.author,bet,"Wallet")
		slots_em=discord.Embed(title="**DESI SLOTS**",color=discord.Color.green())
		slots_em.set_thumbnail(url="https://cdn.shortpixel.ai/client/q_glossy,ret_img/https://www.onlinecasinosguide.org/wp-content/uploads/2017/09/game-6-1-935x526.jpg")
		slots_em.add_field(name=f">{Result[0]} | {Result[1]} | {Result[2]}<",value=f"** U WON!! ₹{bet}** were added to **{ctx.author.name}'s** Wallet!",inline=False)
	elif Result[0]==Result[1] and Result[1]==Result[2] and Result[2]==Result[0]:
		await update_bank(ctx.author,2*bet,"Wallet")
		slots_em=discord.Embed(title="**DESI SLOTS**",color=discord.Color(0x48e917))
		slots_em.set_thumbnail(url="https://cdn.shortpixel.ai/client/q_glossy,ret_img/https://www.onlinecasinosguide.org/wp-content/uploads/2017/09/game-6-1-935x526.jpg")
		slots_em.add_field(name=f">{Result[0]} | {Result[1]} | {Result[2]}<",value=f"** U WON!! ₹{2*bet}** were added to **{ctx.author.name}'s** Wallet!",inline=False)
	else:
		await update_bank(ctx.author,-1*bet,"Wallet")
		slots_em=discord.Embed(title="**DESI SLOTS**",color=discord.Color.red())
		slots_em.set_thumbnail(url="https://cdn.shortpixel.ai/client/q_glossy,ret_img/https://www.onlinecasinosguide.org/wp-content/uploads/2017/09/game-6-1-935x526.jpg")
		slots_em.add_field(name=f">{Result[0]} | {Result[1]} | {Result[2]}<",value=f"** U LOST!! ₹{bet}** were deducted from **{ctx.author.name}'s** Wallet!",inline=False)
	slots_em.set_footer(icon_url=ctx.author.avatar_url, text=f"GG {ctx.author.name}!!")

	await ctx.send(embed=slots_em)

@client.command(name="bet",aliases=["Bet","gamble","Gamble"],help="Try ur luck!!")
async def bet(ctx,bet=None):
	await start_bank(ctx.author)
	if bet==None:
		await ctx.send("How much do U wanna bet??")
		return
	bal=await update_bank(ctx.author)
	if bet=="all" or bet=="max":
		bet=bal[0]
	bet=int(bet)
	if bet>bal[0]:
		await ctx.send("U don't have that much Cash in Wallet rn **Gareeb!!**")
		return
	if bet<0:
		await ctx.send("**ERROR!!** Negative Value entered")
		return
	Dice=[1,2,3,4,5,6]
	for i in range(1):
		P=random.choice(Dice)
		Comp=random.choice(Dice)
		if P>Comp:
			bet_em=discord.Embed(title="**DESI BETTING MACHINE**",color=discord.Color.green(),description=f"*{ctx.author.name} won ₹{bet}*")
			bet_em.add_field(name="**Player Rolled-**",value=f"***{P}***")
			bet_em.add_field(name="**Bot Rolled-**",value=f"***{Comp}***")
			bet_em.set_footer(icon_url=ctx.author.avatar_url,text="U WIN!!")
			await update_bank(ctx.author,bet,"Wallet")
		elif P<Comp:
			bet_em=discord.Embed(title="**DESI BETTING MACHINE**",color=discord.Color.red(),description=f"*{ctx.author.name} lost ₹{bet}*")
			bet_em.add_field(name="**Player Rolled-**",value=f"***{P}***")
			bet_em.add_field(name="**Bot Rolled-**",value=f"***{Comp}***")
			bet_em.set_footer(icon_url=ctx.author.avatar_url,text="BETTER LUCK NEXT TIME!!")
			await update_bank(ctx.author,-1*bet,"Wallet")
		elif P==Comp:
			bet_em=discord.Embed(title="**DESI BETTING MACHINE**",color=discord.Color(0xf0de17),description="*No Profit!! No Loss!!*")
			bet_em.add_field(name="**Player Rolled-**",value=f"***{P}***")
			bet_em.add_field(name="**Bot Rolled-**",value=f"***{Comp}***")
			bet_em.set_footer(icon_url=ctx.author.avatar_url,text="DRAW!!")

	await ctx.send(embed=bet_em)


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<CURRENCY COMMANDS ENDS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#


client.run("ODAxNzExODkxMTI1ODk1MTY5.YAkqYQ.4bKjZRO9NBJiHMVBpPmoMt4EGWA")
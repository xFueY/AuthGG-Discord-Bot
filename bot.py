import discord
from discord.ext import commands
import asyncio
import PyAuthGG
import json
import datetime
from time import strftime

config = json.load(open("config.json"))

AuthGGColor = 0x3569E6

client = commands.Bot(command_prefix=str(config['CommandPrefix']), case_insensitive=True)
client.remove_command("help")

AuthAdmin = PyAuthGG.Administration(str(config['AuthGGAdminAPI']))
AuthApp = PyAuthGG.Application(str(config['AuthGGAPI']), str(config['AuthGGAID']), str(config['AuthGGSecret']))

AuthGGBotVersion = "1.0.0"

@client.event
async def on_command_error(ctx, error):
    SendError = False

    if isinstance(error, commands.MissingRequiredArgument):
        SendError = True
    elif isinstance(error, commands.BadArgument):
        SendError = True
    elif isinstance(error, commands.MissingPermissions):
        SendError = True
    elif isinstance(error, commands.CommandNotFound):
        SendError = True

    if SendError == True:
        CommandErrorEmbed=discord.Embed(description=str(error), color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=CommandErrorEmbed)
    else:
        print(str(datetime.datetime.now())[:-7] + " | ERROR | Command: " + ctx.message.content + "\n-> " + str(error) + "\n")
        CommandErrorEmbed=discord.Embed(description="Something went wrong, please try again.", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=CommandErrorEmbed)


@client.command(name="Help", brief="Information", description="Shows all available commands", usage="Help <Category>")
async def Help(ctx, Category="None"):
    HelpEmbed=discord.Embed(title="AuthGG Help", description=f"Here you can find a list of all available commands, and how to use them.\n``<Argument>`` = Required\n``[Argument | Default]`` = Not Required", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    HelpEmbed.set_thumbnail(url="https://i.imgur.com/3GxXzyn.png")
    HelpEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    HelpEmbed.set_image(url="https://i.imgur.com/JT7PECu.png")
    HelpEmbed.set_footer(text="Developed by xFueY#7575")

    Categories = ['Information', 'Users', 'Licenses', 'HWID']
    CategoriesLower = ['information', 'users', 'licenses', 'hwid']

    if Category.lower() in CategoriesLower:
        for Command in client.commands:
            if Command.brief.lower() == Category.lower():
                HelpEmbed.add_field(name="**" + Command.name + "** | " + Command.description, value=str(config['CommandPrefix']) + "``" + Command.usage + "``", inline=False)

    else:
        for CategoryName in Categories:
            HelpEmbed.add_field(name=f"**{CategoryName}** | {CategoryName} Related Commands" , value=f"``{str(config['CommandPrefix'])}Help {CategoryName}``", inline=False)

    await ctx.send(embed=HelpEmbed)


@client.command(name="Info", brief="Information", description="Show bot info", usage="Info")
async def Info(ctx):
    CreditsEmbed=discord.Embed(title="AuthGG Discord Bot", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    CreditsEmbed.set_thumbnail(url="https://i.imgur.com/cd3jiBe.png")
    CreditsEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    CreditsEmbed.set_image(url="https://i.imgur.com/JT7PECu.png")
    CreditsEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))

    CreditsEmbed.add_field(name="Developer", value="[xFueY](https://github.com/xFueY/)")
    CreditsEmbed.add_field(name="Bot Version", value=AuthGGBotVersion)
    CreditsEmbed.add_field(name="PyAuthGG Version", value=PyAuthGG.Version)
    CreditsEmbed.add_field(name="Download", value="https://github.com/xFueY/AuthGG-Discord-Bot/", inline=False)

    await ctx.send(embed=CreditsEmbed)


@client.command(name="AppInfo", brief="Information", description="Fetch application information", usage="AppInfo")
@commands.has_permissions(administrator=True)
async def AppInfo(ctx):
    FetchedLicenseCount = AuthAdmin.FetchLicenseCount()
    FetchedInfo = AuthApp.Info()

    AppStatsEmbed=discord.Embed(title=FetchedInfo['name'], description=f"**Status:** {FetchedInfo['status']}\n**Version:** {FetchedInfo['version']}\n**Users:** {FetchedInfo['users']}\n**Licenses:** {FetchedLicenseCount['value']}\n\n**Login:** {FetchedInfo['login']}\n**Register:** {FetchedInfo['register']}\n**Freemode:** {FetchedInfo['freemode']}\n**Developermode:** {FetchedInfo['developermode']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    AppStatsEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    AppStatsEmbed.set_thumbnail(url=config['AppInfoLogo'])
    AppStatsEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=AppStatsEmbed)


@client.command(name="AuthStatus", brief="Information", description="Fetch AuthGG's Service Status", usage="AuthStatus")
@commands.has_permissions(administrator=True)
async def AuthStatus(ctx):
    FetchedStatus = AuthAdmin.Status()

    AuthStatusEmbed=discord.Embed(title="AuthGG Status", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    AuthStatusEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    AuthStatusEmbed.set_thumbnail(url=config['AuthGGIcon'])
    AuthStatusEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))

    AuthStatusEmbed.add_field(name="Backend/API", value=str(FetchedStatus['Backend/API']), inline=False)
    AuthStatusEmbed.add_field(name="Frontend", value=str(FetchedStatus['Frontend']), inline=False)
    AuthStatusEmbed.add_field(name="S3 Storage", value=str(FetchedStatus['S3 Storage']), inline=False)

    await ctx.send(embed=AuthStatusEmbed)


@client.command(name="FetchUser", brief="Users", description="Fetch a users info", usage="FetchUser <Username>")
@commands.has_permissions(administrator=True)
async def FetchUser(ctx, Username):
    FetchedUser = AuthAdmin.FetchUser(Username)

    if FetchedUser['status'] == "success":
        FetchedLicenses = AuthAdmin.FetchUsedLicenses(Username)

        FetchUserEmbed=discord.Embed(title="Fetch User", description=f"**Status:** {FetchedUser['status'].replace('success', 'Success')}\n\n**Username:** {FetchedUser['username']}\n**E-Mail:** {FetchedUser['email']}\n**Rank:** {FetchedUser['rank']}\n**HWID:** {FetchedUser['hwid']}\n**Variable:** {FetchedUser['variable']}\n**Last Login:** {FetchedUser['lastlogin']}\n**Last IP:** {FetchedUser['lastip']}\n**Expiry:** {FetchedUser['expiry']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        FetchUserEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))

        FetchUserEmbed.add_field(name="Licenses Used", value="".join(str(x['token'] + " | " + x['days'] + " days") for x in FetchedLicenses['Licenses']), inline=False)

        await ctx.send(embed=FetchUserEmbed)

    else:
        FetchUserEmbed=discord.Embed(title=Username, description=f"**Status:** {FetchedUser['status'].replace('failed', 'Failed')}\n**Message:** {FetchedUser['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        FetchUserEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
        FetchUserEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
        await ctx.send(embed=FetchUserEmbed)


@client.command(name="FetchUsers", brief="Users", description="Fetch all users in application", usage="FetchUsers")
@commands.has_permissions(administrator=True)
async def FetchUsers(ctx):
    FetchedUsers = AuthAdmin.FetchUsers()

    CurrentNumber = 0

    FetchedUsersEmbed=discord.Embed(title=str(FetchedUsers[str(CurrentNumber)]['username']) + " (" + str(CurrentNumber + 1) + "/" + str(len(FetchedUsers)) + ")", description=f"**Username:** {FetchedUsers[str(CurrentNumber)]['username']}\n**E-Mail:** {FetchedUsers[str(CurrentNumber)]['email']}\n**Rank:** {FetchedUsers[str(CurrentNumber)]['rank']}\n**HWID:** {FetchedUsers[str(CurrentNumber)]['hwid']}\n**Variable:** {FetchedUsers[str(CurrentNumber)]['variable']}\n**Last Login:** {FetchedUsers[str(CurrentNumber)]['lastlogin']}\n**Last IP:** {FetchedUsers[str(CurrentNumber)]['lastip']}\n**Expiry:** {FetchedUsers[str(CurrentNumber)]['expiry_date']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    FetchedUsersEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    FetchedUsersEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    MainMessage = await ctx.send(embed=FetchedUsersEmbed)

    await MainMessage.add_reaction("⏪")
    await MainMessage.add_reaction("◀️")
    await MainMessage.add_reaction("▶️")
    await MainMessage.add_reaction("⏩")

    AllowedReactions = ['⏪', '◀️', '▶️', '⏩']

    def ReactionCheck(Reaction, User):
        return str(Reaction.emoji) in AllowedReactions and Reaction.message.id == MainMessage.id and User.id == ctx.author.id

    while True:
        try:
            Reaction, User = await client.wait_for("reaction_add", timeout=600, check=ReactionCheck)
        except asyncio.TimeoutError:
            await MainMessage.clear_reactions()
            break
        else:
            await MainMessage.remove_reaction(str(Reaction.emoji), User)
            if str(Reaction.emoji) == "⏪":
                CurrentNumber = 0

            if str(Reaction.emoji) == "◀️":
                if CurrentNumber != 0:
                    CurrentNumber -= 1

            elif str(Reaction.emoji) == "▶️":
                if CurrentNumber + 1 != len(FetchedUsers):
                    CurrentNumber += 1

            elif str(Reaction.emoji) == "⏩":
                CurrentNumber = len(FetchedUsers) - 1

            NewFetchedUsersEmbed=discord.Embed(title=str(FetchedUsers[str(CurrentNumber)]['username']) + " (" + str(CurrentNumber + 1) + "/" + str(len(FetchedUsers)) + ")", description=f"**Username:** {FetchedUsers[str(CurrentNumber)]['username']}\n**E-Mail:** {FetchedUsers[str(CurrentNumber)]['email']}\n**Rank:** {FetchedUsers[str(CurrentNumber)]['rank']}\n**HWID:** {FetchedUsers[str(CurrentNumber)]['hwid']}\n**Variable:** {FetchedUsers[str(CurrentNumber)]['variable']}\n**Last Login:** {FetchedUsers[str(CurrentNumber)]['lastlogin']}\n**Last IP:** {FetchedUsers[str(CurrentNumber)]['lastip']}\n**Expiry:** {FetchedUsers[str(CurrentNumber)]['expiry_date']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
            NewFetchedUsersEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
            NewFetchedUsersEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
            await MainMessage.edit(embed=NewFetchedUsersEmbed)


@client.command(name="DeleteUser", brief="Users", description="Delete a user", usage="DeleteUser <Username>")
@commands.has_permissions(administrator=True)
async def DeleteUser(ctx, Username):
    DeletedUser = AuthAdmin.DeleteUser(Username)

    DeleteUserEmbed=discord.Embed(title="Delete User", description=f"**Status:** {DeletedUser['status']}\n**Info:** {DeletedUser['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    DeleteUserEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    DeleteUserEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=DeleteUserEmbed)


@client.command(name="ChangeVariable", brief="Users", description="Change a users variable", usage="ChangeVariable <Username> <Variable>")
@commands.has_permissions(administrator=True)
async def ChangeVariable(ctx, Username, *, Variable):
    ChangedVariable = AuthAdmin.ChangeVariable(Username, Variable)

    ChangeVariableEmbed=discord.Embed(title="Change Variable", description=f"**Status:** {ChangedVariable['status']}\n**Info:** {ChangedVariable['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    ChangeVariableEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    ChangeVariableEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=ChangeVariableEmbed)


@client.command(name="ChangeRank", brief="Users", description="Change a users rank", usage="ChangeRank <Username> <Rank>")
@commands.has_permissions(administrator=True)
async def ChangeRank(ctx, Username, Rank : int):
    ChangedRank = AuthAdmin.ChangeRank(Username, Rank)

    ChangeRankEmbed=discord.Embed(title="Change Variable", description=f"**Status:** {ChangedRank['status']}\n**Info:** {ChangedRank['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    ChangeRankEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    ChangeRankEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=ChangeRankEmbed)


@client.command(name="ChangePassword", brief="Users", description="Change a users password", usage="ChangePassword <Username> <Password>")
@commands.has_permissions(administrator=True)
async def ChangePassword(ctx, Username, Password):
    ChangedPassword = AuthAdmin.ChangePassword(Username, Password)

    ChangePasswordEmbed=discord.Embed(title="Change Password", description=f"**Status:** {ChangedPassword['status']}\n**Info:** {ChangedPassword['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    ChangePasswordEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    ChangePasswordEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=ChangePasswordEmbed)


@client.command(name="FetchLicense", brief="Licenses", description="Fetch license information", usage="FetchLicense <License>")
@commands.has_permissions(administrator=True)
async def FetchLicense(ctx, License):
    FetchedLicense = AuthAdmin.FetchLicense(License)

    if FetchedLicense['status'] == "success":
        FetchLicenseEmbed=discord.Embed(title="Fetch License", description=f"**Status:** {FetchedLicense['status']}\n**License:** {FetchedLicense['license']}\n**Rank:** {FetchedLicense['rank']}\n**Used:** {FetchedLicense['used']}\n**Used By:** {FetchedLicense['used_by']}\n**Created:** {FetchedLicense['created']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        FetchLicenseEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
        FetchLicenseEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
        await ctx.send(embed=FetchLicenseEmbed)

    else:
        FetchLicenseEmbed=discord.Embed(title="Fetch License", description=f"**Status:** {FetchedLicense['status']}\n**Info:** {FetchedLicense['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        FetchLicenseEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
        FetchLicenseEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
        await ctx.send(embed=FetchLicenseEmbed)


@client.command(name="FetchLicenses", brief="Licenses", description="Fetch all licenses in application", usage="FetchLicenses")
@commands.has_permissions(administrator=True)
async def FetchLicenses(ctx):
    FetchedLicenses = AuthAdmin.FetchLicenses()

    CurrentNumber = 0

    FetchLicensesEmbed=discord.Embed(title="Fetch Licenses (" + str(CurrentNumber + 1) + "/" + str(len(FetchedLicenses)) + ")", description=f"**License:** {FetchedLicenses[str(CurrentNumber)]['token']}\n**Rank:** {FetchedLicenses[str(CurrentNumber)]['rank']}\n**Rank:** {FetchedLicenses[str(CurrentNumber)]['rank']}\n**Used:** {FetchedLicenses[str(CurrentNumber)]['used'].replace('0', 'False').replace('1', 'True')}\n**Used By:** {FetchedLicenses[str(CurrentNumber)]['used_by']}\n**Days:** {FetchedLicenses[str(CurrentNumber)]['days']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    FetchLicensesEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    FetchLicensesEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    MainMessage = await ctx.send(embed=FetchLicensesEmbed)

    await MainMessage.add_reaction("⏪")
    await MainMessage.add_reaction("◀️")
    await MainMessage.add_reaction("▶️")
    await MainMessage.add_reaction("⏩")

    AllowedReactions = ['⏪', '◀️', '▶️', '⏩']

    def ReactionCheck(Reaction, User):
        return str(Reaction.emoji) in AllowedReactions and Reaction.message.id == MainMessage.id and User.id == ctx.author.id

    while True:
        try:
            Reaction, User = await client.wait_for("reaction_add", timeout=600, check=ReactionCheck)
        except asyncio.TimeoutError:
            await MainMessage.clear_reactions()
            break
        else:
            await MainMessage.remove_reaction(str(Reaction.emoji), User)
            if str(Reaction.emoji) == "⏪":
                CurrentNumber = 0

            if str(Reaction.emoji) == "◀️":
                if CurrentNumber != 0:
                    CurrentNumber -= 1

            elif str(Reaction.emoji) == "▶️":
                if CurrentNumber + 1 != len(FetchedLicenses):
                    CurrentNumber += 1

            elif str(Reaction.emoji) == "⏩":
                CurrentNumber = len(FetchedLicenses) - 1

            NewFetchLicensesEmbed=discord.Embed(title="Fetch Licenses (" + str(CurrentNumber + 1) + "/" + str(len(FetchedLicenses)) + ")", description=f"**License:** {FetchedLicenses[str(CurrentNumber)]['token']}\n**Rank:** {FetchedLicenses[str(CurrentNumber)]['rank']}\n**Rank:** {FetchedLicenses[str(CurrentNumber)]['rank']}\n**Used:** {FetchedLicenses[str(CurrentNumber)]['used'].replace('0', 'False').replace('1', 'True')}\n**Used By:** {FetchedLicenses[str(CurrentNumber)]['used_by']}\n**Days:** {FetchedLicenses[str(CurrentNumber)]['days']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
            NewFetchLicensesEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
            NewFetchLicensesEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
            await MainMessage.edit(embed=NewFetchLicensesEmbed)


@client.command(name="DeleteLicense", brief="Licenses", description="Delete a license", usage="DeleteLicense <License>")
@commands.has_permissions(administrator=True)
async def DeleteLicense(ctx, License):
    DeletedLicense = AuthAdmin.DeleteLicense(License)

    DeleteLicenseEmbed=discord.Embed(title="Delete License", description=f"**Status:** {DeletedLicense['status']}\n**Info:** {DeletedLicense['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    DeleteLicenseEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    DeleteLicenseEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=DeleteLicenseEmbed)


@client.command(name="UseLicense", brief="Licenses", description="Use a license", usage="UseLicense <License>")
@commands.has_permissions(administrator=True)
async def UseLicense(ctx, License):
    UsedLicense = AuthAdmin.UseLicense(License)

    UseLicenseEmbed=discord.Embed(title="Use License", description=f"**Status:** {UsedLicense['status']}\n**Info:** {UsedLicense['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    UseLicenseEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    UseLicenseEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=UseLicenseEmbed)


@client.command(name="UnuseLicense", brief="Licenses", description="Use a license", usage="UnuseLicense <License>")
@commands.has_permissions(administrator=True)
async def UnuseLicense(ctx, License):
    UnusedLicense = AuthAdmin.UnuseLicense(License)

    UnuseLicenseEmbed=discord.Embed(title="Use License", description=f"**Status:** {UnusedLicense['status']}\n**Info:** {UnusedLicense['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    UnuseLicenseEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    UnuseLicenseEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=UnuseLicenseEmbed)


@client.command(name="GenerateLicense", aliases=['GenKeys', 'GenKey', 'Gen'], brief="Licenses", description="Generate a license", usage="GenerateLicense [Amount | 1] [Days | 9998] [Level | 1] [Format | 2] [Prefix | None] [Length | 0]")
@commands.has_permissions(administrator=True)
async def GenerateLicense(ctx, Amount : int = 1, Days : int = 1, Level : int = 1, Format : int = 2, Prefix : str = " ", Length : int = 0):

    if Amount < 50:
        GeneratedLicense = AuthAdmin.GenerateLicense(Amount, Days, Level, Format, Prefix, Length)

        LicenseListed = "".join(x[1] + "\n" for x in GeneratedLicense.items()) # str(int(x[0]) + 1) + " | " +

        GenerateLicenseEmbed=discord.Embed(title="Generate License", description=f"```\n{LicenseListed}```", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        GenerateLicenseEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
        GenerateLicenseEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
        await ctx.send(embed=GenerateLicenseEmbed)

    else:
        GeneratedLicenseEmbed=discord.Embed(description="You can't create more than 50 licenses at once, because Discord does not allow more than 2000 characters per message.", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=GeneratedLicenseEmbed)


@client.command(name="FetchHWID", brief="HWID", description="Fetch a users HWID", usage="FetchHWID <Username>")
@commands.has_permissions(administrator=True)
async def FetchHWID(ctx, Username):
    FetchedHWID = AuthAdmin.FetchHWID(Username)

    if FetchedHWID['status'] == "success":
        FetchHWIDEmbed=discord.Embed(title="Fetch HWID", description=f"**Status:** {FetchedHWID['status']}\n**HWID:** {FetchedHWID['value']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        FetchHWIDEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
        FetchHWIDEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
        await ctx.send(embed=FetchHWIDEmbed)

    else:
        FetchHWIDEmbed=discord.Embed(title="Fetch HWID", description=f"**Status:** {FetchedHWID['status']}\n**Info:** {FetchedHWID['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
        FetchHWIDEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
        FetchHWIDEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
        await ctx.send(embed=FetchHWIDEmbed)


@client.command(name="ResetHWID", brief="HWID", description="Reset a users HWID", usage="ResetHWID <Username>")
@commands.has_permissions(administrator=True)
async def ResetHWID(ctx, Username):
    ResetHWIDResponse = AuthAdmin.ResetHWID(Username)

    ResetHWIDEmbed=discord.Embed(title="Reset HWID", description=f"**Status:** {ResetHWIDResponse['status']}\n**Info:** {ResetHWIDResponse['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    ResetHWIDEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    ResetHWIDEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=ResetHWIDEmbed)


@client.command(name="SetHWID", brief="HWID", description="Set a users HWID", usage="SetHWID <Username> <HWID>")
@commands.has_permissions(administrator=True)
async def SetHWID(ctx, Username, HWID):
    SetHWIDResponse = AuthAdmin.SetHWID(Username, HWID)

    SetHWIDEmbed=discord.Embed(title="Set HWID", description=f"**Status:** {SetHWIDResponse['status']}\n**Info:** {SetHWIDResponse['info']}", color=AuthGGColor, timestamp=datetime.datetime.utcnow())
    SetHWIDEmbed.set_author(name=config['AuthGGName'], icon_url=config['AuthGGIcon'], url=config['AuthGGUrl'])
    SetHWIDEmbed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url_as(format=None, static_format='png', size=1024))
    await ctx.send(embed=SetHWIDEmbed)


client.run(str(config['DiscordToken']))

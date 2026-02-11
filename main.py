import discord
from discord.ext import commands
import os
from dotenv import (load_dotenv)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # ← REQUIRED
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

################################# POLICE FORM #################################
class ApplicationModalPolice(discord.ui.Modal, title="Police Application Form"):
    name = discord.ui.TextInput(label="What is your Name?", required=True)
    reason = discord.ui.TextInput(label="Why do you want to the Police?", style=discord.TextStyle.paragraph, required=True)
    experience = discord.ui.TextInput(label="Why do you want to apply?", style=discord.TextStyle.paragraph, required=True)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📄 Police Service Join Application",
            color=discord.Color.blue()
        )
        embed.add_field(name="Name", value=self.name.value, inline=False)
        embed.add_field(name="Reason for Joining the police", value=self.reason.value, inline=False)
        embed.add_field(name="Any previous experience", value=self.experience.value, inline=False)
        review_channel = interaction.guild.get_channel(1470784191447961663)
        await review_channel.send(
            embed=embed,
            view=ReviewView(interaction.user.id)
        )
        await interaction.response.send_message(
            "✅ Application has been submitted!",
            ephemeral=True
        )
class ReviewView(discord.ui.View):
    def __init__(self, applicant_id: int):
        super().__init__(timeout=None)  # ← REQUIRED
        self.applicant_id = applicant_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        role = interaction.guild.get_role(1461845377845301533)
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                "❌ You are not authorised to do this.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        member = interaction.guild.get_member(self.applicant_id)
        if member is None:
            try:
                member = await interaction.guild.fetch_member(self.applicant_id)
            except discord.NotFound:
                member = None
        if member is None:
            await interaction.response.send_message(
                "⚠️ Applicant not found in server.",
                ephemeral=True
            )
            return

        role = interaction.guild.get_role(1461845378109538478)
        role2 = interaction.guild.get_role(1461845378109538475)
        if member and role:
            await member.add_roles(role, role2, reason="Application Approved")
        button.disabled = True
        self.children[1].disabled = True
        await interaction.message.edit(view=self)
        try:
            await member.send(
                f"🎉 Congratulations! You have passed your application and it has been approved for you to join the force!"
            )
        except discord.Forbidden:
            print("User has DMs Closed")
        await interaction.response.send_message(
            f"✅ Approved {member.mention} and sent them a DM.",
            ephemeral=True
        )
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        member = interaction.guild.get_member(self.applicant_id)
        button.disabled = True
        self.children[0].disabled = True
        await interaction.message.edit(view=self)
        if member:
            try:
                await member.send(
                    "❌ Your application was Denied, please don't hesitate to try again, there is a required 7day cool down period, failure to follow this will result in this being reset every time we receive an application from you."
                )
            except discord.Forbidden:
                print("User has DMs Closed")
        await interaction.response.send_message(
            f"❌ Denied {member.mention} and sent them a DM.",
            ephemeral=True
        )

class ApplyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Open Police Application Form",
        style=discord.ButtonStyle.primary
    )
    async def police(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(ApplicationModalPolice())
@bot.command()
async def police(ctx):
    await ctx.send(
        "Click the button below to apply:",
        view=ApplyView()
    )

bot.run(TOKEN)
